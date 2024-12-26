from django import forms
from .models import Order
from django.contrib.auth.forms import AuthenticationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline_date': forms.DateInput(attrs={'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'type': 'date'}),
    
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make fields read-only based on the user's role
        if user and not (user.is_superuser or user.groups.filter(name='Salespersons').exists()):
            self.fields['order_id'].widget.attrs['readonly'] = True
            self.fields['company_name'].widget.attrs['readonly'] = True
            self.fields['client_name'].widget.attrs['readonly'] = True
            self.fields['salesperson_name'].widget.attrs['readonly'] = True
            self.fields['front_design'].widget.attrs['readonly'] = True
            self.fields['back_design'].widget.attrs['readonly'] = True
            self.fields['pocket_design'].widget.attrs['readonly'] = True
            self.fields['sleeve_design'].widget.attrs['readonly'] = True
            self.fields['design_Size'].widget.attrs['readonly'] = True
            self.fields['product_list'].widget.attrs['readonly'] = True
            self.fields['quantity'].widget.attrs['readonly'] = True
            self.fields['order_date'].widget.attrs['readonly'] = True
            self.fields['deadline_date'].widget.attrs['readonly'] = True
            self.fields['completed_date'].widget.attrs['readonly'] = True
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))