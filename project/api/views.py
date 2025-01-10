from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import ListImageSerializer, RetrieveImageSerializer, RotateImageSerializer, FileUploadSerializer
from .models import ImageFile
from .services import ImageService




# generice views 


class UploadAPIView(CreateAPIView):
    serializer_class = FileUploadSerializer


    def perform_create(self, serializer):
        image = serializer.validated_data.get('image')
        if image:
            ImageFile.objects.create(
                image=image,
                title=image.name,
                user=self.request.user
            )


# image views 

class ListImageAPIView(ListAPIView):
    queryset = ImageFile.objects.all()
    serializer_class = ListImageSerializer  

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class RetrieveDestroyImageAPIView(RetrieveDestroyAPIView):
    queryset = ImageFile.objects.all()
    serializer_class = RetrieveImageSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class RotateImageAPIView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RotateImageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        _id = serializer.validated_data.get("image")
        image = ImageFile.objects.get(id=_id)
        image_service = ImageService(image)
        angel = float(serializer.validated_data.get("angle"))
        path = image_service.rotate(angle=angel)
        return Response({"rotated_image_path": path}, status=status.HTTP_201_CREATED)


