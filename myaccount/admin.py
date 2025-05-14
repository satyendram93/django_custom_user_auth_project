from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from myaccount.models import User, Profile
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']

    def clean_password(self):
        return self.initial["password"]



class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ["email", "password", "first_name", "last_name", "created_at", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    search_fields = ["email"]
    ordering = ["email"]

    fieldsets = (
        (None, {"fields": ["email", "password"]}),
        ("Personal Info", {"fields": ["first_name", "last_name"]}),
        ("Permissions", {
            "fields": [
                "is_staff",
                "is_active",
                "is_superuser",
                "groups",              
                "user_permissions"     
            ]
        }),
        ("Important Dates", {"fields": ["last_login", "created_at", "updated_at"]}),
    )

    add_fieldsets = (
        (None, {
            "classes": ["wide"],
            "fields": ["email", "password1", "password2", "is_staff", "is_superuser", "is_active"],
        }),
    )

    readonly_fields = ["created_at", "updated_at", "last_login"]  

    filter_horizontal = ["groups", "user_permissions"]  

admin.site.register(User, CustomUserAdmin)



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'phone_no', 'country', 'updated_at', 'profile_picture']
admin.site.register(Profile, UserProfileAdmin)