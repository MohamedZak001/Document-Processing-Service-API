from PIL import Image
from .models import ImageFile
from django.conf import settings
import os




class ImageService:

    def __init__(self, instance: ImageFile):
        self.instance = instance
    
    def rotate(self, angle: float):
        image = self.instance.image
        with Image.open(image.path) as img:
            rotated_img = img.rotate(angle, expand=True)
            path = self._rotated_image_path(image.path, rotated_img)
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            rotated_img.save(path)
            return path


    def _rotated_image_path(self, original_path, rotated_img):
        filename, extension = os.path.splitext(os.path.basename(original_path))
        new_filename = f"{filename}_rotated{extension}"
        user_id = self.instance.id
        return os.path.join(settings.MEDIA_ROOT,"users",str(user_id), "rotated_images", new_filename)
