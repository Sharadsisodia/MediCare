from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    ACCOUNT_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        
    ]
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        required=True, 
        label="Account Type",
    )
    speciality = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Speciality'}),
        label="Speciality (For Doctors Only)"
    )

    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    profile_picture = forms.ImageField(required=False)
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    address_line1 = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Address Line 1'})
    )
    city = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    state = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'State'})
    )
    pincode = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Pincode'}),
        validators=[RegexValidator(
            regex='^\d{6}$',
            message='Pincode must be exactly 6 digits.',
            code='invalid_pincode'
        )]
    )

    class Meta:
        model = CustomUser
        fields = [
            'account_type', 'speciality', 'first_name', 'last_name', 'username',
            'email', 'password1', 'password2', 'profile_picture',
            'address_line1', 'city', 'state', 'pincode'
        ]

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')
        speciality = cleaned_data.get('speciality')

        # Ensure 'speciality' is filled out if account type is 'doctor'
        if account_type == 'doctor' and not speciality:
            self.add_error('speciality', "Speciality is required for doctors.")
        
        # If account type is 'patient', ensure speciality is not accidentally filled
        if account_type == 'patient' and speciality:
            self.add_error('speciality', "Speciality should not be provided for patients.")

        return cleaned_data


from django import forms
from .models import Appointment

from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment

from django.core.exceptions import ValidationError

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'start_time', 'reason', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-group', 'id': 'date', 'type': 'date', 'required': True}),
            'start_time': forms.Select(attrs={'class': 'form-group', 'id': 'time', 'required': True}, choices=[
                ("", "Select a time slot"),
                ("09:00", "09:00 AM"),
                ("09:45", "09:45 AM"),
                ("10:30", "10:30 AM"),
                ("11:15", "11:15 AM"),
                ("14:00", "14:00 AM"),
                ("14:45", "14:45 PM"),
                ("15:30", "15:30 PM"),
                ("16:15", "16:15 PM"),
            ]),
            'reason': forms.Textarea(attrs={'class': 'form-group', 'id': 'reason', 'rows': 4, 'required': True}),
            'notes': forms.Textarea(attrs={'class': 'form-group', 'id': 'notes', 'rows': 3}),
        }
        labels = {
            'date': 'Preferred Date',
            'start_time': 'Preferred Time',
            'reason': 'Reason for Visit',
            'notes': 'Additional Notes (Optional)',
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')

        # Check if doctor is passed explicitly
        doctor = self.initial.get('doctor')  # Pass doctor to the form context

        if doctor and date and start_time:
            conflict = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                start_time=start_time
            ).exists()

            if conflict:
                raise ValidationError(
                    f"An appointment with Dr. {doctor.first_name} {doctor.last_name} at {start_time} on {date} is already booked."
                )

        return cleaned_data



from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'featured_image', 'summary', 'content', 'is_draft']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter blog title'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Select a category'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control', 
                'accept': 'image/*'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Brief overview of your blog post'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 10, 
                'placeholder': 'Write your blog content here...'
            }),
            'is_draft': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

