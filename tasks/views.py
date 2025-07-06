from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm ,TaskModelForm
from tasks.models import Employee,Task

# Create your views here.

def manager_dashboard(request):
    return render(request ,"dashboard/manager_dashboard.html")
def user_dashboard(request):
    return render(request ,"dashboard/user_dashboard.html")

def create_task(request):
    # employees = Employee.objects.all()

    form = TaskModelForm() #for get method

    if request.method == 'POST': #for POST method
        form = TaskModelForm(request.POST)

        '''for ModelForm Data'''

        form.save()
        return render(request,'task_form.html',{'form':form,'message':'Task Added!'})
        '''for Django form data '''

        # if form.is_valid():
        #     data = form.cleaned_data
        #     title = data.get('title')
        #     description = data.get('description')
        #     assigned_to = data.get ('assigned_to')

        #     task=Task.objects.create(
        #         title=title , description=description
        #     )

        #     #Assign employee to Task
        #     for emp_id in assigned_to:
        #         employe = Employee.objects.get(id=emp_id)
        #         task.assigned_to.add(employe)

        return HttpResponse("Task added successfully!")

    context = {'form':form}
    return render(request,"task_form.html",context)
# from django.shortcuts import render, redirect
# from .forms import TaskModelForm
# from .models import Task

# def create_task(request):
#     if request.method == 'POST':
#         form = TaskModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('task_success')  # or some success URL
#     else:
#         form = TaskModelForm()

#     return render(request, 'task_form.html', {'form': form})
