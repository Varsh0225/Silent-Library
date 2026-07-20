from django.test import TestCase
from .models import UserProfile, Book, Borrow
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from datetime import timedelta

# ✅ TEST 1 — Book Creation
class BookTest(TestCase):
    def test_book_creation(self):
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre='fiction',
            description='Sample Description',
            isbn='9781234567890',
            published_date=date(2020, 1, 1),
            available=True
        )
        self.assertEqual(book.title, 'Test Book')


# ✅ TEST 2 — UserProfile Creation
class UserProfileTest(TestCase):
    def test_userprofile_creation(self):
        user = User.objects.create_user(username='vijay', password='12345')
        profile = UserProfile.objects.create(user=user, bio='Library User')
        self.assertEqual(profile.user.username, 'vijay')


# ✅ TEST 3 — Borrow Record Creation
class BorrowTest(TestCase):
    def test_borrow_creation(self):
        user = User.objects.create_user(username='john', password='12345')

        book = Book.objects.create(
            title='Borrow Book',
            author='Author',
            genre='science',
            description='Borrow Description',
            isbn='9781111111111',
            published_date=date(2021, 5, 5),
            available=True
        )

        borrow = Borrow.objects.create(user=user, book=book)
        self.assertEqual(borrow.book.title, 'Borrow Book')


# ✅ TEST 4 — Due Date Auto Set
class BorrowDueDateTest(TestCase):
    def test_due_date_auto_generated(self):
        user = User.objects.create_user(username='alex', password='12345')

        book = Book.objects.create(
            title='Due Date Book',
            author='Author2',
            genre='history',
            description='History Description',
            isbn='9782222222222',
            published_date=date(2022, 2, 2),
            available=True
        )

        borrow = Borrow.objects.create(user=user, book=book)

        self.assertIsNotNone(borrow.due_date)

# ✅ TEST 5 — Book Availability Default
class BookAvailabilityTest(TestCase):
    def test_book_default_available(self):
        book = Book.objects.create(
            title='Available Book',
            author='Author3',
            genre='technology',
            description='Tech Description',
            isbn='9783333333333',
            published_date=date(2023, 3, 3)
        )

        self.assertEqual(book.available, True)