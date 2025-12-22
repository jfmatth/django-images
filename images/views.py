import logging
from asgiref.sync import sync_to_async
from asyncio import sleep

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import StreamingHttpResponse, Http404
from django.views import View

from images.forms import UploadForm
from images.models import Image
from images.tables import ImageTable

logger = logging.getLogger(__name__)

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

    success_url = reverse_lazy("images-index")

class ImageStreamView(View):
    # async def get(self, request, pk, *args, **kwargs):
    #     # Fetch object asynchronously (wrap ORM call)
    #     try:
    #         image_obj = await sync_to_async(Image.objects.get)(pk=pk)
    #     except Image.DoesNotExist:
    #         raise Http404("Image not found")

    #     # Generator to stream chunks
    #     async def image_iterator(chunk_size=64*1024):
    #         data = image_obj.filedata
    #         for i in range(0, len(data), chunk_size):
    #             yield data[i:i+chunk_size]

    #     response = StreamingHttpResponse(
    #         image_iterator(),
    #         content_type="image/png"
    #     )
    #     response["Content-Length"] = len(image_obj.filedata)
    #     response["Content-Disposition"] = f'inline; filename="{image_obj.file}"'

    #     return response

    async def get(self, request, pk):
        image_obj = await sync_to_async(Image.objects.get)(pk=pk)
        file = image_obj.file.open("rb")  # if using FileField

        async def iterator(chunk_size=64*1024):
            while True:
                chunk = await sync_to_async(file.read)(chunk_size)
                if not chunk:
                    break
                yield chunk

        response = StreamingHttpResponse(iterator(), content_type="image/png")
        response["Content-Length"] = image_obj.file.size
        return response