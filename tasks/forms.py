
from django import forms

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
