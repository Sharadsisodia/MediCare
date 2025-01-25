from django.contrib import admin

# Register your models here.
from .models import CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'account_type')
    filter_horizontal = ('groups', 'user_permissions')


from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'speciality', 'date', 'start_time', 'end_time')
    search_fields = ('doctor__username', 'patient__username', 'speciality')
    list_filter = ('date', 'speciality')

admin.site.register(Appointment, AppointmentAdmin)


from .models import BlogPost
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_draft', 'created_at', 'updated_at')  # Adjust fields as per your model
    list_filter = ('is_draft', 'category', 'created_at')  # Add filters for better usability
    search_fields = ('title', 'content')  # Enable search by title and content
    ordering = ('-created_at',)  # Order by the most recent first

admin.site.register(BlogPost, BlogPostAdmin)