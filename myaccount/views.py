from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views import View
from myaccount.models import User, Profile
from myaccount.forms import UserLoginForm, UserSignupForm, UserProfileForm


from django.template.loader import get_template
from xhtml2pdf import pisa




class UserHomeView(View):
    def get(self, request):
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, 'myaccount/user_home.html', context)
    

class DownloadUserProfilePDFView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        
        # Get absolute URL for profile picture
        if profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(profile.profile_picture.url)
        else:
            profile_picture_url = request.build_absolute_uri('/static/myaccount/img/profile1.png')
        template = get_template("myaccount/user_profile_pdf.html")
        context = {
            'profile': profile,
            'profile_picture_url': profile_picture_url
        }
        html = template.render(context)
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="profile.pdf"'

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)
        
        return response



class UserProfileView(LoginRequiredMixin ,View):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        context = {
            'profile': profile,
        }
        return render(request, 'myaccount/user_profile.html', context)
    
class UserProfileCreateView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        form = UserProfileForm(instance=profile)
        context = {
            'form': form,
        }
        return render(request, 'myaccount/user_profile_create.html', context)
    def post(self, request):
        profile = request.user.profile
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        context = {
            'form': form,
        }
        return render(request, 'myaccount/user_profile_create.html', context)



class UserSignupView(View):
    def post(self,request):
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
        context = {
            'form': form,
        }
        return render(request, 'myaccount/user_signup.html', context)
    
    def get(self, request):
        form = UserSignupForm()
        context = {
            'form': form,
        }
        return render(request, 'myaccount/user_signup.html', context)


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {
            'form':form
        }
        return render(request, 'myaccount/user_login.html', context)
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')
            else:
                print('Not authenticated')
                form.add_error(None, "Invalid email or password")
        context = {
            'form': form
        }
        return render(request, 'myaccount/user_login.html', context)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(self.request)
        return redirect('user_home')
    

class UserPasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form,
        }
        return render(request, 'myaccount/user_password_change.html', context)
    
    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user_dashboard')
        context = {
            'form': form,
        }
        return render(request, 'myaccount/user_password_change.html', context)


class UserDashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'myaccount/user_dashboard.html')
    


    
# @login_required
# def userPasswordChangeView(request):
#     if request.method == "POST":
#         form = PasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             return redirect('user_dashboard')
#     else:
#         form = PasswordChangeForm(user=request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'myaccount/user_password_change.html', context)



# @login_required
# def userDashboard(request):
#     return render(request, 'myaccount/user_dashboard.html')


# def userLoginView(request):
#     if request.method=='POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             print('email: ', email)
#             password = form.cleaned_data['password']
#             print('Password: ', password)
#             user = authenticate(request, email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('user_dashboard')
#             else:
#                 print('Not authenticated')

#     else:
#         form = UserLoginForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'myaccount/user_login.html', context)


# def userLogoutView(request):
#     logout(request)
#     return redirect('user_home')


# def userSignupView(request):
#     if request.method == "POST":
#         form = UserSignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_signup')
#     else:
#         form = UserSignupForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'myaccount/user_signup.html', context)



# @login_required
# def userProfileView(request):
#     profile = request.user.profile
#     if request.method == "POST":
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('user_profile')
#     else:
#         form = UserProfileForm(instance=profile)
#     context = {
#         'form': form,
#     }
#     return render(request, 'myaccount/user_profile_create.html', context)