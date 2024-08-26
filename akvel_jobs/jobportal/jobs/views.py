from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Job, Application
from .forms import UserRegisterForm, JobForm, ApplicationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin/'  # Redirect to the admin panel for superusers
        return '/jobs/'

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin/'  # Redirect to admin panel if the user is a superuser
        return '/jobs/'
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('job-list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render
from .models import Job

from django.shortcuts import render
from .models import Job  # Adjust according to your actual model import

def job_list(request):
    # Get the query parameter for searching, if any
    query = request.GET.get('q', '')
    
    # Filter jobs based on the query
    jobs = Job.objects.filter(title__icontains=query)
    
    # Pass the jobs to the template
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


from django.shortcuts import render, redirect
from .forms import JobForm  # Make sure JobForm is defined in forms.py

def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job-list')  # Redirect to job list or another page
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            return redirect('job-list')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@login_required
def view_applications(request, job_id):
    if request.user.userprofile.is_admin:
        job = get_object_or_404(Job, id=job_id)
        applications = Application.objects.filter(job=job)
        return render(request, 'view_applications.html', {'applications': applications, 'job': job})
    else:
        return redirect('job-list')
    


from django.shortcuts import render, redirect
from .forms import RegistrationForm  # Import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login or another page
    else:
        form = RegistrationForm()

    return render(request, 'jobs/register.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import JobApplicationForm



def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)  # Get the specific job by ID
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job  # Link the application to the specific job
            application.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

