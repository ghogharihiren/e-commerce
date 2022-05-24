from django import forms
from .models import*
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm



class RegisterForm(UserCreationForm):
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),
    )
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','role','mobile']
        widgets = {
            'role': forms.Select(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),       
        }
        
class Userlogin(AuthenticationForm):
    username=forms.CharField(label='Username')
    password=forms.CharField(label='Password',widget=forms.PasswordInput()) 

class EditprofileForm(forms.ModelForm):
    class Meta:
        model=User    
        fields=['first_name','last_name','username','email','role','mobile']
        widgets = {
            'role': forms.Select(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),       
        }  

    
class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),    
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center'}),    
    )
    
    
class AddproductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_name','category','quantity','price','pic','description']    
        widgets={
            'product_name': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'pic': forms.FileInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),    
        }
        
class EditproductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_name','category','quantity','price','pic','description']    
        widgets={
            'product_name': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'pic': forms.FileInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),    
        }
               
class AddcartForm(forms.ModelForm):
    
    class Meta:
        model=Mycart
        fields=['quantity']   
        
class EditcartForm(forms.ModelForm):
    class Meta:
        model=Mycart
        fields=['quantity'] 
        widgets={
            'quantity': forms.NumberInput(attrs={'class':'form-control'}),
        }             
        
        
        
class BuyproductForm(forms.ModelForm):
    class Meta:
        model=Buyproduct
        fields=['addres','payment_method'] 
        widgets={
            'addres': forms.Textarea(attrs={'class':'form-control'}),   
            'payment_method': forms.Select(attrs={'class':'form-control'}),     
        }       
        
class EditduyproductForm(forms.ModelForm):
    class Meta:
        model=Buyproduct
        fields=['addres','payment_method','quantity']    
        
        widgets={
            'addres': forms.Textarea(attrs={'class':'form-control'}),   
            'payment_method': forms.Select(attrs={'class':'form-control'}),    
            'quantity':forms.NumberInput(attrs={'class':'form-control'})
        }    
        
          