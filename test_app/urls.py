from django.urls import path
from .views import *


urlpatterns = [
    path('accounts/', AccountDetailView.as_view()),
    path('accounts/<int:pk>/',AccountDetailView.as_view()),
    path('destinations/', DestinationAPIView.as_view()),
    path('destinations/<int:pk>/', DestinationAPIView.as_view()),
    path('list_destinations/<int:account_id>/', DestinationListByAccount.as_view(), name='destination-list-by-account'),
    path('server/incoming_data/', IncomingData.as_view(), name='incoming-data'),
]