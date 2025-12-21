import django_tables2 as tables
from django_tables2.utils import A
from images.models import Image

class ImageTable(tables.Table):
    # preview = tables.TemplateColumn(
    #     '<img src="{{record.file.url}}" class="img-fluid" height="25" width="25">'
    # )

    imageurl = tables.LinkColumn(
        "image-stream",
        kwargs={"pk": tables.A("pk")},
        text="Link"
    )

    size = tables.Column(empty_values=[])

    class Meta:
        model = Image
        orderable = False
        # fields = ("preview", "title", "uploaded_at", "imageurl")
        fields = ( "title", "uploaded_at", "size", "imageurl")

    def render_size(self, record):
        return record.file.size