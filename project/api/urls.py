from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.UploadAPIView.as_view(), name="upload"),

]

# image urls
urlpatterns += [
    path('images/',views.ListImageAPIView.as_view(), name="list-images"),
    path('images/<int:id>',views.RetrieveDestroyImageAPIView.as_view(), name="retereive-delete-image"),
    path('rotate/',views.RotateImageAPIView.as_view(), name="rotate-image"),
]

# pdf urls
urlpatterns += [
    path('pdfs/',views.ListPDFAPIView.as_view(), name="list-pdfs"),
    path('pdfs/<int:id>',views.RetrieveDestroyPDFAPIView.as_view(), name="retereive-delete-pdf"),
    path('convert-pdf-to-image/',views.ConvertPDFAPIView.as_view(), name="convert-to-image"),
]