import logging
from asgiref.sync import sync_to_async
from asyncio import sleep

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import StreamingHttpResponse, Http404
from django.views import View
from django.http import JsonResponse

from images.forms import UploadForm
from images.models import Image
from images.tables import ImageTable

logger = logging.getLogger(__name__)


def health_check(request):
    return JsonResponse({"status": "ok"})

class IndexView(TemplateView):
    template_name = "images/index.html"

    def get_context_data(self, **kwargs):
        images = Image.objects.all()

        context = super().get_context_data(**kwargs)

        context['images']      = images
        context['image_table'] = ImageTable(images)
        context['upload_form'] = UploadForm()

        return context

class UploadView(CreateView):
    form_class = UploadForm
    http_method_names = ['post']

    def form_valid(self, form):
        print("form_valid")
        # Create instance but don’t commit yet
        obj = form.save(commit=False)

        # Read raw bytes from uploaded file
        uploaded_file = self.request.FILES["image_upload"]
        obj.filedata = uploaded_file.read()

        # Save final object
        obj.save()

        return super().form_valid(form)

    success_url = reverse_lazy("images-index")

class ImageStreamView(View):
    async def get(self, request, pk, *args, **kwargs):
        # Fetch object asynchronously (wrap ORM call)
        try:
            image_obj = await sync_to_async(Image.objects.get)(pk=pk)
        except Image.DoesNotExist:
            raise Http404("Image not found")

        # Generator to stream chunks
        async def image_iterator(chunk_size=64*1024):
            data = image_obj.filedata
            for i in range(0, len(data), chunk_size):
                yield data[i:i+chunk_size]

        response = StreamingHttpResponse(
            image_iterator(),
            content_type="image/png"
        )
        response["Content-Length"] = len(image_obj.filedata)
        response["Content-Disposition"] = f'inline; filename="{image_obj.file}"'

        return response