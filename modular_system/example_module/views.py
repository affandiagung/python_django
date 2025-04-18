from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Product
from django.contrib.auth import logout
from module_engine.models import Module

def home(request):
    return render(request, 'example_module/home.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login') 
    else:
        return redirect('product_list')
def redirect_home(request):
    return redirect('product_list')  
def check_product_permission(user, action):
    return Product.check_permission(user, action)

@login_required(login_url='login')
def product_list(request):
    if not Module.objects.filter(name="example_module", installed=True).exists():
        return redirect('home')  
    
    if not check_product_permission(request.user, 'view'):
        return redirect('login')
    if not check_product_permission(request.user, 'view'):
        return redirect('login')
    
    products = Product.objects.all()
    return render(request, 'example_module/product_list.html', {'products': products})

@login_required(login_url='login')
def product_create(request):
    if not Product.check_permission(request.user, 'add'):
        return redirect('product_list')  
    
    if request.method == 'POST':
        name = request.POST.get('name')
        barcode = request.POST.get('barcode')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        
        if name and barcode and price and stock:
            product = Product.objects.create(
                name=name,
                barcode=barcode,
                price=price,
                stock=stock
            )
            return redirect('product_list')
        else:
            return render(request, 'example_module/product_form.html', {'error': 'All fields are required'})

    return render(request, 'example_module/product_form.html')


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.barcode = request.POST.get('barcode')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.save()
        return redirect('product_list')


    products = Product.objects.all()
    return render(request, 'example_module/product_list.html', {
        'products': products,
        'edit_product': product  
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if not check_product_permission(request.user, 'delete'):
        return redirect('product_list')
    
    if request.method == 'POST' and request.POST.get('confirm') == 'yes':
        product.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({
        'success': False,
        'message': 'Are you sure to delete this data?'
    }, status=400)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'example_module/product_detail.html', {'product': product})