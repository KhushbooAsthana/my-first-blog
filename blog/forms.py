from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Post,Comment
#from info import SENDER_EMAIL,SENDER_PASSWORD
import smtplib

SENDER_EMAIL='python.blogtutorial@gmail.com'
SENDER_PASSWORD='Python@123'

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('author','text',)

class RegisterUser(forms.Form):
    username=forms.CharField(label='Enter User Name:',min_length=4,max_length=150)
    email=forms.EmailField(label='Enter Email:')
    password1=forms.CharField(label='Enter Password:',widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirm Password:',widget=forms.PasswordInput)
    first_name=forms.CharField(label='Enter First Name:',min_length=4,max_length=50)
    last_name=forms.CharField(label='Enter Lase Name:',min_length=4,max_length=50)

    def clean_username(self):
        username=self.cleaned_data['username'].lower()
        r=User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email=self.cleaned_data['email'].lower()
        r=User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise ValidationError("Passwords dont match")
        return password2
    def save(self, commit=True):
        print(self.cleaned_data['email'])
        user=User.objects.create_user(
            self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        smtp=smtplib.SMTP('smtp.gmail.com')
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(SENDER_EMAIL,SENDER_PASSWORD)
        subject="Registration successful!!!"
        msg="Hi"+self.cleaned_data['username']+"\n Thank you for registering with us!!! \n Thanks & Regards,\nKhushboo Asthana"
        email_msg="Subject: {} \n\n{}".format(subject,msg)
        smtp.sendmail(SENDER_EMAIL,self.cleaned_data['email'],email_msg)
        smtp.quit()
        return user
