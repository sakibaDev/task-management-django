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
       

    context = {'form':form}
    return render(request,"task_form.html",context)

def view_task(request):
    tasks = Task.objects.all()
    return render(request,'show_task.html',{'tasks':tasks})