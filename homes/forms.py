from django import forms
from .models import ApartmentApplication

class ApartmentApplicationForm(forms.ModelForm):

    # ✅ DEFINE FIELD HERE (NOT inside Meta)
    EMPLOYMENT_CHOICES = [
        ('employed', 'Employed'),
        ('self-employed', 'Self-Employed'),
        ('unemployed', 'Unemployed'),
    ]

    employment_status = forms.ChoiceField(
        choices=EMPLOYMENT_CHOICES,
        required=True
    )

    class Meta:
        model = ApartmentApplication
        fields = [
            'full_name',
            'email',
            'phone',
            'id_number',
            'apartment',
            'move_in_date',
            'employment_status',
            'monthly_income',
            'notes'
        ]

        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
        }