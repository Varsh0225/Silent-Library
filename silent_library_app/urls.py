from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.user_login,    name='home'),
    path('signup/',           views.signup,         name='signup'),
    path('thank-you/',        views.thank_you,      name='thank_you'),
    path('login/',            views.user_login,     name='login'),
    path('logout/',           views.user_logout,    name='logout'),
    path('dashboard/',        views.user_dashboard, name='user_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('profile/',          views.user_profile,   name='user_profile'),
    path('profile/update/',   views.update_profile, name='update_profile'),
    path('search/',           views.search_books,   name='search_books'),
    path('book/<int:book_id>/', views.book_detail,  name='book_detail'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('add-book/', views.add_book, name='add_book'),
    path('manage-books/', views.manage_books, name='manage_books'),
    path('edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
]





