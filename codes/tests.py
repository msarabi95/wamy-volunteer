from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from codes.forms import CreateCodeForm, RedeemCodeForm
from codes.models import Category, Code
from teams.models import Event, Team


class CreateCodeFormTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.event = Event.objects.create(name="Test Event", team=self.team)

    def test_dynamic_fields(self):
        """
        Test dynamic field creation based on the categories present.
        The form should have a field for each category in the db.
        """
        # Sanity check
        self.assertEqual(Category.objects.count(), 0)

        # Without any categories, there should be no fields
        self.form = CreateCodeForm(self.event)
        self.assertEqual(len(self.form.fields), 0)

        # Add some categories and check
        Category.objects.create(name="Test Category 1", credit=1.5)
        self.form = CreateCodeForm(self.event)
        self.assertEqual(len(self.form.fields), 1)

        Category.objects.create(name="Test Category 2", credit=3)
        self.form = CreateCodeForm(self.event)
        self.assertEqual(len(self.form.fields), 2)

    def test_create_codes(self):
        """
        Test
        """
        # Sanity check
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Code.objects.count(), 0)

        # Create some categories
        Category.objects.bulk_create([
            Category(name="Test Category 1", credit=1),
            Category(name="Test Category 2", credit=1.5),
            Category(name="Test Category 3", credit=3),
        ])

        # Create a couple of codes from each category via the code creation form
        self.form = CreateCodeForm(self.event,
                                   {"category_1": 1,
                                    "category_2": 2,
                                    "category_3": 10})
        self.form.create_codes()

        self.assertEqual(Code.objects.filter(category__credit=1).count(), 1)
        self.assertEqual(Code.objects.filter(category__credit=1.5).count(), 2)
        self.assertEqual(Code.objects.filter(category__credit=3).count(), 10)
        

class RedeemCodeFormTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Test Team")
        self.event = Event.objects.create(name="Test Event", team=self.team)
        self.user = User.objects.create_user(username="test1", email="test@example.com", password="12345678")
        self.user2 = User.objects.create_user(username="test2", email="test@example.com", password="12345678")
        
        self.category = Category.objects.create(name="Test Category", credit=1)
        
        order_form = CreateCodeForm(self.event, {"category_1": 2})
        order_form.create_codes()
        
        self.code = Code.objects.first()
        self.code2 = Code.objects.last()
        
    def test_clean_string(self):
        
        # Try submitting an incorrect code
        self.form = RedeemCodeForm(self.user, {"string": self.code.string[::-1]})
        self.form.full_clean()
        self.assertIn('string', self.form.errors)

        # Try submitting an unavailable code
        self.code.user = self.user2
        self.code.save()

        self.form = RedeemCodeForm(self.user, {"string": self.code.string})
        self.form.full_clean()
        self.assertIn('string', self.form.errors)

        self.code.user = None
        self.code.save()

        # Try submitting a code while user has another code in the same event
        self.code2.user = self.user
        self.code2.save()

        self.form = RedeemCodeForm(self.user, {"string": self.code.string})
        self.form.is_valid()
        self.assertIn('string', self.form.errors)

        self.code2.user = None
        self.code2.save()

        # Try submitting code properly

        self.form = RedeemCodeForm(self.user, {"string": self.code.string})
        self.assertNotIn('string', self.form.errors)

    def test_process(self):

        # Try processing an incorrect code
        self.form = RedeemCodeForm(self.user, {"string": self.code.string[::-1]})
        self.form.process()