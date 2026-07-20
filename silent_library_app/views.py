from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, Book
from .models import Book, Borrow



# ──────────────────────────────────────────
#  SIGNUP
# ──────────────────────────────────────────
def signup(request):
        
    if request.method == 'POST':
        username        = request.POST.get('username', '').strip()
        first_name      = request.POST.get('first_name', '').strip()
        last_name       = request.POST.get('last_name', '').strip()
        email           = request.POST.get('email', '').strip()
        password        = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        profile_pic     = request.FILES.get('profile_pic')



        # --- Validations ---
        if not username or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'signup.html')

        # --- Create User ---
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # --- Create UserProfile ---
        user_profile = UserProfile.objects.create(user=user)
        if profile_pic:
            user_profile.profile_pic = profile_pic
            user_profile.save()

        # --- Send Confirmation Email ---
        try:
            send_mail(
                subject='Welcome to Silent Library!',
                message=(
                    f'Hi {first_name},\n\n'
                    f'Thank you for registering at Silent Library!\n\n'
                    f'Your account has been successfully created.\n'
                    f'Username: {username}\n\n'
                    f'Happy Reading!\n'
                    f'Silent Library Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email error: {e}")

        messages.success(request, 'Registration successful! Check your email.')
        return redirect('thank_you')

    return render(request, 'signup.html')
   

# ──────────────────────────────────────────
#  THANK YOU
# ──────────────────────────────────────────
def thank_you(request):
    return render(request, 'thank_you.html')


# ──────────────────────────────────────────
#  LOGIN
# ──────────────────────────────────────────
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

         # ✅ Validation
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'user_login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅SUPER ADMIN → Django admin panel
            if user.is_superuser:
                return redirect('/admin/')
            
            # ✅ STAFF USER → custom staff dashboard
            elif user.is_staff:
                return redirect('staff_dashboard')
            
            # ✅ NORMAL USER → user dashboard
            else:
                return redirect('user_dashboard')

                                 
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'user_login.html')

    return render(request, 'user_login.html')


# ──────────────────────────────────────────
#  LOGOUT
# ──────────────────────────────────────────

def user_logout(request):
    if request.method == 'POST':
        # messages.success(request, 'You have been logged out successfully.')
        logout(request)
        return render('login')
         
    
    if request.user.is_superuser:
        return redirect('/admin/')
    elif request.user.is_staff:
        return redirect('staff_dashboard')
    else:
        return redirect('user_dashboard')
    

# ──────────────────────────────────────────
#  DASHBOARD
# ──────────────────────────────────────────
@login_required(login_url='/login/')
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


# ──────────────────────────────────────────
#  USER PROFILE
# ──────────────────────────────────────────
@login_required(login_url='/login/')
def user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    return render(request, 'userProfile.html', {'profile': profile})


# ──────────────────────────────────────────
#  UPDATE PROFILE
# ──────────────────────────────────────────
@login_required(login_url='/login/')
def update_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        first_name  = request.POST.get('first_name', '').strip()
        last_name   = request.POST.get('last_name', '').strip()
        email       = request.POST.get('email', '').strip()
        bio         = request.POST.get('bio', '').strip()
        profile_pic = request.FILES.get('profile_pic')

        if not first_name or not last_name or not email:
            messages.error(request, 'First name, last name, and email are required.')
            return render(request, 'updateProfile.html', {'profile': user_profile})

        if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            messages.error(request, 'This email is already used by another account.')
            return render(request, 'updateProfile.html', {'profile': user_profile})

        # Update User
        request.user.first_name = first_name
        request.user.last_name  = last_name
        request.user.email      = email
        request.user.save()

        # Update Profile
        user_profile.bio = bio
        if profile_pic:
            user_profile.profile_pic = profile_pic
        user_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    return render(request, 'updateProfile.html', {'profile': user_profile})


# ──────────────────────────────────────────
#  SEARCH BOOKS
# ──────────────────────────────────────────
def search_books(request):
    query  = request.GET.get('q', '').strip()
    genre  = request.GET.get('genre', '').strip()
    author = request.GET.get('author', '').strip()
    books  = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query)
    if genre:
        books = books.filter(genre__icontains=genre)
    if author:
        books = books.filter(author__icontains=author)

    context = {
        'books':  books,
        'query':  query,
        'genre':  genre,
        'author': author,
    }
    return render(request, 'search.html', context)


# ──────────────────────────────────────────
#  BOOK DETAIL
# ──────────────────────────────────────────
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_detail.html', {'book': book})


# ──────────────────────────────────────────
#  BORROW VIEW
# ──────────────────────────────────────────

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.available:
        Borrow.objects.create(user=request.user, book=book)

        # mark book unavailable
        book.available = False
        book.save()

        messages.success(request, f'"{book.title}" borrowed successfully!')
    else:
        messages.error(request, "Book is not available")

    return redirect('user_dashboard')


# ──────────────────────────────────────────
#  STAFF DASHBOARD
# ──────────────────────────────────────────
@login_required(login_url='/login/')
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

# ──────────────────────────────────────────
#  ADD BOOK
# ──────────────────────────────────────────

@login_required
def add_book(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        isbn = request.POST.get('isbn')
        published_date = request.POST.get('published_date')
        cover_image = request.FILES.get('cover_image')

        Book.objects.create(
            title=title,
            author=author,
            genre=genre,
            description=description,
            isbn=isbn,
            published_date=published_date,
            cover_image=cover_image
        )

        messages.success(request, f'"{title}" added successfully!')
        return redirect('manage_books')

    return render(request, 'add_book.html')

# ──────────────────────────────────────────
#  VIEW ALL BOOKS (MANAGE BOOK)
# ──────────────────────────────────────────
@login_required
def manage_books(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    query = request.GET.get('q', '').strip()
    books = Book.objects.all()

    if query:
        books = books.filter(
            title__icontains=query
        ) | books.filter(
            author__icontains=query
        ) | books.filter(
            genre__icontains=query
        ) | books.filter(
            isbn__icontains=query
        )

    return render(request, 'manage_books.html', {
        'books': books,
        'query': query
    })

# ──────────────────────────────────────────
#  EDIT BOOKS
# ──────────────────────────────────────────
@login_required
def edit_book(request, book_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.genre = request.POST.get('genre')
        book.description = request.POST.get('description')
        book.isbn = request.POST.get('isbn')
        book.published_date = request.POST.get('published_date')

        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES.get('cover_image')

        book.save()

        messages.success(request, f'"{book.title}" has been updated successfully!')
        return redirect('manage_books')

    return render(request, 'edit_book.html', {'book': book})

# ──────────────────────────────────────────
#  DELETE BOOKS
# ──────────────────────────────────────────
@login_required
def delete_book(request, book_id):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        deleted_title = book.title
        book.delete()
        messages.success(request, f'"{deleted_title}" has been deleted successfully!')
        return redirect('manage_books')

    return render(request, 'delete_book.html', {'book': book})




