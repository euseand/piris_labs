from django.contrib import admin

from clients.models import City, Citizenship, Disability, MaritalStatus, Client, Account, Deposit, Credit


class CityAdmin(admin.ModelAdmin):
    model = City
    list_display = ('id', 'city_name')
    list_display_links = ('id', 'city_name')
    search_fields = ('city_name',)
    ordering = ('city_name',)


class CitizenshipAdmin(admin.ModelAdmin):
    model = Citizenship
    list_display = ('id', 'country')
    list_display_links = ('id', 'country')
    search_fields = ('country',)
    ordering = ('country',)


class DisabilityAdmin(admin.ModelAdmin):
    model = Disability
    list_display = ('id', 'type')
    list_display_links = ('id', 'type')
    search_fields = ('type',)
    ordering = ('type',)


class MartialStatusAdmin(admin.ModelAdmin):
    model = MaritalStatus
    list_display = ('id', 'status')
    list_display_links = ('id', 'status')
    search_fields = ('status',)
    ordering = ('id', 'status')


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('id', 'last_name', 'first_name', 'passport_serial', 'passport_number', 'registration_place',)
    list_display_links = ('last_name', 'first_name',)
    ordering = ('last_name',)
    radio_fields = {'sex': admin.HORIZONTAL, 'pensioner': admin.HORIZONTAL}


class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ('id',)
    list_display_links = ()
    ordering = ('name',)


class DepositAdmin(admin.ModelAdmin):
    model = Deposit
    list_display = ('id',)
    list_display_links = ()
    ordering = ('client',)


class CreditAdmin(admin.ModelAdmin):
    model = Credit
    list_display = ('id',)
    list_display_links = ()
    ordering = ('client',)


admin.site.register(City, CityAdmin)
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(Disability, DisabilityAdmin)
admin.site.register(MaritalStatus, MartialStatusAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Credit, CreditAdmin)
