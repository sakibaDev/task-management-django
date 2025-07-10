from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q

from tasks.forms import TaskModelForm, TaskDetailModelForm
from tasks.models import Task, Employee


def manager_dashboard(request):
    task_type = request.GET.get('type', 'all')

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    if task_type == 'completed':
        tasks = base_query.filter(status="COMPLETED")
    elif task_type == 'in_progress':
        tasks = base_query.filter(status="IN_PROGRESS")
    elif task_type == 'pending':
        tasks = base_query.filter(status="PENDING")
    else:
        tasks = base_query.all()

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))
    )

    context = {
        'tasks': tasks,
        'counts': counts,
    }

    return render(request, "dashboard/manager_dashboard.html", context)


def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")


def create_task(request):
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Added!")
            # Redirect to dashboard to see the new task
            return redirect('manager_dashboard')

    else:
        task_form = TaskModelForm()
        task_detail_form = TaskDetailModelForm()

    context = {
        'task_form': task_form,
        'task_detail_form': task_detail_form,
    }

    return render(request, "task_form.html", context)
def update_task(request, id):
    task = get_object_or_404(Task, id=id)

    # Try to get the related TaskDetail object
    task_detail = getattr(task, 'details', None)

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task_detail)

        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated!")
            return redirect('manager_dashboard')

    else:
        task_form = TaskModelForm(instance=task)
        task_detail_form = TaskDetailModelForm(instance=task_detail)

    context = {
        'task_form': task_form,
        'task_detail_form': task_detail_form,
    }

    return render(request, "task_form.html", context)



def view_task(request, employee_id):
    # Example: Show tasks assigned to a specific employee
    employee = get_object_or_404(Employee, id=employee_id)
    tasks = Task.objects.filter(assigned_to=employee)
    return render(request, 'show_task.html', {'employee': employee, 'tasks': tasks})


from django.views.decorators.http import require_POST

@require_POST  # Ensures deletion only happens via POST request
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('manager_dashboard')
