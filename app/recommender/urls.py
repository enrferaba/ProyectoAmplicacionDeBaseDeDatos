from django.urls import path

from .views import (
    CollaborativeRecommendationView,
    ContentRecommendationView,
    HybridRecommendationView,
    ListenEventView,
    SimilarUsersView,
    CommunityDetectionView,
)

urlpatterns = [
    path('listen', ListenEventView.as_view(), name='reco-listen'),
    path('content/<str:user_id>', ContentRecommendationView.as_view(), name='reco-content'),
    path('collab/<str:user_id>', CollaborativeRecommendationView.as_view(), name='reco-collab'),
    path('hybrid/<str:user_id>', HybridRecommendationView.as_view(), name='reco-hybrid'),
    path('similar/<str:user_id>', SimilarUsersView.as_view(), name='reco-similar'),
    path('communities', CommunityDetectionView.as_view(), name='reco-communities'),
]
