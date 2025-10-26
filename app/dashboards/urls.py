from django.urls import path

from .views import DashboardSummaryView, DashboardView

urlpatterns = [
    path('summary', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('', DashboardView.as_view(), name='dashboard-view'),
]
