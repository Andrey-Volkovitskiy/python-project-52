from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)
from django_filters.views import FilterView
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilter
from task_manager.mixins import CustomLoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from rest_framework import viewsets, permissions
from .serializers import TaskSerializer
from .permissions import DeleteOnlyByAuthor


class TaskPermissionsForCRU(CustomLoginRequiredMixin):
    '''Implements user permissions to create/read/update tasks'''
    permission_denied_message = _("You are not authorized! Please sign in.")


class TaskPermissionsForDelete(CustomLoginRequiredMixin, UserPassesTestMixin):
    '''Implements user permissions to delete tasks'''
    permission_denied_message = _("You are not authorized! Please sign in.")

    def test_func(self):
        subject_user = self.request.user
        deleted_task = self.get_object()
        author = deleted_task.author
        if subject_user == author:
            return True
        else:
            return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.add_message(
                self.request,
                messages.ERROR,
                _("The task can only be deleted by its author.")
            )
            return redirect('task-list')
        return super().handle_no_permission()


class TaskListView(
        TaskPermissionsForCRU,
        FilterView):
    model = Task
    template_name = "tasks/list.html"
    ordering = ['id']
    filterset_class = TaskFilter


class TaskCreateView(
        TaskPermissionsForCRU,
        SuccessMessageMixin,
        CreateView):
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("task-list")
    success_message = _("Task successfully created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(
        TaskPermissionsForCRU,
        SuccessMessageMixin,
        DetailView):
    model = Task
    template_name = "tasks/detail.html"


class TaskUpdateView(
        TaskPermissionsForCRU,
        SuccessMessageMixin,
        UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("task-list")
    success_message = _("Task successfully updated")


class TaskDeleteView(
        TaskPermissionsForDelete,
        SuccessMessageMixin,
        DeleteView):
    model = Task
    fields = []
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("task-list")
    success_message = _("Task successfully deleted")


class TaskAPIViewSet(viewsets.ModelViewSet):
    '''Only authenticateed user can CRUD tasks.
    A task can only be deleted by its author.'''
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        DeleteOnlyByAuthor
    ]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)
