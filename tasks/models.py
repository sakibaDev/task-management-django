from django.db import models

class Project(models.Model):
    name = models.CharField( max_length=100)
    start_date = models.DateField()

class Employee(models.Model):
    name=  models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):

    project = models.ForeignKey(Project,on_delete=models.CASCADE,default=1)

    assigned_to = models.ManyToManyField(Employee,related_name ='tasks')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskDetail(models.Model):
    HIGH ='H'
    MEDIUM ='M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low')
    )
    task = models.OneToOneField(Task,on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1,choices=PRIORITY_OPTIONS , default=HIGH)

