from django.db import models

class Imageupload(models.Model):
    title = models.CharField(max_length=100)
    img = models.FileField(null=True, blank=True, upload_to='')
    def __str__(self):
        return self.title
