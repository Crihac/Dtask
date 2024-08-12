from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import tasks

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class registeruser(FormView):
    template_name='daily/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')

    def form_valid(self, form: Any) -> HttpResponse:
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(registeruser,self).form_valid(form)
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
           return redirect('tasks')
        return super(registeruser,self).get(request, *args, **kwargs)


class listlogin(LoginView):
    template_name='daily/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self) -> str:
        return reverse_lazy('tasks')


class listview(LoginRequiredMixin,ListView):
    model=tasks
    context_object_name='task'


    def get_context_data(self, **kwargs: Any):
       context=  super().get_context_data(**kwargs)
       context['task']=context['task'].filter(user=self.request.user)
       context['count']=context['task'].filter(complete=False).count()

       search_input=self.request.GET.get('search-area') or ''
       if search_input:
           context['task']=context['task'].filter(title__icontains=search_input)

       context['search_input']=search_input    

       return context

class taskdetail(LoginRequiredMixin,DetailView):
    model=tasks
    context_object_name='task'


class taskcreate(LoginRequiredMixin,CreateView):
    model=tasks
    fields=['title','description','complete']
    context_object_name='task'
    success_url=reverse_lazy('tasks')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user=self.request.user
        return super(taskcreate,self).form_valid(form)


class taskupdate(LoginRequiredMixin,UpdateView):
    model=tasks
    fields=['title','description','complete']
    context_object_name='task'
    success_url=reverse_lazy('tasks')


class taskdelete(LoginRequiredMixin,DeleteView):
    model=tasks
    context_object_name='task'
    success_url=reverse_lazy('tasks')
