from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('order_list')
        else:
            # Add error message if the form is invalid
            messages.error(request, "Invalid username or password. Please try again.")
     # Replace 'home' with your desired redirect URL
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def role_required(*allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_roles = [group.name for group in request.user.groups.all()]
            if not any(role in allowed_roles for role in user_roles):
                raise PermissionDenied("You do not have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Order List View with Search and Pagination (accessible by Sales)
@role_required('Salespersons' ,'Production')
def order_list(request):
    query = request.GET.get('q', '')
    orders = Order.objects.all()
    
    if query:
        orders = orders.filter(
            Q(order_id__icontains=query) |
            Q(company_name__icontains=query) |
            Q(client_name__icontains=query) |
            Q(salesperson_name__icontains=query) |
            Q(product_list__icontains=query) |
            Q(progress__icontains=query)
        )
    
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    user_groups = [group.name for group in request.user.groups.all()]
    return render(request, 'orders/order_list.html', {'user_groups': user_groups, 'orders': orders})



# Order Form View (Create New Order)
@role_required('Salespersons')
  # Allow only Sales to create orders
def order_form(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

# Edit Order View (Editable by Sales and Accounts)
@login_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    user = request.user

    # Check if the user is in the Salespersons group
    user_in_salespersons = user.groups.filter(name='Salespersons').exists()

    if request.method == 'POST':
        if user.is_superuser or user_in_salespersons:
            # Superusers and Salespersons can edit all fields
            form = OrderForm(request.POST, request.FILES, instance=order)
            if form.is_valid():
                form.save()
                return redirect('order_list')
        else:
            # Other users can only edit remark and progress
            form = OrderForm(instance=order)  # Load the form with the current order instance
            if 'remark' in request.POST and 'progress' in request.POST:
                order.remark = request.POST['remark']
                order.progress = request.POST['progress']
                order.save()
                return redirect('order_list')
    else:
        # Pre-fill the form
        form = OrderForm(instance=order)

    return render(
        request, 
        'orders/edit_order.html', 
        {'form': form, 'order': order, 'user_in_salespersons': user_in_salespersons}
    )
# Delete Order View (Accessible by Admin only)
@role_required('Salespersons')
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')  # Redirect to the history page after deleting
    return render(request, 'orders/delete_order.html', {'order': order})


@csrf_exempt  # Allows CSRF bypass if needed (use only if necessary)
def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':  # Handle both methods
        logout(request)
        return redirect('/')  # Redirect to the home page after logout
    return redirect('login')  # Redirect to login if method is invalid