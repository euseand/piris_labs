import datetime

from django.db.models import F
from django.shortcuts import render, redirect
from django.forms import model_to_dict

from clients.models import Client, Deposit, Account
from clients.forms import ClientForm, DepositForm


# CLIENTS LIST
def get_clients_list(request):
    clients_list = Client.objects.all().order_by('last_name')
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
            context = {
                'form': form,
            }
            return render(request, 'clients/clients_create.html', context)
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
    client = Client.objects.get(pk=pk)
    client_dict = model_to_dict(client)
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            client = Client(pk=pk, **cleaned_data)
            client.save(force_update=True)
            return get_client_details(request, pk)
        else:
            context = {
                'client': client,
                'form': form,
            }
            return render(request, 'clients/clients_update.html', context)
    else:
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


# DEPOSITS LIST
def get_deposits_list(request, pk):
    client = Client.objects.get(pk=pk)
    deposits = Deposit.objects.filter(client=pk)
    context = {
        'client': client,
        'deposits': deposits,
    }
    return render(request, 'clients/clients_deposits.html', context)


# ACCOUNTS LIST
def get_accounts_list(request, pk):
    client = Client.objects.get(pk=pk)
    deposits = Deposit.objects.filter(client=pk)
    accounts = []
    for deposit in deposits:
        accounts.append(Account.objects.get(pk=deposit.main_account.id))
        accounts.append(Account.objects.get(pk=deposit.percent_account.id))
    context = {
        'client': client,
        'accounts': accounts,
    }
    return render(request, 'clients/clients_accounts.html', context)


# OPEN NEW DEPOSIT
def create_deposit(request, pk):
    client = Client.objects.get(pk=pk)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            deposit_id = Deposit.objects.filter(client=pk).count() + 1
            new_deposit = Deposit()
            new_deposit.revocable = cleaned_data['revocable']
            new_deposit.number = cleaned_data['number']
            new_deposit.start_date = cleaned_data['start_date']
            new_deposit.end_date = cleaned_data['end_date']
            new_deposit.currency = cleaned_data['currency']
            new_deposit.amount = cleaned_data['amount']
            new_deposit.percents = cleaned_data['percents']
            new_deposit.client = client
            main_account = create_account(client=client, debit=cleaned_data['amount'], main=True, code='1523',
                                          activity='Passive', currency=cleaned_data['currency'], deposit_id=deposit_id)
            percent_account = create_account(client=client, debit=0, main=False, code='1572', activity='Passive',
                                             currency=cleaned_data['currency'], deposit_id=deposit_id)
            new_deposit.main_account = main_account
            new_deposit.percent_account = percent_account
            delta = new_deposit.end_date - new_deposit.start_date
            new_deposit.days_left = delta.days
            pay_monthly = True if cleaned_data['revocable'] else False
            new_deposit.pay_monthly = pay_monthly
            new_deposit.save()

            bank = Account.objects.get(pk=13)
            bank.debit = bank.debit + new_deposit.amount
            bank.balance = abs(bank.debit - bank.credit)
            bank.save()

            main = Account.objects.get(pk=new_deposit.main_account_id)
            main.credit = main.credit + new_deposit.amount
            main.balance = abs(main.debit - main.credit)
            main.save()

            return redirect('clients_deposits', pk=pk)
        else:
            context = {
                'client_pk': pk,
                'form': form,
            }
            return render(request, 'clients/clients_deposits_create.html', context)
    else:
        form = DepositForm(initial={
            'last_name': client.last_name,
            'first_name': client.first_name,
            'passport': str(client.passport_serial) + str(client.passport_number),
            'start_date': datetime.date.today()
        })
        context = {
            'client_pk': pk,
            'form': form,
        }
        return render(request, 'clients/clients_deposits_create.html', context)


def create_account(client, debit, main, code, activity, currency, deposit_id):
    client_id = getattr(client, 'id')
    account_id = str(deposit_id).zfill(2) + '1' if main else str(deposit_id).zfill(2) + '2'
    number = '3014' + str(client_id).zfill(5) + account_id + str(7)
    main_str = 'Main' if main else 'Percent'
    name = str(account_id) + '/' + main_str + '/' + getattr(client, 'last_name') + getattr(client, 'first_name') \
           + '/' + currency
    credit = 0
    balance = abs(debit - credit)
    account = Account(number=number, main=main, name=name, code=code, activity=activity, debit=debit, credit=credit,
                      balance=balance)
    account.save()
    return account


def is_deposit_ended():
    deposits = Deposit.objects.filter(active=True)
    for deposit in deposits:
        if deposit.days_left <= 0:

            bank = Account.objects.get(pk=13)
            bank.credit = bank.credit + deposit.amount
            bank.balance = abs(bank.debit - bank.credit)
            bank.save()

            main = Account.objects.get(pk=deposit.main_account_id)
            main.debit = main.debit + deposit.amount
            main.balance = abs(main.debit - main.credit)
            main.save()

            if not deposit.pay_monthly:
                perc = Account.objects.get(pk=deposit.percent_account_id)
                perc.debit = perc.debit + deposit.amount * deposit.percents / 100
                perc.balance = abs(perc.debit - perc.credit)
                perc.save()

            deposit.days_left = 0
            deposit.active = False
            deposit.save()


def close_day(request, pk):
    Deposit.objects.filter(active=True).update(days_left=F('days_left') - 1)

    is_deposit_ended()

    deposits = Deposit.objects.all()
    client = Client.objects.get(pk=pk)
    context = {
        'client': client,
        'deposits': deposits,
    }
    return render(request, 'clients/clients_deposits.html', context)


def close_month(request, pk):
    Deposit.objects.filter(active=True).update(days_left=F("days_left") - 30)

    deposits = Deposit.objects.filter(active=True, pay_monthly=True)
    for deposit in deposits:
        perc = Account.objects.get(pk=deposit.percent_account_id)
        perc.debit = perc.debit + deposit.amount * deposit.percents / 100
        perc.balance = abs(perc.debit - perc.credit)
        perc.save()
        deposit.save()

    is_deposit_ended()

    deposits = Deposit.objects.all()
    client = Client.objects.get(pk=pk)
    context = {
        'client': client,
        'deposits': deposits,
    }
    return render(request, 'clients/clients_deposits.html', context)
