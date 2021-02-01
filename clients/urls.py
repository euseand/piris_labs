from django.urls import path

from clients.views import get_clients_list, get_client_details, create_client, update_client, delete_client


urlpatterns = [
    path('clients/', get_clients_list, name='clients_list'),
    path('clients/create', create_client, name='clients_create'),
    path('clients/details/<int:pk>', get_client_details, name='clients_details'),
    path('clients/update/<int:pk>', update_client, name='clients_update'),
    path('clients/delete/<int:pk>', delete_client, name='clients_delete'),
]