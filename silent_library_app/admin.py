from django.contrib import admin
from .models import UserProfile, Book, Borrow


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'isbn', 'available', 'cover_preview']
    search_fields = ['title', 'author', 'genre', 'isbn']
    list_filter = ['genre', 'available']

    def cover_preview(self, obj):
        if obj.cover_image:
            return "Yes"
        return "No"

    cover_preview.short_description = "Cover Image"

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'due_date', 'returned')
    list_filter = ('returned', 'borrowed_date')
    search_fields = ('user__username', 'book__title')
