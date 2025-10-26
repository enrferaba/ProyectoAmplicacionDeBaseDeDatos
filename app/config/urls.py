from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from core.views import CachePingView
from realtime.views import RealtimeCounterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('auth/', include('users.urls')),
    path('cache/ping', CachePingView.as_view(), name='cache-ping'),
    path('realtime/counter', RealtimeCounterView.as_view(), name='realtime-counter'),
    path('transcriptions/', include('transcripts.urls')),
    path('reco/', include('recommender.urls')),
    path('dash/', include('dashboards.urls')),
]
