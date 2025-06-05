
from django import forms

# Django Form

class Task_Form(forms.Form):
    title = forms.CharField(
        max_length=200,
        label="Task Title"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label="Description"
    )
    due_date = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Due Date"
    )
    assign_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label="Assign To"
    )

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        # print(employees)
        super().__init__(*args, **kwargs) # Unpack 

        # print(self.fields)
        self.fields['assign_to'].choices = [(emp.id, emp.name) for emp in employees]


# Django Model Form

from tasks.models import *

class Task_Model_Form(forms.ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['title', 'description', 'due_date', 'assign_to']
        # exclude = ['project', 'is_completed' ......]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'border-2 rounded-lg border-gray-300 w-full p-2 px-3',
                'placeholder': 'Enter Task Name'
            }),

            'description': forms.Textarea(attrs={
                'class': 'border-2 rounded-lg border-gray-300 w-full p-2 px-3 mt-2',
                'placeholder': 'Enter Details Description'
            }),
            
            'due_date': forms.SelectDateWidget(attrs={
                'class': 'border-2 border-black-500 p-2 rounded-lg mt-2'
            }),

            'assign_to': forms.CheckboxSelectMultiple(attrs={
                'class': 'mt-2 p-3 font-semibold'
            }),
        }