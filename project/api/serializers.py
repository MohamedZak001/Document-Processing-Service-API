from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import ImageFile






class FileUploadSerializer(serializers.Serializer):
    pdf = serializers.FileField(required=False, help_text="the pdf file to be uploaded")
    image = serializers.ImageField(required=False, help_text="the image file to be uploaded")


    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs.get('pdf') and not attrs.get('image'):
            raise ValidationError("Either 'pdf' or 'image' must be provided.")
        print(attrs)
        return attrs
    


# image serializers

class ListImageSerializer(serializers.ModelSerializer):


    class Meta:
        model = ImageFile
        fields = [
            "title", "image","uploaded_at"
        ]



class RetrieveImageSerializer(serializers.Serializer):

    location = serializers.CharField()
    width = serializers.DecimalField(max_digits=6, decimal_places=2)
    height = serializers.DecimalField(max_digits=6,decimal_places=2)
    number_of_channels = serializers.DecimalField(max_digits=6,decimal_places=2)


    def get_location(self, instance):
        return instance.location

    def get_width(self, instance):
        return instance.width

    def get_height(self, instance):
        return instance.height

    def get_number_of_channels(self, instance):
        return instance.number_of_channels


class RotateImageSerializer(serializers.Serializer):
    angle = serializers.DecimalField(max_digits=6,decimal_places=2)
    image = serializers.IntegerField()



