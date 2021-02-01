from django.shortcuts import render, redirect
from django.forms import model_to_dict

from clients.models import Client
from clients.forms import ClientForm


# CLIENTS LIST
def get_clients_list(request):
    clients_list = Client.objects.all()
    context = {
        'clients_list': clients_list,
    }
    return render(request, 'clients/clients_list.html', context)


# CLIENTS CRUD
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_client = Client(**cleaned_data)
            new_client.save()
        return redirect('clients_list')
    else:
        form = ClientForm()
        context = {
            'form': form,
        }
        return render(request, 'clients/clients_create.html', context)


def get_client_details(request, pk):
    client = Client.objects.get(pk=pk)
    client_dict = model_to_dict(client)
    context = {
        'client': client,
        'client_dict': client_dict,
    }
    return render(request, 'clients/clients_details.html', context)


def update_client(request, pk):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            client = Client(pk=pk, **cleaned_data)
            client.save(force_update=True)
        return get_client_details(request, pk)
    else:
        client = Client.objects.get(pk=pk)
        client_dict = model_to_dict(client)
        form = ClientForm(client_dict)
        context = {
            'client': client,
            'form': form,
        }
        return render(request, 'clients/clients_update.html', context)


def delete_client(request, pk):
    client_to_delete = Client.objects.get(pk=pk)
    client_to_delete.delete()
    return redirect('clients_list')
