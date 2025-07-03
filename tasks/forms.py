
from django import forms

class Style_Form_Mixins:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widget_styles()

    default_classes = "border-2 rounded-lg border-gray-300 p-2"

    def apply_widget_styles(self):
        for field_name, field in self.fields.items():
            if isinstance( field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} px-3 w-full",
                    'placeholder': f"Enter {field.label} Name"
                })
            elif isinstance( field.widget, forms.PasswordInput):
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
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })



# Django Model Form

from tasks.models import Tasks, Task_Detail

class Task_Model_Form( Style_Form_Mixins, forms.ModelForm ):

    class Meta:
        model = Tasks
        fields = ['title', 'description', 'due_date', 'assigned_to']

        widgets = {
            
            'due_date': forms.SelectDateWidget(),
            'assigned_to': forms.CheckboxSelectMultiple()

        }

class Task_Detail_Form( Style_Form_Mixins, forms.ModelForm ):
    class Meta:
        model = Task_Detail
        fields = ['priority', 'notes', 'task_image']