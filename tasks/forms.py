from django import forms

from tasks.models import Task

#for form
class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label='Assigned to')

    # to fetch employee

    def __init__(self,*args, **kwargs):
        employee = kwargs.pop("employee",[])
        super().__init__(*args,**kwargs)
        self.fields["assigned_to"].choices=[
            (emp.id, emp.name ) for emp in employee
        ]

#for ModelForm
class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'assigned_to', 'description']  # title comes first
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'border border-gray-300 p-2 rounded w-full',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={'rows': 3}),
            'assigned_to': forms.CheckboxSelectMultiple(),
        }
