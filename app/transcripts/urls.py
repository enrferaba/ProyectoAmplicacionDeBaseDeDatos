from django.urls import path

from .views import TranscriptionDetailView, TranscriptionListCreateView

urlpatterns = [
    path('', TranscriptionListCreateView.as_view(), name='transcription-list'),
    path('<str:pk>', TranscriptionDetailView.as_view(), name='transcription-detail'),
]
