from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView, View, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import History
from django.db.models import Sum

from .forms import CreateUserForm
import requests

def logout_view(request):
    logout(request)
    return redirect('login') 

def getBalance(user):
   deposits = History.objects.filter(user = user, 
                                     type = 'deposit').aggregate(total_amount = Sum('amount'))['total_amount'] or 0
   withdrawals = History.objects.filter(user = user, 
                                        type = 'debit').aggregate(total_amount = Sum('amount'))['total_amount'] or 0
   balance = deposits - withdrawals
   return float(balance) 
'''
    Write a function that finds the user's balance and returns it with the float data type. 
    To calculate the balance, calculate the sum of all user's deposits and the sum of all withdrawals.
    Then subtract the withdrawal amount from the deposit amount and return the result.
    '''

def getCurrencyParams():
    url = "https://fake-api.apps.berlintech.ai/api/currency_exchange"
    response = requests.get(url)

    if response.status_code ==200:
        data = response.json() # (dictionary of currency rates)
        currency_choices = [(currency, f"{currency} ({rate})") for currency, rate in data.items()] # (list of formatted strings)
        return [data, currency_choices] # returns list 'cas of [], else default is tuples
    else:
        return[None, None]
    '''
    Write a function that makes a GET request to the following address 
    https://fake-api.apps.berlintech.ai/api/currency_exchange

    if the response code is 200 return a list of two values:
    - a dictionary of data that came from the server
    - a list of strings based on the received data 
    mask to form the string f'{currency} ({rate})'.
    example string: 'USD (1.15)'

    if the server response code is not 200 you should 
    return the list [None, None]
    '''

class CreateUserView(CreateView):
    model = User 
    form_class = CreateUserForm
    template_name = 'app/create_account.html'
    success_url = reverse_lazy('login')
    '''
    Finalize this class. It should create a new user.
    The model should be the User model
    The CreateUserForm model should be used as a form.
    The file create_account.html should be used as a template.
    If the account is successfully created, it should redirect to the page with the name login
    '''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        return context
        '''
        If the user is authenticated, then add the 'username' key with the value of username to the context.
        '''

class CustomLoginView(LoginView):
    template_name= 'app/login.html'
    success_url = reverse_lazy('main_menu')

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        '''
        If the user is authenticated, then add the 'username' key with the value of username to the context.
        '''
        return context

class MainMenuView(LoginRequiredMixin, TemplateView):
    template_name = 'app/main_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
        '''
        If the user is authenticated, then add the 'username' key with the value of username to the context.
        '''
        return context
    
    #EXCEPTION HANDLING
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Log the exception
            print(f"Exception occurred: {e}")
            # Render a custom error template
            return render(request, 'app/error.html', {'message': 'An error occurred. Please try again later.'}, status=500)



class BalanceOperationsView(LoginRequiredMixin, View):
    template_name = 'app/operations.html'
    
    def get(self, request):
        pass # this line can be deleted 
        '''
        This method should return the page given in template_name with a context.

        Context is a dictionary with balance and username keys.
        The balance key contains the result of the getBalance function
        username contains the username of the user.
        '''

    def post(self, request):
        pass # this line can be deleted 
        '''
        This method should process a balance transaction.
        For this purpose it is necessary to add an entry to the History model. 
        
        status - if the amount on the account is not enough when attempting to withdraw funds, the status is failure, otherwise withdraw
        amount - amount of operation, obtained from the form
        type - type of operation (withdraw/deposit), the value is obtained from the form.
        user - object of the current user

        This method should return the page given in template_name with a context.

        Context is a dictionary with balance and username keys.
        The balance key contains the result of the getBalance function (after account update)
        username contains the username of the user.
        '''

class ViewTransactionHistoryView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'app/history.html'
    context_object_name = 'transactions'
    ordering = ['-datetime']

    def get_queryset(self):
        # Filter the transaction history by the current logged-in user
        return History.objects.filter(user = self.request.user)
        '''
        This method should return the entire transaction history of the current user
        '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['username'] = self.request.user.username
        '''
        Add the 'username' key with the value of username to the context.
        '''
        return context

class CurrencyExchangeView(LoginRequiredMixin, View):
    template_name = 'app/currency_exchange.html'
    empty_context = {'currency_choices': [], 'amount': None, 'currency': None, 'exchanged_amount': None}

    def get(self, request):
        # Fetch currency_choices from utility function # _, ** is used to unpack tuples/ 
        _, currency_choices = getCurrencyParams() 
        
        context = {
            **self.empty_context, # Include all values from empty_context
            "currency_choices": currency_choices, # Add currency_choices from getCurrencyParam function
            "username": self.request.user.username # Add current username
        }
        return render(request, self.template_name, context)

        '''
        Generate a context variable with all values from empty_context and the converted values of currency_choices and username
        currency_choices contains the value of the currency_choices variable
        username contains the name of the current user
        '''

    def post(self, request):
        data, currency_choices = getCurrencyParams()

        # Step 1: Retrieve form data
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')

        # Step 2: Process and validate form data
        if amount:
            try: 
                amount = float(amount)
            except ValueError:
                amount = None

        # Step 3: Handle invalid data
        if data is None or amount is None:
            context = self.empty_context
            context['currency_choices'] = currency_choices
            context['username'] = self.request.user.username
            return render(request, self.template_name, context)
        
        # Step 4: Calculate exchange rate
        exchange_rate = data.get(currency)
        # Step 5: Calculate exchanged amount
        exchanged_amount = round(amount * exchange_rate, 2)

        # Step 6: Prepare context (uses empty_context as base) and render template
        context = {'currency_choices': currency_choices,
                   'amount': amount,
                   'currency': currency,
                   'exchanged_amount': exchanged_amount,
                   'username' : self.request.user.username
                   }
        return render(request, self.template_name, context)

        '''
            Improve this method:
            1) add the process of forming the variable amount.
            If the amount value from the form is converted to float type, then write the amount value from the form converted to float to the amount variable. Otherwise, write None.
            2) add a currency variable that contains the currency value from the form.
            3) if the variables data or amount contain None, return page with empty context (empty_context). Otherwise, perform the following steps
            4) generate the exchange_rate variable by calculating the corresponding value from the data variable
            5) generate the exchanged_amount variable, which contains the converted currency to two decimal places.
            6) form a context from the previously created variables and return a template with it.
        '''
