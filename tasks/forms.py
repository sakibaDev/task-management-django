from django import forms

from tasks.models import Task,TaskDetail

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

# tasks/forms.py

from django import forms
from .models import Task, TaskDetail

# Mixin defined here directly
class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = field.widget
            base_class = 'block w-full px-4 py-2 mt-1 border rounded-md shadow-sm focus:ring focus:ring-blue-300 focus:outline-none'

            if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                base_class = 'mr-2 accent-blue-500'

            existing_classes = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{existing_classes} {base_class}'.strip()

# Now use it in your forms
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'assigned_to', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'assigned_to': forms.CheckboxSelectMultiple(),
        }

class TaskDetailModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = ['priority']


