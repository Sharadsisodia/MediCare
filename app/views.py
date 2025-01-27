from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if user.account_type == 'doctor' and not user.speciality:
                messages.error(request, "Speciality is required for doctors.")
                return render(request, 'signup.html', {'form': form})
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:  # Check if the user is already logged in
        # Redirect to the appropriate dashboard if already logged in
        if request.user.account_type == 'doctor':
            return redirect('doctor_dashboard')
        elif request.user.account_type == 'patient':
            return redirect('patient_dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Check account type and redirect accordingly
            if user.account_type == 'doctor':
                return redirect('doctor_dashboard')  # Redirect to doctor's dashboard
            elif user.account_type == 'patient':
                return redirect('patient_dashboard')  # Redirect to patient's dashboard
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Log out the user
    response = redirect('login')  # Redirect to the login page

    # Add headers to prevent caching
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


from datetime import date
from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BlogPost
def doctor_dashboard(request):
    user = request.user  # Get logged-in user
    appointments = Appointment.objects.filter(
        doctor=user, 
        date__gte=datetime.date.today()
    ).order_by('date', 'start_time')

    # Fetch blogs authored by the current user
    blog_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    blog_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Calculate blog stats
    total_posts = blog_posts.count()
    from datetime import date

    def count_upcoming_appointments(doctor):
        # Count appointments where the doctor is assigned and the appointment date is today or in the future
        return Appointment.objects.filter(
            doctor=doctor,
            date__gte=date.today()
        ).count()

    upcoming_count = count_upcoming_appointments(user)
    
    return render(request, 'doctor_dashboard.html', {'user': user,'appointments':appointments, "blog_posts":blog_posts,"total_posts":total_posts,"upcoming_count":upcoming_count})

def patient_dashboard(request):
    user = request.user  # Get logged-in user
    return render(request, 'patient_dashboard.html', {'user': user})



from django.contrib.auth.decorators import login_required
from .models import Appointment
import datetime  # Add this import

@login_required
def upcoming_appointments(request):
    user = request.user  # Get the logged-in user

    # Fetch upcoming appointments for the logged-in patient
    appointments = Appointment.objects.filter(patient=user, date__gte=datetime.date.today()).order_by('date', 'start_time')

    
    # Render the page with the appointments
    return render(request, 'upcoming_appointments.html', {'user': user, 'appointments': appointments})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment
import datetime

@login_required
def doctor_upcoming_appointments(request):
    user = request.user  # Get the logged-in user

    # Ensure the user is a doctor
    if user.account_type != 'doctor':
        return render(request, 'error.html', {'message': 'Unauthorized access.'})

    # Fetch upcoming appointments for the logged-in doctor
    appointments = Appointment.objects.filter(
        doctor=user, 
        date__gte=datetime.date.today()
    ).order_by('date', 'start_time')
    
    # Fetch blogs authored by the current user
    blog_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    blog_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Calculate blog stats
    total_posts = blog_posts.count()

    def count_upcoming_appointments(doctor):
        # Count appointments where the doctor is assigned and the appointment date is today or in the future
        return Appointment.objects.filter(
            doctor=doctor,
            date__gte=date.today()
        ).count()

    upcoming_count = count_upcoming_appointments(user)

    # Render the page with the appointments
    return render(request, 'doctor_upcoming_appointments.html', {'appointments': appointments,"total_posts":total_posts,"upcoming_count":upcoming_count})



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Appointment
from .forms import AppointmentForm
from .utils import create_google_calendar_event

@login_required
def list_doctors(request):
    doctors = CustomUser.objects.filter(account_type='doctor')
    return render(request, 'list_doctors.html', {'doctors': doctors})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Appointment
from .forms import AppointmentForm
from .utils import create_google_calendar_event  # Make sure this function is imported correctly

@login_required
def book_appointment(request, doctor_id):
    # Fetch the doctor using the doctor_id and ensure they are of account_type 'doctor'
    doctor = get_object_or_404(CustomUser, id=doctor_id, account_type='doctor')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        
        # Debugging: check if form is valid and output any errors
        if form.is_valid():
            # Save form but do not commit yet
            appointment = form.save(commit=False)
            
            # Assign the doctor and patient
            appointment.doctor = doctor
            appointment.patient = request.user  # The logged-in user is the patient
            
            # Save the appointment
            appointment.save()

            # Optionally create a Google Calendar event for the appointment
            create_google_calendar_event(appointment)

            # Redirect or render a confirmation page
            return render(request, 'upcoming_appointments', {'appointment': appointment})

        else:
            # Debugging: Output the errors if the form is not valid
            print("Form errors:", form.errors)

    else:
        # If it's a GET request, initialize an empty form
        form = AppointmentForm()

    # Pass doctor and form to the template for rendering
    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .utils import delete_google_calendar_event  # Utility to delete Google Calendar events

@login_required
def cancel_appointment(request, appointment_id):
    # Fetch the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    # Try to delete the Google Calendar event
    try:
        delete_google_calendar_event(appointment)  # Assuming this utility function exists
    except Exception as e:
        print(f"Error deleting Google Calendar event: {e}")

    # Delete the appointment from the database
    appointment.delete()

    # Redirect to the upcoming appointments page
    return redirect('upcoming_appointments') # Replace with your appointments page URL name





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from .models import BlogPost

@login_required
def doctor_create_blog(request):
    # user=request.user
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, "Blog created successfully!")
            return redirect('doctor_dashboard')  # Replace with your dashboard view name
    else:
        form = BlogPostForm()

    # Fetching draft posts for the logged-in user
    draft_posts = BlogPost.objects.filter(author=request.user, is_draft=True)

     # Fetch blogs authored by the current user
    blog_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Calculate blog stats
    total_posts = blog_posts.count()
    
    def count_upcoming_appointments(doctor):
        # Count appointments where the doctor is assigned and the appointment date is today or in the future
        return Appointment.objects.filter(
            doctor=doctor,
            date__gte=date.today()
        ).count()

    upcoming_count = count_upcoming_appointments(request.user)

    context = {
        'form': form,
        'draft_posts': draft_posts,
        "total_posts":total_posts,
        "upcoming_count":upcoming_count,
    }
    

    return render(request, 'doctor_create_blog.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogPostForm

@login_required
def edit_blog_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id, author=request.user)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            blog_post = form.save(commit=False)  # Save the form but don't commit to DB yet
            blog_post.status = 'published'  # Ensure you update the status if needed
            blog_post.save()
            messages.success(request, "Blog edited successfully!")
            return redirect('doctor_dashboard')  # Replace with your dashboard view name
    else:
        form = BlogPostForm(instance=blog_post)

    blog_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Calculate blog stats
    total_posts = blog_posts.count()

    context = {
        'form': form,
        'blog_post': blog_post,
        "total_posts":total_posts,
    }
    

    return render(request, 'edit_blog_post.html', context)



@login_required
def delete_blog_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        blog_post.delete()
        messages.success(request, "Blog deleted successfully!")
        return redirect('doctor_dashboard')  # Replace with your dashboard view name

    context = {
        'blog_post': blog_post,
    }
    return render(request, 'confirm_delete.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import BlogPost

@login_required
def delete_draft(request, post_id):
    # Fetch only the draft version of the blog post
    blog_post = get_object_or_404(BlogPost, id=post_id, author=request.user, is_draft=True)
    
    # Change the draft status to False
    blog_post.is_draft = False
    blog_post.save()
    
    # Notify the user
    messages.success(request, f'The draft for "{blog_post.title}" has been deleted successfully.')
    return redirect('doctor_dashboard')  # Replace with your dashboard view name



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import BlogPost

@login_required
def doctor_my_blogs(request):
    user = request.user
    # Retrieve all blog posts authored by the current doctor
    blog_posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    
    # Calculate blog stats
    total_posts = blog_posts.count()
    total_views = sum(post.views for post in blog_posts)
    total_likes = sum(post.likes for post in blog_posts)
    
    def count_upcoming_appointments(doctor):
        # Count appointments where the doctor is assigned and the appointment date is today or in the future
        return Appointment.objects.filter(
            doctor=doctor,
            date__gte=date.today()
        ).count()

    upcoming_count = count_upcoming_appointments(user)

    context = {
        'blog_posts': blog_posts,
        'total_posts': total_posts,
        'total_views': total_views,
        'total_likes': total_likes,
        "upcoming_count":upcoming_count,
    }
    return render(request, 'doctor_my_blogs.html', context)



from django.shortcuts import render
from .models import BlogPost
from django.contrib.auth.decorators import login_required

@login_required
def patient_blogs(request):
    # Fetch published blog posts (excluding drafts)
    blog_posts = BlogPost.objects.filter(is_draft=True).order_by('-created_at')
    
    return render(request, 'patient_blogs.html', {'blog_posts': blog_posts})
