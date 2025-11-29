import logging

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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
