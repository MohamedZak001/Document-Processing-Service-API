import os
from PIL import Image
from pdf2image import convert_from_path

from django.conf import settings

from .models import ImageFile, PdfFile




class ImageService:

    def __init__(self, instance: ImageFile):
        self.instance = instance
    
    def rotate(self, angle: float):
        image = self.instance.image
        with Image.open(image.path) as img:
            rotated_img = img.rotate(angle, expand=True)
            path = self._rotated_image_path(image.path)
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            rotated_img.save(path)
            return path

    def _rotated_image_path(self, original_path):
        filename, extension = os.path.splitext(os.path.basename(original_path))
        new_filename = f"{filename}_rotated{extension}"
        user_id = self.instance.user.id
        return os.path.join(settings.MEDIA_ROOT,"users",str(user_id),"images", "rotated_images", new_filename)



class PDFService:

    def __init__(self, instance: PdfFile):
        self.instance = instance
    
    def convert(self):
        pdf = self.instance.pdf
        images = convert_from_path(pdf.path)
        image_path = None
        for i, image in enumerate(images):
            image_path = self._converted_pdf_to_image_path(pdf.path, i)
            directory = os.path.dirname(image_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            image.save(image_path)
            # save only the first image
            break
        return image_path

    def _converted_pdf_to_image_path(self, original_path, num):
        filename, _ = os.path.splitext(os.path.basename(original_path))
        new_filename = f"{filename}_converted_{num}.png"
        user_id = self.instance.user.id
        return os.path.join(settings.MEDIA_ROOT,"users",str(user_id),"pdfs", "converted_pdfs", new_filename)
