# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from .. import forms,models
from timeline.models import History
from ..permission import group as GroupPermission
from django.urls import reverse_lazy
from django.views.generic import FormView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required
from timeline.decorator.manager import decorator_manager

class ManagerGroupListView(LoginRequiredMixin,TemplateView):
    template_name= 'manager/group.html'

    def get(self,request,*args, **kwargs):
        return super(ManagerGroupListView, self).get(request, *args, **kwargs)

class ManagerGroupCreateView(LoginRequiredMixin,GroupPermission.GroupAddRequiredMixin,CreateView):
    model = models.Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'manager/new_update_group.html'
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(ManagerGroupCreateView, self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        context.update({'hosts':hosts})
        return context

    @decorator_manager(0,u'新增应用组')
    def form_valid(self, form):
        form.before_save(request=self.request,commit=True)
        return self.request.user,super(ManagerGroupCreateView,self).form_valid(form)

    def get_success_url(self):
         return self.success_url

class ManagerGroupUpdateView(LoginRequiredMixin,GroupPermission.GroupChangeRequiredMixin,UpdateView):
    model = models.Group
    form_class = forms.GroupCreateUpdateForm
    template_name = 'manager/new_update_group.html'
    success_url = reverse_lazy('manager:group')

    def get_context_data(self, **kwargs):
        context = super(ManagerGroupUpdateView, self).get_context_data(**kwargs)
        hosts = models.Host.objects.all()
        group_hosts = [host.id for host in self.object.hosts.all()]
        context.update({
            'hosts':hosts,
            'group_hosts':group_hosts
        })
        return context

    @decorator_manager(0,u'修改应用组')
    def form_valid(self, form):
        form.before_save(request=self.request,commit=True)
        return self.request.user,super(ManagerGroupUpdateView,self).form_valid(form)

    def get_success_url(self):
        return self.success_url

class ManagerGroupDetailView(LoginRequiredMixin,DetailView):
    model = models.Group
    template_name = 'manager/detail_group.html'

    def get_context_data(self, **kwargs):
        context=super(ManagerGroupDetailView,self).get_context_data(**kwargs)
        group=self.object
        hosts=self.object.hosts.all()
        context.update({
            'group':group,
            'hosts':hosts,
        })
        return context