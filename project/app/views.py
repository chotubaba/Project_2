from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView, TemplateView, View, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import History
from .forms import CreateUserForm
import requests

def logout_view(request):
    logout(request)
    return redirect('login') 

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