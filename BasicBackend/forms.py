from django import forms
from django.utils.timezone import now

from .models import DanceClassAttendance, DanceClass


class DanceClassAttendanceForm(forms.ModelForm):
    class Meta:
        model = DanceClassAttendance
        fields = ['session_date', 'user', 'status']

    def __init__(self, *args, **kwargs):
        dance_class_id = kwargs.pop('dance_class_id', None)
        dance_class = DanceClass.objects.get(pk=dance_class_id)
        super().__init__(*args, **kwargs)

        if dance_class:
            self.fields['user'].queryset = dance_class.users.all()


class ClassAttendanceForm(forms.ModelForm):
    class Meta:
        model = DanceClassAttendance
        fields = ['dance_class', 'session_date', 'user', 'status']
        widgets = {
            'dance_class': forms.HiddenInput(),
            'session_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=DanceClassAttendance.ATTENDANCE_STATUS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        dance_class_id = kwargs.pop('dance_class_id', None)
        dance_class = DanceClass.objects.get(pk=dance_class_id)
        super().__init__(*args, **kwargs)

        self.fields['session_date'].initial = now().date()
        self.fields['dance_class'].initial = dance_class
        self.fields['user'].queryset = dance_class.users.all()
        self.fields['user'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        dance_class = cleaned_data.get('dance_class')
        session_date = cleaned_data.get('session_date')

        if DanceClassAttendance.objects.filter(user=user, dance_class=dance_class, session_date=session_date).exists():
            raise forms.ValidationError("This attendance record already exists.")

        return cleaned_data
