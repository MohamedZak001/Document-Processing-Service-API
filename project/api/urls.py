from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.UploadAPIView.as_view(), name="upload"),
    path('images/',views.ListImageAPIView.as_view(), name="list-images"),
    path('images/<int:id>',views.RetrieveDestroyImageAPIView.as_view(), name="get-image"),
    path('rotate/',views.RotateImageAPIView.as_view(), name="rotate-image"),
]
