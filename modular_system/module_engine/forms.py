from django import forms

class UpgradeForm(forms.Form):
    ACTION_CHOICES = [
        ('add_field', 'Add Field'),
        ('remove_field', 'Remove Field'),
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES)
    field_name = forms.CharField(max_length=100)
    field_type = forms.CharField(max_length=50) 
