from django import forms
from django.utils.timezone import now

from .models import DanceClassAttendance, DanceClass, User, DanceClassAssignment


class DanceClassAttendanceForm(forms.ModelForm):
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


class DanceClassForm(forms.ModelForm):
    class Meta:
        model = DanceClass
        fields = '__all__'
        widgets = {
            'level': forms.Select(choices=DanceClass.LEVEL_CHOICES),
            'days': forms.CheckboxSelectMultiple(choices=DanceClass.DAY_CHOICES),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.filter(groups__name='Dancer')
        self.fields['instructor'].queryset = User.objects.filter(groups__name='Instructor')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        if self.cleaned_data.get('users'):
            instance.users.set(self.cleaned_data['users'])

        return instance


class AddParticipantsForm(forms.ModelForm):
    class Meta:
        model = DanceClassAssignment
        fields = ['dance_class', 'user']
        widgets = {
            'dance_class': forms.HiddenInput(),
            'user': forms.Select(attrs={'type': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dance_class = kwargs.get('instance')

        self.fields['dance_class'].initial = dance_class
