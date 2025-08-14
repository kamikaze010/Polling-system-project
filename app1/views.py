from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
import matplotlib
from app1.emailbackend import  Emailbackend
from .models import CustomUser,Poll,PollOptions,Vote
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import AddUserForm, EditUserForm,PollForm,PollOptionFormset,UpdateUserForm
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .models import Profile
import pandas as pd
matplotlib.use('agg')

import matplotlib.pyplot as plt
import io
import base64
import numpy as np


def landing_page(request):
    return render(request,'landing_page.html')
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        mobile_number = request.POST.get('mobile')  
        address = request.POST.get('address') 
        gender = request.POST.get('gender')  

        if ' ' in uname:
            return HttpResponse("Username should not contain spaces.")
        
        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same")
        else:
            my_user = CustomUser.objects.create_user(username=uname, email=email, password=pass1, mobile_number=mobile_number, address=address, gender=gender)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')



def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = Emailbackend().authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_role = user.role
            if user_role == 'admin':
                return redirect('admin_dashboard')
            elif user_role == 'voter':
                return redirect('voter_dashboard')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')




def LogoutPage(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def view_profile(request):
    return render(request,'profile.html')


@login_required(login_url='login')
def voter_dashboard(request):
    return render(request,'voter_dashboard.html')

@login_required(login_url='login')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')


@login_required(login_url='login')
def next_page(request):
    return render(request,'next_page.html')

def letsvote(request):
    return render(request,'events.html')



def users_view(request):
    return render(request,'users.html')



def display_events(request):
    return render(request,'events.html')

def report_view(request):
    return render(request,'report.html')

class Users(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        if request.user.is_superuser:
            UserModel_data = CustomUser.objects.all().order_by('username')
            return render(request, 'users.html', {'UserModeldata': UserModel_data})
        else:
            return render(request, 'unauthorized.html')

class Add_UserModel(View):
    def get(self, request):
        fm = AddUserForm()
        return render(request, 'add_user.html', {'form': fm})
    
    def post(self, request):
        fm = AddUserForm(request.POST)
        if fm.is_valid():
            password = fm.cleaned_data['password']
            hashed_password = make_password(password)
            fm.instance.password = hashed_password
            fm.save()
            return redirect('users')
        else:
            return render(request, 'add_user.html', {'form': fm})


class Delete_UserModel(View):

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        data = request.POST
        id = data.get('id')
        UserModeldata = CustomUser.objects.get(id=id)
        UserModeldata.delete()
        return redirect('users')

class Edit_UserModel(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, id):
        userm = CustomUser.objects.get(id=id)
        fm = EditUserForm(instance=userm)
        return render(request, 'edit_usermodel.html', {'form':fm})
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request, id):
        userm = CustomUser.objects.get(id=id)
        fm = EditUserForm(request.POST, instance=userm)
        if fm.is_valid():
            fm.save()
            return redirect('users')
        else:
            return render(request, 'edit_usermodel.html', {'form':fm})
        
def Polls(request):

    poll_data = Poll.objects.all()
    poll_options_data = PollOptions.objects.all()

    return render(request,'events.html',{'Poll':poll_data,'Poll_options':poll_options_data})
    

from django.contrib import messages

@login_required(login_url='login')
def create_poll(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        option_formset = PollOptionFormset(request.POST)

        if poll_form.is_valid() and option_formset.is_valid():
            poll = poll_form.save()
            options = option_formset.save(commit=False)
            for option in options:
                option.poll = poll
                option.save()
            messages.success(request, 'Poll has been created successfully.')
            return redirect('events')
    else:
        poll_form = PollForm()
        option_formset = PollOptionFormset()

    return render(request, 'create_poll.html', {'poll_form': poll_form, 'option_formset': option_formset})

@login_required(login_url='login')
def edit_poll(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
        print("running")
    except Poll.DoesNotExist:
        messages.error(request, 'Poll not found.')
        return redirect('events')  # Redirect to a relevant view

    print("running up to here")
    poll_form = PollForm(request.POST, instance=poll)
    option_formset = PollOptionFormset(request.POST, instance=poll)

    if poll_form.is_valid() and option_formset.is_valid():
        poll = poll_form.save()
        options = option_formset.save(commit=False)
        for option in options:
            option.poll = poll
            option.save()
        messages.success(request, 'Poll has been updated successfully.')
        return redirect('events')  # Redirect to a relevant view
    
    else:
        poll_form = PollForm(instance=poll)
        option_formset = PollOptionFormset(instance=poll)

    return render(request, 'edit_poll.html', {'poll_form': poll_form, 'option_formset': option_formset})


            
@login_required(login_url='login')
def display_events(request):

    poll_data = Poll.objects.all().order_by('-start_date') # send
    poll_options_data = PollOptions.objects.all()
    poll_length = len(poll_data)

    return render(request,'events.html',{'Poll':poll_data,'Poll_options':poll_options_data,'poll_length':poll_length})


@login_required(login_url='login')
def vote(request):
    if request.method == 'POST':
        option_id = request.POST.get('option')
        
        if not option_id:
            messages.error(request, "You must choose an option before voting.")
            return redirect('events')
        
        option = get_object_or_404(PollOptions, id=option_id)
        poll = option.poll

        if Vote.objects.filter(user=request.user, poll=poll).exists():
            messages.error(request, "You have already voted in this poll.")
            return redirect('events')

        vote = Vote(user=request.user, poll=poll)
        vote.save()

        option.votes += 1
        option.save()

        messages.success(request, "You have successfully voted.")
    
    return redirect('events')

def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user.role != 'admin':
        # If not admin, show a message or redirect to some other page
        messages.error(request, "You are not authorized to delete this poll.")
        return redirect('events')
    poll.delete()
    return redirect('events')


def home(request):
    return render(request, 'home.html')


def profile(request):
    return render(request,'profile.html')



@login_required
def profile_edit(request):
    if request.user.is_authenticated:
        current_user = CustomUser.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)

        if request.method == 'POST':
            if user_form.is_valid():
                if user_form.has_changed():
                    user_form.save()
                    messages.success(request, "User profile has been updated.")
                else:
                    messages.info(request, "No changes were made to the profile.")
                return redirect('profile') 

        return render(request, "profile_edit.html", {'user_form': user_form})
    else:
        messages.error(request, "You must be logged in to edit your profile.")
        return redirect('login')

    
@login_required(login_url='login')
def report(request):
    # Retrieve poll data from the database
    poll_options = PollOptions.objects.all()

    # Convert poll data to a DataFrame
    df = pd.DataFrame(list(poll_options.values()))

    if df.empty:
        messages.info(request, "There are no poll options to display.")
        return render(request, 'no_event.html', {'plot_data_dict': {}})

    # Group poll options by poll question
    grouped_options = df.groupby('poll_id')

    # Dictionary to hold plot data for each poll question
    plot_data_dict = {}

    # Generate a bar chart for each poll question
    for poll_id, group_df in grouped_options:
        plt.figure(figsize=(8, 6))  # size of the plot
        group_df.plot(kind='bar', x='option_text', y='votes', rot=45) #bar chart
        plt.xlabel('Poll Options')  # Label for the x-axis
        plt.ylabel('Vote Counts')  # Label for the y-axis
        plt.title(f'Poll Results')  # Title of the plot
        plt.tight_layout()

        # Convert the plot to a base64-encoded string
        buffer = io.BytesIO()  # Create a memory buffer
        plt.savefig(buffer, format='png')  # Save the plot in PNG format to the buffer
        buffer.seek(0)  # Reset the buffer position to the start
        plot_data = base64.b64encode(buffer.read()).decode()  # Encode the plot as base64
        buffer.close()  # Close the buffer to free memory

        poll_question = Poll.objects.get(pk=poll_id).question
        # Store plot data in the dictionary
        plot_data_dict[poll_question] = plot_data

        plt.close()
        

    plot_data_dict = dict(reversed(plot_data_dict.items()))

    # Pass the dictionary containing plot data for all poll questions to the template
    return render(request, 'report.html', {'plot_data_dict': plot_data_dict})


@login_required(login_url='login')
def admin_dashboard(request):

    Number_Of_User = len(CustomUser.objects.all())
    Number_Of_Active_Events = len(Poll.objects.filter(start_date__lte = timezone.localtime(timezone.now()),end_date__gte = timezone.localtime(timezone.now())))
    Number_Of_Votes = len(Vote.objects.all())

    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    context = {
        'Number_Of_User': Number_Of_User,
        'Number_Of_Active_Events':Number_Of_Active_Events,
        'Number_Of_Votes':Number_Of_Votes

    }
    return render(request,'admin_dashboard.html',context)

# @login_required(login_url='login')
# def candidate_dashboard(request):
#     if request.user.role != 'candidate' and request.user.role !='admin':
#         return HttpResponseForbidden("You are not authorized to access this page.")
#     return render(request,'candidate_dashboard.html')



@login_required(login_url='login')
def voter_dashboard(request):

    Number_Of_User = len(CustomUser.objects.all())
    Number_Of_Active_Events = len(Poll.objects.filter(start_date__lte = timezone.localtime(timezone.now()),end_date__gte = timezone.localtime(timezone.now())))
    Number_Of_Votes = len(Vote.objects.all())
    context = {
        'Number_Of_User': Number_Of_User,
        'Number_Of_Active_Events':Number_Of_Active_Events,
        'Number_Of_Votes':Number_Of_Votes
    }

    return render(request,'voter_dashboard.html',context)


# Password reset request view
def password_reset_request(request):
    return PasswordResetView.as_view(template_name='registration/password_reset_form.html')(request)

# Password reset done view
def password_reset_done(request):
    return PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html')(request)

# Password reset confirm view
def password_reset_confirm(request, uidb64, token):
    return PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html')(request, uidb64=uidb64, token=token)

# Password reset complete view
def password_reset_complete(request):
    return PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html')(request)


# from django.core.mail import send_mail

# def test_email(request):
#     send_mail(
#         'Subject here',
#         'Here is the message.',
#         'tvashita75@gmail.com',
#         ['recipient@example.com'],  # Replace with a valid recipient email address
#         fail_silently=False,
#     )
#     return HttpResponse("Email sent")