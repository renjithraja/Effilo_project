

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import ProductForm
from .models import Product, UserProfile
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.shortcuts import render, redirect
from .models import UserProfile,Order
from .forms import UserProfileForm
from django.db.models import F



def adminpage(request):
    products_at_reorder_level = Product.objects.filter(quantity__lte=F('reorderlevel'))
    products = Product.objects.all()

    context = {
        'products_at_reorder_level': products_at_reorder_level,
        'productdata': products
    }
    
    return render(request, 'user.html', context)


def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                url='/adminpage'
                x=f'''
                    <script>
                        alert("wlecome admin");
                        window.location.href = "{url}"; 
                    </script>
                '''
                
                return HttpResponse(x)
        else:
            form = AuthenticationForm()  
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'admin_login.html', {'form': form, 'error_message': error_message})
    
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})


def user_register(request):
    registration_successful = False

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            registration_successful = True
            return redirect('user_login')
    else:
        form = UserCreationForm()

    return render(request, 'user_register.html', {'form': form, 'registration_successful': registration_successful})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    # Redirect to the index page after logout

    return redirect('index')

# @login_required
# def profile_update(request):
#     # Get the UserProfile object for the current user or create it if it doesn't exist
#     profile, created = UserProfile.objects.get_or_create(username=request.user)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile_update_success')  # Redirect to a success page
#     else:
#         form = UserProfileForm(instance=profile)
    
#     return render(request, 'profile_update.html', {'form': form})
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            user = form.save(commit=False)
            password = password_form.cleaned_data['new_password1']
            if password:
                user.password = make_password(password)  # Change password
            user.save()
            password_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_login')  # Redirect to the profile update page
    else:
        form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'profile_update.html', {'form': form, 'password_form': password_form})

def admin_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the form data including quantity and reorderlevel
            name = form.cleaned_data['name']
            brand = form.cleaned_data['brand']
            material= form.cleaned_data['material']
            Size = form.cleaned_data['Size']
            Sex = form.cleaned_data['Sex']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            quantity = form.cleaned_data['quantity']
            reorderlevel = form.cleaned_data['reorderlevel']

            # Create a new product instance
            new_product = Product.objects.create(
                name=name,
                brand=brand,
                material=material,
                Size=Size,
                Sex=Sex,
                description=description,
                price=price,
                image=image,
                quantity=quantity,
                reorderlevel=reorderlevel
            )
            # Save the new product to the database
            new_product.save()

            return redirect('adminpage')  # Redirect after adding a product
    else:
        form = ProductForm()

    return render(request, 'admin_add.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'product_list.html', {'products': products})

# def admin_add(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('adminpage')
#     else:
#         form = ProductForm()
#     return render(request, 'admin_add.html', {'form': form})



def index(request):   #user page product view
    products = Product.objects.all()
    return render(request, 'index.html', {'productdata': products})

from django.urls import reverse



def product_list(request): #admin page product view
    products = Product.objects.all()
    return render(request, 'user/user.html', {'product': products})


def edit_product(request, product_id):
    product_to_edit = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_to_edit)
        if form.is_valid():
            form.save()
            return redirect('adminpage')  # Redirect to the user page
    else:
        form = ProductForm(instance=product_to_edit)

    return render(request, 'edit_product.html', {'form': form, 'product': product_to_edit})



# def delete_product(request, product_id):
#     product_to_delete = get_object_or_404(Product, pk=product_id)  # Assuming product is the name of model

#     if request.method == 'POST':
#         confirmation = request.POST.get('confirmation', None)
#         if confirmation == 'confirmed':
#             #product_to_delete.is_active = False  # Set the product as inactive
#             product_to_delete.save()
#             return redirect('adminpage')  # Redirect to the user page after deletion
#         else:
#             return redirect('adminpage')  # Redirect without deleting if not confirmed

#     return render(request, 'confirmation_page.html', {'product': product_to_delete})
    


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query, is_active=True)
    return render(request, 'search_results.html', {'products': products, 'query': query})

def search_view(request):
    query = request.GET.get('query', '')  # Get the 'query' parameter from the request's GET parameters

    if query:
        # Perform a search using the query, ensuring it's not None
        products = Product.objects.filter(name__icontains=query)
    else:
        # Handle the case where 'query' is None or empty
        products = []

    context = {
        'query': query,
        'products': products,
    }

    return render(request, 'search_results.html', context)

#from requests import request






def checkout_view(request):
    cart_iteam=Cart.objects.filter(user=request.user)
    print(cart_iteam)
    total_amount=0
    for iteam in cart_iteam:
        total_amount+=iteam.quantity*iteam.product.price

    if request.method == 'POST':
        # Retrieve form data
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        # Construct redirect URL with parameters
        redirect_url = reverse('order_summary')
        params = {
            'fullname': fullname,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'total_amount': total_amount,
        }

        redirect_url += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
        return HttpResponse(pop_message(redirect_url,'checkout done'))
        
    return render(request, 'checkout.html', {'total_amount': total_amount})

from django.shortcuts import render, redirect
from .models import Cart, Order

def order_summary_view(request):
    # Retrieve order information from request parameters
    fullname = request.GET.get('fullname')
    address = request.GET.get('address')
    city = request.GET.get('city')
    postal_code = request.GET.get('postal_code')
    total_amount = request.GET.get('total_amount')

    # Create order instance
    order = Order.objects.create(
        user=request.user,
        fullname=fullname,
        address=address,
        city=city,
        postal_code=postal_code,
        total_amount=total_amount,
    )

    # Retrieve and move cart items to the order
    cart_items = Cart.objects.filter(user=request.user)
    for cart_item in cart_items:
        order.items.create(product=cart_item.product, quantity=cart_item.quantity)
        print(fullname, address, city, postal_code, total_amount)

        cart_item.delete()

    # Prepare context for rendering the order summary page
    context = {
        'fullname': fullname,
        'address': address,
        'city': city,
        'postal_code': postal_code,
        'total_amount': total_amount,
        'cart_products': order.items.all()  # Assuming you have a related_name 'items' for the OrderItem model
    }

    return render(request, 'order_summary.html', context)


from .models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url=user_login)
def add_to_cart(request, product_id):

    product = Product.objects.get(pk=product_id)
    # print(isinstance(request.user,UserProfile)
    if request.method=='POST':
        if product.quantity > 0:
            cart_item = Cart(user=request.user, product=product, quantity=1)  # Adjust quantity as needed
            cart_item.save()
            # Decrease product quantity by 1
            product.quantity -= 1
            product.save()
            # Redirect to the cart page or product detail page
            return redirect('cart')  # Redirect to cart page or wherever you manage cart items
        else:
            # Handle out of stock case
            return render(request, 'out_of_stock.html', {'product': product})

def decrease_to_cart(request, product_id):
    cart_items = Cart.objects.filter(product_id=product_id,user=request.user).first()
    print('============')
    print("items",cart_items)

    cart_items.delete()
    return redirect('cart')




def remove_from_cart(request, product_id):
    print('--------')
    cart_items = Cart.objects.filter(product_id=product_id,user=request.user).all()
    print('============')
    print("items",cart_items)
    cart_items.delete()
    return redirect('cart')



# def cart(request):
#     cart = request.session.get('cart', {})
#     product_ids = list(cart.keys())

#     cart_items = []
#     total_amount = 0

#     if product_ids:
#         cart_products = Product.objects.filter(id__in=product_ids)
#         for cart_product in cart_products:
#             quantity = cart.get(str(cart_product.id), 0)
#             if quantity > 0:
#                 item_total = quantity * cart_product.price
#                 total_amount += item_total
#                 cart_items.append({
#                     'product': cart_product,
#                     'quantity': quantity,
#                     'item_total': item_total,
#                 })
    

#     return render(request, 'cart.html', {'cart_products': cart_items, 'total_amount': total_amount})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product

@login_required
def cart(request):
    upcart_items = Cart.objects.filter(user=request.user)
    
    
    # <QuerySet [<Cart: Cart for alvin: Apple VX max>, <Cart: Cart for alvin: Apple VX max>]>
    cart_items={}
    for item in upcart_items:
        # print(item.product.name)
        
        if item.product.name in cart_items:
            cart_items[item.product.name]['quantity']+=1
            cart_items[item.product.name]['total_price']+=cart_items[item.product.name]['price']
            
        else:
            cart_items[item.product.name]={
                'id':item.product.id,
                'name':item.product.name,
                'price':item.product.price,
                'quantity':item.quantity,
                'price':item.product.price,
                'total_price':item.product.price,
                'image':item.product.image
            }
            # print(cart_items)

    total_price = sum(item['total_price'] for item in cart_items.values())

    
    context= {
        'cart_items': cart_items,
        'total_price': total_price
        }
    
    return render(request, 'cart.html',context)
 
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        # Handle adding product to cart
        if product.quantity > 0:
            # Decrement quantity and add to cart logic here
            product.quantity -= 1
            product.save()
            # Add to cart logic here
            return redirect('cart')  # Redirect to cart page after adding to cart
        else:
            # Product is out of stock, handle this case as needed
            return render(request, 'product_detail.html', {'product': product, 'message': 'Out of Stock'})
    else:
        return render(request, 'product_detail.html', {'product': product})
#wishlist
@login_required(login_url=user_login)
def add_to_wishlist(request, product_id):
    if 'wishlist' not in request.session:  
        request.session['wishlist'] = []  

    wishlist = request.session['wishlist'] 
    if product_id not in wishlist:  
        wishlist.append(product_id)
        request.session['wishlist'] = wishlist 
        message='Item added to your wishlist!'
    else:
        message='Item already in wishlist'

    url='/'
    return HttpResponse(pop_message(url,message))
#return HttpRespone
    
@login_required(login_url=user_login)
def remove_to_wishlist(request, product_id):
    wishlist = request.session['wishlist']   
    wishlist.remove(product_id)
    request.session['wishlist']=wishlist
    return redirect('index')





@login_required(login_url=user_login)
def view_to_wishlist(request):
    if 'wishlist' not in request.session:  
        context={
            'product':'',
        }
    else:
        wishlist = request.session['wishlist'] 
        data=Product.objects.filter(id__in=wishlist)
        
        context={
            'data':data
        }

    return render(request,'wishlist.html',context)



#custom popup message

def pop_message(url,message):
    url=url
    x=f'''
        <script>
            alert("{message}");
            window.location.href = "{url}"; 
        </script>
    '''
    return(x)



@login_required
def admin_order_view(request):
    # Admin view to display all orders
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)

@login_required
def order_detail_view(request, order_id):
    # Admin view to display order details
    order = Order.objects.get(id=order_id)
    items = order.items.all()
    context = {'order': order, 'items': items}
    return render(request, 'order_detail.html', context)

@login_required
def update_status(request, order_id):
    # Update order status view
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
    return redirect('order_list_and_detail')  # Redirect to orders list
def order_list_and_detail(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)

@login_required
def user_order_view(request):
    # Admin view to display all orders
    orders = Order.objects.filter(user=request.user).all()
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)

def delete_product(request, product_id):
    # Retrieve the product instance to delete
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        # Delete the product from the database
        product.delete()
        return redirect('adminpage')  # Redirect after deleting a product

    return render(request, 'confirmation_page.html', {'product': product})