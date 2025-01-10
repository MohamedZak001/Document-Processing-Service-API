from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import ImageFile, PdfFile




class FileUploadSerializer(serializers.Serializer):
    pdf = serializers.FileField(required=False, help_text="the pdf file to be uploaded")
    image = serializers.ImageField(required=False, help_text="the image file to be uploaded")

    def validate_pdf(self, value):
        if value:
            if not value.name.lower().endswith('.pdf'):
                raise ValidationError("Only PDF files are allowed.")
        return value

    def validate_image(self, value):
        if value:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError("Only image files (JPG, JPEG, PNG, GIF, BMP, WEBP) are allowed.")
            
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs.get('pdf') and not attrs.get('image'):
            raise ValidationError("Either 'pdf' or 'image' must be provided.")
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




# pdf serializers

class ListPDFSerializer(serializers.ModelSerializer):


    class Meta:
        model = PdfFile
        fields = [
            "title", "pdf","uploaded_at"
        ]



class RetrievePDFSerializer(serializers.Serializer):

    location = serializers.CharField()
    number_of_pages = serializers.IntegerField()
    page_width = serializers.DecimalField(max_digits=6,decimal_places=2)
    page_height = serializers.DecimalField(max_digits=6,decimal_places=2)


    def get_location(self, instance: PdfFile):
        return instance.location

    def get_number_of_pages(self, instance: PdfFile):
        return instance.number_of_pages

    def get_page_width(self, instance: PdfFile):
        return instance.page_width

    def get_page_height(self, instance: PdfFile):
        return instance.page_height


class CovertPDFSerializer(serializers.Serializer):
    pdf = serializers.PrimaryKeyRelatedField(
        queryset=PdfFile.objects.none(),
        write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get("user")
        if user:
            self.fields["pdf"].queryset = PdfFile.objects.filter(user=user)