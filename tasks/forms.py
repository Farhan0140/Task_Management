
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
    assigned_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label="Assign To"
    )

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        # print(employees)
        super().__init__(*args, **kwargs) # Unpack 

        # print(self.fields)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]



class Style_Form_Mixins:

    default_classes = "border-2 rounded-lg border-gray-300 p-2"

    def apply_widget_styles(self):
        for field_name, field in self.fields.items():
            if isinstance( field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} px-3 w-full",
                    'placeholder': f"Enter {field.label} Name"
                })
            elif isinstance( field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} px-3 mt-2 w-full",
                    'placeholder': "Enter Details Description"
                })
            elif isinstance( field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} mt-2 bg-gray-200",
                    'placeholder': "Enter Details Description"
                })
            elif isinstance( field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': f"mt-2 p-3 font-semibold",
                    'placeholder': "Enter Details Description"
                })



# Django Model Form

from tasks.models import *

class Task_Model_Form( Style_Form_Mixins, forms.ModelForm ):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widget_styles()


    class Meta:
        model = Tasks
        # fields = '__all__'
        fields = ['title', 'description', 'due_date', 'assigned_to']
        # exclude = ['project', 'is_completed' ......]

        widgets = {
            
            'due_date': forms.SelectDateWidget(),
            'assigned_to': forms.CheckboxSelectMultiple()

            # Reduce Redundancy Using Mixins

            # 'title': forms.TextInput(attrs={
            #     'class': 'border-2 rounded-lg border-gray-300 w-full p-2 px-3',
            #     'placeholder': 'Enter Task Name'
            # }),

            # 'description': forms.Textarea(attrs={
            #     'class': 'border-2 rounded-lg border-gray-300 w-full p-2 px-3 mt-2',
            #     'placeholder': 'Enter Details Description'
            # }),
            
            # 'due_date': forms.SelectDateWidget(attrs={
            #     'class': 'border-2 border-gray-300 p-2 rounded-lg mt-2 bg-gray-200'
            # }),

            # 'assign_to': forms.CheckboxSelectMultiple(attrs={
            #     'class': 'mt-2 p-3 font-semibold'
            # }),
        }