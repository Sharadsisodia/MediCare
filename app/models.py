from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    ACCOUNT_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]

    account_type = models.CharField(
        max_length=7, choices=ACCOUNT_TYPE_CHOICES, default='patient'
    )
    # profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    profile_picture = CloudinaryField("profile_pics")
    address_line1 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)  # New field for doctors

    groups = models.ManyToManyField(
        'auth.Group', related_name='customuser_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='customuser_permissions', blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

# models.py
from django.db import models
from django.conf import settings

class Appointment(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_doctor'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_patient'
    )
    speciality = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    calendar_event_id = models.CharField(max_length=255, blank=True, null=True)  # New field for event ID

    def save(self, *args, **kwargs):
        if self.start_time and not self.end_time:
            from datetime import datetime, timedelta
            start_datetime = datetime.combine(self.date, self.start_time)
            self.end_time = (start_datetime + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)





from django.conf import settings
from django.db import models

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('wellness', 'Wellness'),
        ('technology', 'Technology'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    featured_image = models.ImageField(upload_to='blog_images/')
    summary = models.TextField(max_length=500)
    content = models.TextField()
    is_draft = models.BooleanField(default=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)  # Add this field
    likes = models.IntegerField(default=0)  # Add this field (if not already present)

    def __str__(self):
        return self.title

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost

@login_required
def blog_detail(request, blog_id):
    # Retrieve the blog post using its ID
    blog = get_object_or_404(BlogPost, id=blog_id)
    
    # Increment the views count
    blog.views += 1
    blog.save()
    
    # Pass the blog to the template for rendering
    return render(request, 'blog_detail.html', {'blog': blog})