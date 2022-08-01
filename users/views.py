from multiprocessing import context
from operator import ne
import re
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm


def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

def index(request):
    
    return render(request,'users/index.html')
def contact(request):
    return render(request, 'users/contact.html')
def result(request):
    if request.method == 'POST':
        n =int(request.POST['truck'])
        bag = int(request.POST['con1'])
        can = int(request.POST['con2'])
        drum = int(request.POST['con3'])
        
        truck = (n*1000)
        

        drum_sec = truck/2
        bag_sec = truck/4
        can_sec = truck/4
        
        total_drums = (drum_sec/drum)
        total_bags = (bag_sec/bag)
        total_cans =  (can_sec/can)

        s1=round(total_drums)
        s2=round(total_cans)
        s3=round(total_bags)
        print("Total Number of Drums is ",round(total_drums),"Units")
        print("Total Number of cans is ",round(total_cans),"Units")
        print("Total Number of bags is ",round(total_bags),"Units")
        
        drums = round(total_drums) * drum
        cans = round(total_cans) * can
        bags = round(total_bags) * bag
        
        print("The Total weight of Drums is ", drums,"\n The Total weight of cans is ", cans,"\n The Total weight of bags is ",bags)
        
        total_weight = drums+cans+bags
        print("Total weight in truck ",total_weight)
        newc=0
        newb=0
        newd=0
        newcb=0
        newbb=0
        if total_weight>truck:
            capacity="Ooppss Truck Overloaded!!!"
            extra = total_weight-truck
            case = "You truck is having extra "+str(extra)+" kgs"
            if extra%bag == 0:
                print("hello")
                extra_bags = extra/bag
                remove = "Must remove "+str(extra_bags)+"  bags"
                # new = "Updated weight of truck is "+str(total_weight-(extra_bags*bag))+" and The number of bags now is "+str(round(total_bags)-extra_bags)
               
                s3 = (round(total_bags)-extra_bags)
            elif extra%can == 0:
                extra_cans = extra/can
                remove = "Must remove "+str(extra_cans)+" cans"
                # new = "Updated weight of truck is "+str(extra_cans*can-total_weight)+" and The number of cans now is "+str(round(total_cans)-extra_cans)
              
                s2 = (round(total_cans)-extra_cans)
            elif extra%drum ==0:
                extra_drums = extra/drum
                remove = "Must remove "+str(extra_drums)+"  drums"
                # new = "Updated weight of truck is "+str(extra_drums*drum-total_weight)+" and The number of Drums now is ",str(round(total_drums)-extra_drums)
               
                s1 = (round(total_drums)-extra_drums)
            elif drum >extra > can:
                extra_weight = total_weight-truck
                remove = "Must remove a can or some bags you have extra"+str(extra_weight)+" kgs"
                s2=s2-1
                
            elif can > extra > bag:
                extra_weight = total_weight-truck
                remove = "Must remove a bag or two you have extra"+str(extra_weight)+" kgs"
                s3 = s3-1
           
            params = {'s1':s1,'s2':s2,'s3':s3}
        elif total_weight==truck:
            capacity="You are good to Go "
            case =" "
            remove=" "
            newb = " "
            params = {'s1':s1,'s2':s2,'s3':s3}
        else:
            capacity="Truck is Underload !!"
            less = truck-total_weight

            case="You truck is having less "+str(less)+" kgs"
            if less%bag == 0:
                less_bags = less/bag
                remove = "Must add "+str(less_bags)+"  bags"
                # new = "Updated weight of truck is "+str(total_weight+(less_bags*bag))+" and The number of bags now is "+str(round(total_bags)+less_bags)
               
                s3 = (round(total_bags)+less_bags)
                
            elif less%can == 0:
                less_cans = less/can
                remove = "Must add "+str(less_cans)+" cans"
                # new = "Updated weight of truck is "+str(less_cans*can+total_weight)+" and The number of cans now is ",str(round(total_cans)+less_cans)
               
                s2 = (round(total_cans)+less_cans)
            elif less%drum ==0:
                less_drums = less/drum
                remove = "Must add "+str(less_drums)+"  drums"
                # new = "Updated weight of truck is "+str(less_drums*drum+total_weight)+" and The number of Drums now is "+str(round(total_drums)+less_drums)
               
                s1 = (round(total_drums)+less_drums)
            elif drum > less > can:
                less_weight = truck-total_weight
                remove = "Must add a can or some bags you have less"+str(less_weight)+" kgs"
                s2=s2+1
                
            elif can > less > bag:
                less_weight = truck-total_weight
                remove = " Must add a bag or two you have less"+str(less_weight)+" kgs"
                s3 = s3+1
            
            params = {'s1':s1,'s2':s2,'s3':s3}

    # print(newb)
    # print(newc)
    # print(newd)
    # print(newcb)
    # print(newbb)
    return render(request,'users/result.html',params)




@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
