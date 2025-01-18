from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .form import OrderForm, CreateCustomer, addProduts
# Create your views here.


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, username + ' welcome back !')
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect !')

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers,'total_customers':total_customers,'total_orders':total_orders, 'delivered':delivered, 'pending':pending}

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(reuqest):
    products = Product.objects.all()
    return render(reuqest, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
def customer(request):
   # Fetch all customers and orders
    customers = Customer.objects.all()
    orders = Order.objects.all()

    # Total number of customers and orders
    total_customer = customers.count()
    total_orders = orders.count()
    
    # Count the number of orders for each customer
    customers_with_order_count = Customer.objects.annotate(order_count=Count('order'))

    # Debugging: Print the queryset to the console
    #print("Total Customers:", total_customer)
    #print("Customers with Order Count:", customers_with_order_count)

    # Count customers created this month
    now = timezone.now()
    start_of_month = now.replace(day=1)
    customer_count = Customer.objects.filter(date_created__gte=start_of_month).count()

    # Count the number of returning customers
    returning_customers = Customer.objects.annotate(order_count=Count('order')).filter(order_count__gt=1).count()

    context = {
        'total_customer': total_customer,
        'customer_count': customer_count,
        'returning_customers': returning_customers,
        'total_orders': total_orders,
        'customers': customers_with_order_count, # Key for customers  
    }

    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def createOrder(request):

    form = OrderForm()
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)  # Get the specific order
    form = OrderForm(instance=order)  # Pass the order instance to the form

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # Update the order with the new data
        if form.is_valid():
            form.save()  # Save the updated order
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
def create_Customer(request):
    form = CreateCustomer()
    if request.method == 'POST':
        form = CreateCustomer(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer')
    context = {'form':form} 
    return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CreateCustomer(instance=customer)
    if request.method == 'POST':
        form = CreateCustomer(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer')

    context = {'form': form}
    return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer')
    
    context = {'customer':customer}
    return render(request, 'accounts/delete_customer.html', context)

@login_required(login_url='login')
def add_product(request):
    form = addProduts()
    if request.method == 'POST':
        form = addProduts(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    context = {'form':form}
    return render(request, 'accounts/add_products.html', context)

@login_required(login_url='login')
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    form = addProduts(instance=product)
    if request.method == 'POST':
        form = addProduts(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    context = {'form':form}
    return render(request, 'accounts/add_products.html', context)

@login_required(login_url='login')
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    context = {'product':product}
    return render(request, 'accounts/delete_product.html', context)

@login_required(login_url='login')
def search_products(request):
    query = request.GET.get('q1')  # get the query from the search input field (name="q")
    if query:
        products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, 'accounts/products.html', {'products': products, 'query': query})

@login_required(login_url='login')
def search_customer(request):
    query = request.GET.get('q')
    if query:
        customers = Customer.objects.filter(name__icontains=query)
    else:
        customers = Customer.objects.all()
    
    context = {'customers': customers}
    return render(request, 'accounts/customer.html', context)