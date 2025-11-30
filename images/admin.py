from django.contrib import admin

from images.models import Image


class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at','file')
    list_display = ('__str__', 'uploaded_at', 'file')


admin.site.register(Image, ImageAdmin)

