from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from task_manager.users.forms import UserForm
from task_manager.tasks.models import Task
from task_manager.mixins import CustomLoginRequiredMixin
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from .permissions import IsHimselfOrReadOnly


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully created")


class UserPermissions(CustomLoginRequiredMixin, UserPassesTestMixin):
    '''Implements user permissions to upd / del another users'''
    permission_denied_message = _("You are not authorized! Please sign in.")

    def test_func(self):
        subject_user = self.request.user
        object_user = self.get_object()
        if subject_user == object_user:
            return True
        else:
            return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.add_message(
                self.request,
                messages.ERROR,
                _("You do not have rights to change another user.")
            )
            return redirect('user-list')
        return super().handle_no_permission()


class UserUpdateView(
        UserPermissions,
        SuccessMessageMixin,
        UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("user-list")
    success_message = _("User successfully updated")


class UserDeleteView(
        UserPermissions,
        SuccessMessageMixin,
        DeleteView):
    model = User
    fields = []
    template_name = "users/delete.html"
    success_url = reverse_lazy("user-list")
    success_message = _("User successfully deleted")

    def form_valid(self, form):
        user = self.get_object()
        is_author_or_executor = Task.objects.filter(
            Q(author=user) | Q(executor=user)).exists()
        if is_author_or_executor:
            messages.add_message(
                self.request,
                messages.ERROR,
                _("The user cannot be deleted because it is in use"))
            return redirect('user-list')
        return super().form_valid(form)


class UserAPIViewSet(viewsets.ModelViewSet):
    '''An anonymous user can create, retrieve and list users.
    Only the user himself can change or delete his account.
    A user associated with a task cannot be deleted.'''
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsHimselfOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_author = instance.author_set.exists()
        is_executor = instance.executor_set.exists()
        if is_author or is_executor:
            message = _("The user cannot be deleted because it is in use")
            return Response({'detail': message}, status=405)
        return super().destroy(request, *args, **kwargs)
