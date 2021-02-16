from django.urls import path

from clients.views import *


urlpatterns = [
    path('clients/', get_clients_list, name='clients_list'),
    path('clients/create', create_client, name='clients_create'),
    path('clients/details/<int:pk>', get_client_details, name='clients_details'),
    path('clients/update/<int:pk>', update_client, name='clients_update'),
    path('clients/delete/<int:pk>', delete_client, name='clients_delete'),
    path('clients/details/<int:pk>/accounts/', get_accounts_list, name='clients_accounts'),
    path('clients/details/<int:pk>/deposites/', get_deposits_list, name='clients_deposits'),
    path('clients/details/<int:pk>/deposites/create', create_deposit, name='clients_deposits_create'),
    path('clients/details/<int:pk>/credits/', get_credits_list, name='clients_credits'),
    path('clients/details/<int:pk>/credits/create', create_credit, name='clients_credits_create'),
    path('clients/details/<int:pk>/close_day', close_day, name='clients_close_day'),
    path('clients/details/<int:pk>/close_month', close_month, name='clients_close_month'),
]
