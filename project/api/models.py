import os
from PIL import Image
from PyPDF2 import PdfReader

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model




def image_upload_path(instance: 'ImageFile', filename) -> str:
    return f"users/{instance.user.id}/images/{filename}"


class ImageFile(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="image_files")
    image = models.ImageField(upload_to=image_upload_path)
    uploaded_at =  models.DateTimeField(default=timezone.now, editable=False)

    @property
    def location(self):
        return self.image.path

    @property
    def width(self):
        if not hasattr(self,"_width"):
            self.read_image_meta_data()
        return self._width

    @property
    def height(self):
        if not hasattr(self,"_height"):
            self.read_image_meta_data()
        return self._height

    @property
    def number_of_channels(self):
        if not hasattr(self,"_number_of_channels"):
            self.read_image_meta_data()
        return self._number_of_channels
        
    def read_image_meta_data(self):
        with Image.open(self.image) as img:
            self._width = img.width
            self._height = img.height
            self._number_of_channels = len(img.getbands())
    

    def delete(self, *args, **kwargs):

        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)



def pdf_upload_path(instance: 'PdfFile', filename) -> str:
    return f"users/{instance.user.id}/pdfs/{filename}"



class PdfFile(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="pdf_files")
    pdf = models.FileField(upload_to=pdf_upload_path)
    uploaded_at =  models.DateTimeField(default=timezone.now, editable=False)

    @property
    def location(self):
        return self.pdf.path

    @property
    def number_of_pages(self):
        if not hasattr(self,"_number_of_pages"):
            self.read_pdf_meta_data()
        return self._number_of_pages

    @property
    def page_width(self):
        if not hasattr(self,"_page_width"):
            self.read_pdf_meta_data()
        return self._page_width

    @property
    def page_height(self):
        if not hasattr(self,"_page_height"):
            self.read_pdf_meta_data()
        return self._page_height
        
    def read_pdf_meta_data(self):

        reader = PdfReader(self.pdf.path)
        self._number_of_pages = len(reader.pages)

        first_page = reader.pages[0]
        self._page_width = float(first_page.mediabox.width)
        self._page_height = float(first_page.mediabox.height)
    

    def delete(self, *args, **kwargs):

        if self.pdf:
            if os.path.isfile(self.pdf.path):
                os.remove(self.pdf.path)
        super().delete(*args, **kwargs)