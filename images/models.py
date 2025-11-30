from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=128)
    file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filedata = models.BinaryField()     # We will store the actual file here for restore ability, bad idea but I've always wanted to do it

    class Meta:
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        self.file.seek(0)
        self.filedata = self.file.read()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
