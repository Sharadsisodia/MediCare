"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.login_view, name='home'),  # Redirect default route to login
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('book-appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('ucoming_appointments/', views.upcoming_appointments, name='list_doctors'),
    path('upcoming_appointments/', views.upcoming_appointments, name='upcoming_appointments'),
    path('doctor_upcoming_appointments/', views.doctor_upcoming_appointments, name='list_doctors'),
    path('doctor_create_blog/', views.doctor_create_blog, name='create_blog'),
    path('edit_blog_post/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),
    path('delete_blog_post/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('delete_draft/<int:post_id>/', views.delete_draft, name='delete_draft'),
    path('doctor_my_blogs/', views.doctor_my_blogs, name='my_blogs'),
    path('patient_blogs/', views.patient_blogs, name='patients_blogs'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)