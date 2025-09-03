# shop/views.py
from django.shortcuts import render
from .models import Product

def home(request):
    # All products (optional)
    products = Product.objects.all()

    # Back to School products
    back_to_school_products = Product.objects.filter(
        name__in=["Pencil", "Pencil Sketch", "Diary"]
    )

    # Pass to template
    return render(request, 'home.html', {
        'products': products,
        'back_to_school_products': back_to_school_products
    })


def shop(request):
    return render(request, "shop.html")

def about(request):
    return render(request, "about.html")

from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})



from django.shortcuts import render
from shop.models import Category, Product
from django.db.models import Q
from django.http import HttpResponse 

def shop(request):
    office_category = Category.objects.filter(slug="office").first()
    products = Product.objects.filter(category=office_category)

    # Get price ranges from GET parameters (can be multiple)
    price_ranges = request.GET.getlist('price')  # e.g., ["50-100", "200-300"]

    if price_ranges:
        q = Q()
        for r in price_ranges:
            min_price, max_price = map(int, r.split('-'))
            q |= Q(price__gte=min_price, price__lte=max_price)
        products = products.filter(q)

    context = {
        'products': products,
        'category_name': office_category.name if office_category else "Office",
    }

    # For AJAX request, return only product grid HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = ""
        for product in products:
            html += f"""
            <div class="col-12 col-md-4 d-flex">
                <div class="card flex-fill shadow-sm rounded-4" style="background-color:#78b2f9;">
                    {'<img src="' + product.image.url + '" class="card-img-top rounded-xl" alt="' + product.name + '">' if product.image else ''}
                    <div class="card-body text-center text-dark">
                        <h5 class="card-title mb-1">{product.name}</h5>
                        <p class="mb-1">Rs. {product.price}</p>
                        <p class="card-text mb-3">{product.bulk_price_info}</p>
                        <a href="#" class="btn btn-primary fw-bold rounded-2">Add to Cart</a>
                    </div>
                </div>
            </div>
            """
        if not products:
            html = '<p class="col-12 text-center text-muted">No products available in this category.</p>'
        return HttpResponse(html)

    return render(request, 'shop.html', context)

from django.shortcuts import render
from shop.models import Category, Product
from django.db.models import Q
from django.http import HttpResponse 

def files(request):
    # Get the "Files & Folders" category
    files_category = Category.objects.filter(name="Files & Folders").first()
    if not files_category:
        return render(request, 'files.html', {'products': [], 'category_name': "Files & Folders"})

    # Start with all products in the "Files & Folders" category
    products = Product.objects.filter(category=files_category)

    # Get price ranges from GET parameters (can be multiple)
    price_ranges = request.GET.getlist('price')  # e.g., ["50-100", "200-300"]

    if price_ranges:
        q = Q()
        for r in price_ranges:
            try:
                min_price, max_price = map(int, r.split('-'))
                q |= Q(price__gte=min_price, price__lte=max_price)
            except ValueError:
                continue  # skip invalid ranges
        products = products.filter(q)

    context = {
        'products': products,
        'category_name': files_category.name,
    }

    # For AJAX requests, return only the product grid HTML
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = ""
        for product in products:
            html += f"""
            <div class="col-12 col-md-4 d-flex">
                <div class="card flex-fill shadow-sm rounded-4" style="background-color:#78b2f9;">
                    {'<img src="' + product.image.url + '" class="card-img-top rounded-xl" alt="' + product.name + '">' if product.image else ''}
                    <div class="card-body text-center text-dark">
                        <h5 class="card-title mb-1">{product.name}</h5>
                        <p class="mb-1">Rs. {product.price}</p>
                        <p class="card-text mb-3">{product.bulk_price_info}</p>
                        <a href="#" class="btn btn-primary fw-bold rounded-2">Add to Cart</a>
                    </div>
                </div>
            </div>
            """
        if not products:
            html = '<p class="col-12 text-center text-muted">No products available in this category.</p>'
        return HttpResponse(html)

    return render(request, 'files.html', context)

from django.shortcuts import render
from shop.models import Category, Product
from django.db.models import Q
from django.http import HttpResponse 

def paper(request):
    # Get the "Paper & Notebooks" category
    paper_category = Category.objects.filter(name="Paper & Notebooks").first()
    if not paper_category:
        return render(request, 'paper.html', {'products': [], 'category_name': "Paper & Notebooks"})

    # Get all products in this category
    products = Product.objects.filter(category=paper_category)

    # Price filter
    price_ranges = request.GET.getlist('price')
    if price_ranges:
        q = Q()
        for r in price_ranges:
            try:
                min_price, max_price = map(int, r.split('-'))
                q |= Q(price__gte=min_price, price__lte=max_price)
            except ValueError:
                continue
        products = products.filter(q)

    # Context
    context = {
        'products': products,
        'category_name': paper_category.name,
    }

    # AJAX response for filtered products
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = ""
        for product in products:
            html += f"""
            <div class="col-12 col-md-4 d-flex">
                <div class="card flex-fill shadow-sm rounded-4" style="background-color:#78b2f9;">
                    {'<img src="' + product.image.url + '" class="card-img-top rounded-xl" alt="' + product.name + '">' if product.image else ''}
                    <div class="card-body text-center text-dark">
                        <h5 class="card-title mb-1">{product.name}</h5>
                        <p class="mb-1">Rs. {product.price}</p>
                        <p class="card-text mb-3">{product.bulk_price_info}</p>
                        <a href="#" class="btn btn-primary fw-bold rounded-2">Add to Cart</a>
                    </div>
                </div>
            </div>
            """
        if not products:
            html = '<p class="col-12 text-center text-muted">No products available in this category.</p>'
        return HttpResponse(html)

    # Render template
    return render(request, 'paper.html', context)


from django.shortcuts import render
from shop.models import Category, Product
from django.db.models import Q
from django.http import HttpResponse

def pens(request):
    pens_category = Category.objects.filter(name="Pens & Writing").first()
    if not pens_category:
        return render(request, 'pens.html', {'products': [], 'category_name': "Pens & Writing"})

    products = Product.objects.filter(category=pens_category)

    # Price filter
    price_ranges = request.GET.getlist('price')
    if price_ranges:
        q = Q()
        for r in price_ranges:
            try:
                min_price, max_price = map(int, r.split('-'))
                q |= Q(price__gte=min_price, price__lte=max_price)
            except ValueError:
                continue
        products = products.filter(q)

    context = {
        'products': products,
        'category_name': pens_category.name,
    }

    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = ""
        for product in products:
            html += f"""
            <div class="col-12 col-md-4 d-flex">
                <div class="card flex-fill shadow-sm rounded-4" style="background-color:#78b2f9;">
                    {'<img src="' + product.image.url + '" class="card-img-top rounded-xl" alt="' + product.name + '">' if product.image else ''}
                    <div class="card-body text-center text-dark">
                        <h5 class="card-title mb-1">{product.name}</h5>
                        <p class="mb-1">Rs. {product.price}</p>
                        <p class="card-text mb-3">{product.bulk_price_info}</p>
                        <a href="#" class="btn btn-primary fw-bold rounded-2">Add to Cart</a>
                    </div>
                </div>
            </div>
            """
        if not products:
            html = '<p class="col-12 text-center text-muted">No products available in this category.</p>'
        return HttpResponse(html)

    return render(request, 'pens.html', context)


from django.shortcuts import render
from shop.models import Category, Product
from django.db.models import Q
from django.http import HttpResponse

def school(request):
    school_category = Category.objects.filter(name="School Supplies").first()
    if not school_category:
        return render(request, 'school.html', {'products': [], 'category_name': "School Supplies"})

    products = Product.objects.filter(category=school_category)

    # Price filter
    price_ranges = request.GET.getlist('price')
    if price_ranges:
        q = Q()
        for r in price_ranges:
            try:
                min_price, max_price = map(int, r.split('-'))
                q |= Q(price__gte=min_price, price__lte=max_price)
            except ValueError:
                continue
        products = products.filter(q)

    context = {
        'products': products,
        'category_name': school_category.name,
    }

    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = ""
        for product in products:
            html += f"""
            <div class="col-12 col-md-4 d-flex">
                <div class="card flex-fill shadow-sm rounded-4" style="background-color:#78b2f9;">
                    {'<img src="' + product.image.url + '" class="card-img-top rounded-xl" alt="' + product.name + '">' if product.image else ''}
                    <div class="card-body text-center text-dark">
                        <h5 class="card-title mb-1">{product.name}</h5>
                        <p class="mb-1">Rs. {product.price}</p>
                        <p class="card-text mb-3">{product.bulk_price_info}</p>
                        <a href="#" class="btn btn-primary fw-bold rounded-2">Add to Cart</a>
                    </div>
                </div>
            </div>
            """
        if not products:
            html = '<p class="col-12 text-center text-muted">No products available in this category.</p>'
        return HttpResponse(html)

    return render(request, 'school.html', context)
# 
# 
# payment
# shop/views.py (Payment/Checkout related)

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product

# Checkout / Payment Page
# def payment(request):
#     cart = request.session.get('cart', {})
#     cart_items = []
#     subtotal = 0

#     for pid, item in cart.items():
#         total_price = item['price'] * item['quantity']
#         subtotal += total_price
#         cart_items.append({
#             'id': pid,
#             'name': item['name'],
#             'price': item['price'],
#             'quantity': item['quantity'],
#             'image': item['image'],
#             'total': total_price,
#         })

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#     }
#     return render(request, 'payment.html', context)

# # Place Order (simulate order placement)
# def place_order(request):
#     if request.method == "POST":
#         # Here you would typically save the order to the database
#         # For now, we just clear the cart
#         request.session['cart'] = {}
#         request.session.modified = True
#         return JsonResponse({'success': True, 'message': "Order placed successfully"})
#     return JsonResponse({'success': False, 'message': "Invalid request"})

# cart

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from shop.models import Product

# Add to Cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        cart[str(product.id)]['quantity'] += 1
    else:
        cart[str(product.id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else ''
        }

    request.session['cart'] = cart
    request.session.modified = True

    return JsonResponse({'success': True, 'message': f'"{product.name}" added to cart'})

# Cart Page
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = 0

    for pid, item in cart.items():
        total_price = item['price'] * item['quantity']
        subtotal += total_price
        cart_items.append({
            'id': pid,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'total': total_price,
        })

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }
    return render(request, 'cart.html', context)

# Update Cart
def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    pid = str(product.id)

    if pid in cart:
        if action == 'increment':
            cart[pid]['quantity'] += 1
        elif action == 'decrement':
            cart[pid]['quantity'] -= 1
            if cart[pid]['quantity'] <= 0:
                del cart[pid]

    request.session['cart'] = cart
    request.session.modified = True

    item_total = cart[pid]['quantity'] * cart[pid]['price'] if pid in cart else 0
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    total_items = sum(item['quantity'] for item in cart.values())

    return JsonResponse({
        'success': True,
        'quantity': cart[pid]['quantity'] if pid in cart else 0,
        'item_total': item_total,
        'subtotal': subtotal,
        'total_items': total_items
    })

# Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        request.session['cart'] = cart
        request.session.modified = True

    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())

    return JsonResponse({'success': True, 'subtotal': subtotal})


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json

# Normal auth page (login/register)
def auth_view(request):
    next_url = request.GET.get("next") or "/"

    if request.method == "POST":
        # LOGIN
        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password")

        # REGISTER
        elif "register" in request.POST:
            username = request.POST.get("reg_username")
            email = request.POST.get("reg_email")
            password = request.POST.get("reg_password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)  # auto login after register
                messages.success(request, "Account created successfully!")
                return redirect(next_url)

    return render(request, "auth.html")


# ---------------------------
# AJAX / API login and register
# ---------------------------

@csrf_protect
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # login immediately after registration
        return JsonResponse({"message": "Registration successful!", "username": user.username})

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_protect
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful!", "username": user.username})
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Logged out"})

from django.http import JsonResponse

def check_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"logged_in": True, "username": request.user.username})
    return JsonResponse({"logged_in": False})


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order, OrderItem, Product

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return render(request, 'cart.html', {'cart_items': [], 'subtotal': 0})

    cart_items = []
    subtotal = 0
    for pid, item in cart.items():
        total_price = item['price'] * item['quantity']
        subtotal += total_price
        cart_items.append({
            'id': pid,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'total': total_price,
        })

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }
    return render(request, 'payment.html', context)


from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def place_order(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        name = data.get('name')
        street = data.get('street')
        city = data.get('city')
        postal_code = data.get('postal_code')
        payment_mode = data.get('payment_mode')

        cart = request.session.get('cart', {})
        if not cart:
            return JsonResponse({'success': False, 'message': 'Your cart is empty.'})

        if not all([name, street, city, postal_code, payment_mode]):
            return JsonResponse({'success': False, 'message': 'Please fill all fields.'})

        subtotal = sum(item['price'] * item['quantity'] for item in cart.values())

        # Assign the logged-in user
        order = Order.objects.create(
            user=request.user,  # ✅ Add this line
            total_amount=subtotal,
            payment_mode=payment_mode
        )

        # Create Order Items
        for pid, item in cart.items():
            product = Product.objects.get(id=int(pid))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear session cart
        request.session['cart'] = {}
        request.session.modified = True

        return JsonResponse({'success': True, 'message': 'Order placed successfully!', 'total_amount': subtotal})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
# orders
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def my_orders(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'myorder.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'myorder.html', {'orders': orders})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from datetime import timedelta

@login_required
def track_order(request, order_id):
    # Fetch the order for the logged-in user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()  # all products in this order

    # Example: tracking status
    tracking_status = 'shipped'  # you can replace this with a field in Order later
    delivery_date = items[0].delivery_date if items.exists() else order.created_at + timedelta(days=7)

    context = {
        'order': order,
        'items': items,
        'tracking_status': tracking_status,
        'delivery_date': delivery_date,
    }

    return render(request, 'track.html', context)
from django.shortcuts import render, get_object_or_404
from .models import Product  # Make sure you have a Product model

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

from django.shortcuts import render
from .models import Product   # make sure your Product model exists

def search_products(request):
    query = request.GET.get("q")
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, "search_results.html", {
        "products": products,
        "query": query
    })
from django.shortcuts import render

def search_redirect(request):
    query = request.GET.get("q", "").lower().strip()  # get the search term

    # Map search keywords to templates
    if "pen" in query:
        return render(request, "pens.html")
    elif "shop" in query:
        return render(request, "shop.html")
    elif "school" in query:
        return render(request, "school.html")
    elif "paper" in query:
        return render(request, "paper.html")
    elif "file" in query or "files" in query:
        return render(request, "files.html")
    else:
        # fallback page if no match found
        return render(request, "search_results.html", {"query": query})
