import datetime
import math

from django.db.models import F
from django.shortcuts import render, redirect
from django.forms import model_to_dict

from clients.models import Client, Account, Deposit, Credit
from clients.forms import ClientForm, DepositForm, CreditForm


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
    deposits = Deposit.objects.filter(client_id=pk)
    context = {
        'client': client,
        'deposits': deposits,
    }
    return render(request, 'clients/clients_deposits.html', context)


# WITHDRAW DEPOSIT MONEY FROM CASH
def withdraw_deposit(request, pk, account_id):
    # ACCOUNTS TO USE
    cash = Account.objects.get(name='CASH')
    account = Account.objects.get(pk=account_id)
    amount = account.balance

    # MAIN/PERCENTS -> CASH -> CASH TO CLIENT
    change_account_debit(account, amount)
    change_account_debit(cash, amount)
    change_account_credit(cash, amount)

    return get_deposits_list(request, pk)


# CREDITS LIST
def get_credits_list(request, pk):
    client = Client.objects.get(pk=pk)
    bank_credits = Credit.objects.filter(client_id=pk)
    context = {
        'client': client,
        'credits': bank_credits,
    }
    return render(request, 'clients/clients_credits.html', context)


# DEPOSIT CREDIT MONEY TO CASH
def deposit_credit(request, pk, account_id, credit_id):
    # ACCOUNTS TO USE
    credit = Credit.objects.get(pk=credit_id)
    cash = Account.objects.get(name='CASH')
    account = Account.objects.get(pk=account_id)
    amount = account.balance

    # CLIENT TO CASH -> CASH -> MAIN/PERCENT

    change_account_debit(cash, amount)
    change_account_credit(cash, amount)
    change_account_debit(account, amount)
    credit.amount_paid = math.ceil(credit.amount_paid) + amount
    credit.amount_left = math.ceil(credit.amount_left)
    credit.save()

    return get_credits_list(request, pk)


# ACCOUNTS LIST
def get_accounts_list(request, pk):
    client = Client.objects.get(pk=pk)
    deposits = Deposit.objects.filter(client=pk)
    bank_credits = Credit.objects.filter(client=pk)
    accounts = []
    accounts.append(Account.objects.get(name='BDFA'))
    accounts.append(Account.objects.get(name='CASH'))
    for deposit in deposits:
        accounts.append(Account.objects.get(pk=deposit.main_account.id))
        accounts.append(Account.objects.get(pk=deposit.percent_account.id))
    for credit in bank_credits:
        accounts.append(Account.objects.get(pk=credit.main_account.id))
        accounts.append(Account.objects.get(pk=credit.percent_account.id))
    context = {
        'client': client,
        'accounts': accounts,
    }
    return render(request, 'clients/clients_accounts.html', context)


# OPEN NEW DEPOSIT
def create_deposit(request, pk):
    client = Client.objects.get(pk=pk)
    account = Account.objects.get(name='BDFA')
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_deposit = Deposit.objects.create(revocable=True, number='0', start_date='2021-01-01',
                                                 end_date='2021-01-01', currency='USD', amount='0', percents='0',
                                                 client=client, main_account=account, percent_account=account,
                                                 days_left=0, days_passed=0, pay_monthly=True)
            new_deposit.save()

            new_deposit = Deposit.objects.get(number='0')
            deposit_id = new_deposit.pk
            new_deposit.revocable = cleaned_data['revocable']
            new_deposit.number = cleaned_data['number']
            new_deposit.start_date = cleaned_data['start_date']
            new_deposit.end_date = cleaned_data['end_date']
            new_deposit.currency = cleaned_data['currency']
            new_deposit.amount = cleaned_data['amount']
            new_deposit.percents = cleaned_data['percents']
            new_deposit.client = client

            main_account = create_account(client=client, main=True, code='1523', activity='Passive',
                                          currency=cleaned_data['currency'], credit_deposit_id=deposit_id)
            percent_account = create_account(client=client, main=False, code='1572', activity='Passive',
                                             currency=cleaned_data['currency'], credit_deposit_id=deposit_id)

            new_deposit.main_account = main_account
            new_deposit.percent_account = percent_account
            delta = new_deposit.end_date - new_deposit.start_date
            new_deposit.days_left = delta.days
            new_deposit.days_passed = 0
            pay_monthly = cleaned_data['revocable']
            new_deposit.pay_monthly = pay_monthly
            new_deposit.save()

            # ACCOUNTS TO USE
            cash = Account.objects.get(name='CASH')
            bank = Account.objects.get(name='BDFA')
            main = Account.objects.get(pk=new_deposit.main_account_id)

            # DEPOSIT CASH -> CASH -> MAIN ACCOUNT -> BANK ACCOUNT
            change_account_debit(cash, new_deposit.amount)
            change_account_credit(cash, new_deposit.amount)
            change_account_credit(main, new_deposit.amount)
            change_account_debit(main, new_deposit.amount)
            change_account_credit(bank, new_deposit.amount)

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


# OPEN NEW CREDIT
def create_credit(request, pk):
    client = Client.objects.get(pk=pk)
    account = Account.objects.get(name='BDFA')
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_credit = Credit.objects.create(
                annuity=True, number='0', start_date='2021-01-01', end_date='2021-01-01', currency='USD', amount='0',
                percents='0', client=client, main_account=account, percent_account=account, days_left=0, days_passed=0,
                amount_left=0, amount_paid=0, pay_period=0
            )
            new_credit.save()

            new_credit = Credit.objects.get(number='0')
            credit_id = new_credit.pk
            new_credit.annuity = cleaned_data['annuity']
            new_credit.number = cleaned_data['number']
            new_credit.start_date = cleaned_data['start_date']
            new_credit.end_date = cleaned_data['end_date']
            new_credit.currency = cleaned_data['currency']
            new_credit.amount = cleaned_data['amount']
            new_credit.percents = cleaned_data['percents']
            new_credit.client = client
            main_account = create_account(
                client=client, main=True, code='1523', activity='Active', currency=cleaned_data['currency'],
                credit_deposit_id=credit_id
            )
            percent_account = create_account(
                client=client, main=False, code='1572', activity='Active', currency=cleaned_data['currency'],
                credit_deposit_id=credit_id)
            new_credit.main_account = main_account
            new_credit.percent_account = percent_account
            delta = new_credit.end_date - new_credit.start_date
            new_credit.days_left = delta.days
            new_credit.days_passed = 0
            new_credit.amount_left = new_credit.amount + new_credit.amount * new_credit.percents / 100
            new_credit.amount_paid = 0
            new_credit.pay_period = math.floor(delta.days/math.ceil(delta.days / 30))
            new_credit.save()

            # ACCOUNTS TO USE
            cash = Account.objects.get(name='CASH')
            bank = Account.objects.get(name='BDFA')
            main = Account.objects.get(pk=new_credit.main_account_id)

            # BANK -> MAIN -> CASH -> CASH CLIENT
            change_account_debit(bank, new_credit.amount)
            change_account_debit(main, new_credit.amount)
            change_account_debit(cash, new_credit.amount)
            change_account_credit(main, new_credit.amount)
            change_account_credit(cash, new_credit.amount)

            return redirect('clients_credits', pk=pk)
        else:
            context = {
                'client_pk': pk,
                'form': form,
            }
            return render(request, 'clients/clients_credits_create.html', context)
    else:
        form = CreditForm(initial={
            'last_name': client.last_name,
            'first_name': client.first_name,
            'passport': str(client.passport_serial) + str(client.passport_number),
            'start_date': datetime.date.today()
        })
        context = {
            'client_pk': pk,
            'form': form,
        }
        return render(request, 'clients/clients_credits_create.html', context)


# CREATE NEW ACCOUNT
def create_account(client, main, code, activity, currency, credit_deposit_id):
    client_id = getattr(client, 'id')
    account_id = str(credit_deposit_id).zfill(3) + '1' if main else str(credit_deposit_id).zfill(3) + '2'
    number = '3014' + str(client_id).zfill(4) + account_id + str(7)
    main_str = 'Main' if main else 'Percent'
    name = str(account_id) + '/' + main_str + '/' + getattr(client, 'last_name') + getattr(client, 'first_name') \
           + '/' + currency
    credit = 0
    debit = 0
    balance = 0
    account = Account(number=number, main=main, name=name, code=code, activity=activity, debit=debit, credit=credit,
                      balance=balance)
    account.save()
    return account


# ACCOUNT DEBIT CHANGES
def change_account_debit(account, amount):
    if account.activity == 'Active':
        account.debit = account.debit + amount
        account.balance = abs(account.debit - account.credit)
    else:
        account.debit = account.debit - amount
        account.balance = abs(account.credit - account.debit)
    account.save()


# ACCOUNT CREDIT CHANGES
def change_account_credit(account, amount):
    if account.activity == 'Passive':
        account.credit = account.credit - amount
        account.balance = abs(account.debit - account.credit)
    else:
        account.credit = account.credit + amount
        account.balance = abs(account.credit - account.debit)
    account.save()


def is_deposit_closed():
    deposits = Deposit.objects.filter(active=True)
    for deposit in deposits:
        if deposit.days_left <= 0:

            # CLOSE DEPOSIT
            # ACCOUNTS TO USE
            bank = Account.objects.get(name='BDFA')
            main = Account.objects.get(pk=deposit.main_account_id)

            # BANK -> MAIN
            change_account_debit(bank, deposit.amount)
            change_account_credit(main, deposit.amount)

            if deposit.revocable:

                bank = Account.objects.get(name='BDFA')
                percents = Account.objects.get(pk=deposit.percent_account_id)

                amount = deposit.amount * deposit.percents / 100

                change_account_debit(bank, amount)
                change_account_credit(percents, amount)

            deposit.days_left = 0
            deposit.active = False
            deposit.save()


def is_credit_closed():
    bank_credits = Credit.objects.filter(active=True)
    for credit in bank_credits:
        percents_amount = credit.amount + credit.amount * credit.percents / 100
        if credit.amount_paid >= credit.amount_left or credit.days_left <= 0:

            # CLOSE CREDIT
            # ACCOUNTS TO USE
            bank = Account.objects.get(name='BDFA')
            main = Account.objects.get(pk=credit.main_account_id)
            if not credit.annuity:
                # MAIN -> BANK
                change_account_credit(main, credit.amount)
                change_account_credit(bank, credit.amount)

            '''if credit.annuity:

                bank = Account.objects.get(name='BDFA')
                percents = Account.objects.get(pk=credit.percent_account_id)
                main = Account.objects.get(pk=credit.main_account_id)

                delta = credit.end_date - credit.start_date
                amount = ((credit.amount * credit.percents)/100)/math.ceil(delta.days/30)
                #amount = ((float(credit.amount) * float(credit.percents)) / 100) / (delta.days / 30)

                change_account_credit(percents, amount)
                change_account_credit(bank, amount)

                #amount = credit.amount/math.ceil(delta.days/30)
                #amount = float(credit.amount)/(delta.days / 30)

                # MAIN ACCOUNT -> BANK ACCOUNT
                #change_account_credit(main, amount)
                #change_account_credit(bank, amount)'''

            credit.days_left = 0
            credit.active = False
            credit.save()


def close_period(request, pk, period, page):
    if period == 'day':
        Deposit.objects.filter(active=True).update(days_left=F('days_left') - 1)
        Deposit.objects.filter(active=True).update(days_passed=F('days_passed') + 1)
        Credit.objects.filter(active=True).update(days_left=F('days_left') - 1)
        Credit.objects.filter(active=True).update(days_passed=F('days_passed') + 1)
    else:
        Deposit.objects.filter(active=True).update(days_left=F("days_left") - 30)
        Deposit.objects.filter(active=True).update(days_passed=F('days_passed') + 30)
        Credit.objects.filter(active=True).update(days_left=F('days_left') - 30)
        Credit.objects.filter(active=True).update(days_passed=F('days_passed') + 30)

    pay_irrevocable_deposits_percents()
    get_credits_percents()

    is_deposit_closed()
    is_credit_closed()

    if page == 'deposits':
        deposits = Deposit.objects.filter(client__id=pk)

        client = Client.objects.get(pk=pk)
        context = {
            'client': client,
            'deposits': deposits,
        }
        return render(request, 'clients/clients_deposits.html', context)
    else:
        bank_credits = Credit.objects.filter(client__id=pk)

        client = Client.objects.get(pk=pk)
        context = {
            'client': client,
            'credits': bank_credits,
        }
        return render(request, 'clients/clients_credits.html', context)


def pay_irrevocable_deposits_percents():
    deposits = Deposit.objects.filter(active=True, revocable=False)
    for deposit in deposits:
        if deposit.days_passed >= 30:
            # ACCOUNTS TO USE
            bank = Account.objects.get(name='BDFA')
            percents = Account.objects.get(pk=deposit.percent_account_id)

            amount = deposit.amount * deposit.percents / 100

            # BANK ACCOUNT -> PERCENTS ACCOUNT
            change_account_debit(bank, amount)
            change_account_credit(percents, amount)

            deposit.days_passed = 0
            deposit.save()


def get_credits_percents():
    bank_credits = Credit.objects.filter(active=True)
    for credit in bank_credits:
        if credit.annuity:
            pay_period = credit.pay_period
        else:
            pay_period = 30
        if credit.days_passed >= pay_period:
            # ACCOUNTS TO USE
            bank = Account.objects.get(name='BDFA')
            percents = Account.objects.get(pk=credit.percent_account_id)
            main = Account.objects.get(pk=credit.main_account_id)

            delta = credit.end_date - credit.start_date
            amount = ((credit.amount * credit.percents)/100)/math.ceil(delta.days/30)
            #amount = ((float(credit.amount) * float(credit.percents))/100)/(delta.days/30)

            # PERCENTS ACCOUNT -> BANK ACCOUNT
            change_account_credit(percents, amount)
            change_account_credit(bank, amount)
            if credit.annuity:

                amount = credit.amount/math.ceil(delta.days/30)
                #amount = float(credit.amount) / (delta.days / 30)
                # MAIN ACCOUNT -> BANK ACCOUNT
                change_account_credit(main, amount)
                change_account_credit(bank, amount)

            credit.days_passed = 0
            credit.save()
