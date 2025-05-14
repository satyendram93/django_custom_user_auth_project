from django.urls import path 
from django.contrib.auth import views as auth_views
from myaccount import views

urlpatterns = [
    path('',views.UserHomeView.as_view(), name='user_home'),
    path('user-profile-pdf/', views.DownloadUserProfilePDFView.as_view(), name='user_profile_pdf'),
    path('user-profile/',views.UserProfileView.as_view(), name='user_profile'),
    path('user-profile-create/',views.UserProfileCreateView.as_view(), name='user_profile_create'),
    path('signup/',views.UserSignupView.as_view(), name='user_signup'),
    path('login/',views.UserLoginView.as_view(), name='user_login'),
    path('logout/',views.UserLogoutView.as_view(), name='user_logout'),
    path('user-dashboard/',views.UserDashboard.as_view(), name='user_dashboard'),
    path('user-password-change/',views.UserPasswordChangeView.as_view(), name='user_password_change'),


    #Authentication
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='myaccount/password_reset.html'), 
        name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='myaccount/password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='myaccount/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='myaccount/password_reset_complete.html'), 
        name='password_reset_complete'),


    # path('user-password-change/',views.userPasswordChangeView, name='user_password_change'),
    # path('signup/',views.userSignupView, name='user_signup'),
    # path('login/',views.userLoginView, name='user_login'),
    # path('logout/',views.userLogoutView, name='user_logout'),
    # path('user-dashboard/',views.userDashboard, name='user_dashboard'),
    # path('user-profile-create/',views.userProfileView, name='user_profile_create'),
]
