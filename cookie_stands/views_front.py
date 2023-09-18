from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import CookieStand


class CookieStandListView(LoginRequiredMixin, ListView):
    template_name = "cookie_stands/thing_list.html"
    model = CookieStand
    context_object_name = "cookie_stands"


class ThingDetailView(LoginRequiredMixin, DetailView):
    template_name = "cookie_stands/thing_detail.html"
    model = CookieStand


class ThingUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cookie_stands/thing_update.html"
    model = CookieStand
    fields = "__all__"


class ThingCreateView(LoginRequiredMixin, CreateView):
    template_name = "cookie_stands/thing_create.html"
    model = CookieStand
    fields = ["name", "rating", "reviewer"] # "__all__" for all of them


class ThingDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "cookie_stands/thing_delete.html"
    model = CookieStand
    success_url = reverse_lazy("thing_list")
