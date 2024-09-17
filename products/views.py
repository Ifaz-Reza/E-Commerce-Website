from .models import Product
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cs50 import SQL
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
import datetime

db = SQL("sqlite:///db.sqlite3")


def RegisterPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        date_joined = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            existing_user = db.execute("SELECT * FROM auth_user WHERE username = ?", username)
            if existing_user:
                messages.error(request, "Username already exists.")
                return redirect('register')

            db.execute("INSERT INTO auth_user (username, email, password, is_superuser, is_staff, is_active, date_joined, last_login, first_name, last_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", username, email, make_password(pass1), False, False, True, date_joined, None, '', '')
            messages.success(request, "Registration successful.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register')
        
    return render(request, 'signin.html')


def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Must provide username and password.")
            return redirect('login')

        user = db.execute("SELECT * FROM auth_user WHERE username = ?", username)

        if not user or not check_password(password, user[0]["password"]):
            messages.error(request, "Invalid username and/or password.")
            return redirect('login')

        user_obj = authenticate(request, username=username, password=password)
        if user_obj is not None:
            login(request, user_obj)
            messages.success(request, "Login successful.")
            return redirect('home')  # Redirect to the user homepage
        else:
            messages.error(request, "Authentication failed.")
            return redirect('login')
    else:
        return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    products = Product.objects.all()
    return render(request,'index.html', {'products': products})


@login_required(login_url='login')
def buy(request):
    if request.method=="POST":
        number = request.POST.get("cardnumber")
        card = request.POST.get("cardtype")

        num = int(str(number)[0:2])
        card_length = len(number)

        def check(x):
            sum = 0
            num_digits = len(str(x))
            parity = num_digits % 2
            for i, c in enumerate(str(x)):
                digit = int(c)
                if i % 2 == parity:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                sum += digit
            return sum % 10 == 0

        if ((num == 34 or num == 37) and card == 'amex' and card_length == 15) or (51 <= num <= 55 and card == 'mastercard' and card_length == 16) or (str(number)[0] == '4' and (card_length == 13 or card_length == 16) and card == "visa") and check(number):
            return HttpResponse("Success!! you will recieve a confirmation email if payment goes through.")
        else:
            return redirect("buy")
        
    return render(request, 'buy.html')

def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'details.html', {'product': product})


def new(request):
    return HttpResponse('New products')



@login_required(login_url='login')
def cart(request):
    return render(request, 'cart.html')
