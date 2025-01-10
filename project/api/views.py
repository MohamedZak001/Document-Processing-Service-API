from .models import ImageFile, PdfFile
from .services import ImageService, PDFService
from .serializers import  (
    ListImageSerializer, RetrieveImageSerializer, RotateImageSerializer, 
    FileUploadSerializer, ListPDFSerializer, RetrievePDFSerializer, CovertPDFSerializer
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated





# generice views 


class UploadAPIView(CreateAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        image = serializer.validated_data.get('image')
        if image:
            ImageFile.objects.create(
                image=image,
                title=image.name,
                user=self.request.user
            )
        pdf = serializer.validated_data.get('pdf')
        if pdf:
            PdfFile.objects.create(
                pdf=pdf,
                title=pdf.name,
                user=self.request.user
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


# image views 

class ListImageAPIView(ListAPIView):
    queryset = ImageFile.objects.all()
    serializer_class = ListImageSerializer  
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class RotateImageAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = RotateImageSerializer(data=data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data.get("image")
        angle = serializer.validated_data.get("angle")

        image_service = ImageService(image)
        path = image_service.rotate(angle=angle)
    
        return Response({"rotated_image_path": path}, status=status.HTTP_201_CREATED)


# pdf views

class ListPDFAPIView(ListAPIView):
    queryset = PdfFile.objects.all()
    serializer_class = ListPDFSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class RetrieveDestroyPDFAPIView(RetrieveDestroyAPIView):
    queryset = PdfFile.objects.all()
    serializer_class = RetrievePDFSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ConvertPDFAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = CovertPDFSerializer(data=data,context={"user":request.user})
        serializer.is_valid(raise_exception=True)

        pdf = serializer.validated_data.get("pdf")
        pdf_service = PDFService(pdf)
        path = pdf_service.convert()

        return Response({"converted_pdf_path": path}, status=status.HTTP_201_CREATED)
