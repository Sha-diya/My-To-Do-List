from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django import forms
import json
from django.contrib.auth import login
from .forms import RegistrationForm

# --------------------- Auth Views ------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('task_list')  # Replace 'home' with your homepage or dashboard view
    else:
        form = RegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

# --------------------- Task Views ------------------------

@login_required
def task_list(request, filter_type=None):
    tasks = Task.objects.filter(user=request.user)

    if filter_type == 'today':
        tasks = tasks.filter(due_date=date.today(), completed=False)
    elif filter_type == 'pending':
        tasks = tasks.filter(completed=False, due_date__isnull=False, due_date__gt=date.today())
    elif filter_type == 'overdue':
        tasks = tasks.filter(completed=False, due_date__lt=date.today())

    return render(request, 'task_list.html', {'tasks': tasks, 'current_filter': filter_type})



@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due_date")
        Task.objects.create(user=request.user, title=title, due_date=due_date)
    return redirect('task_list')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('task_list')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        task.due_date = due_date if due_date else None
        task.save()
        return redirect('task_list')
    
    return render(request, 'update_task.html', {'task': task})


@csrf_exempt  # Use CSRF token properly in production
@require_POST
@login_required
def update_task_completion(request):
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        completed = data.get('completed')

        task = Task.objects.get(id=task_id, user=request.user)
        task.completed = completed
        task.save()

        return JsonResponse({'status': 'success'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def filtered_tasks(request, filter_type):
    today = date.today()

    if filter_type == 'today':
        tasks = Task.objects.filter(due_date=today)
    elif filter_type == 'pending':
        tasks = Task.objects.filter(due_date__gt=today)
    elif filter_type == 'overdue':
        tasks = Task.objects.filter(due_date__lt=today)
    else:
        tasks = Task.objects.all()

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'current_filter': filter_type
    })
