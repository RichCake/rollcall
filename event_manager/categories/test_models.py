from django.test import TestCase

from categories.models import Category


class CategoryModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        category = Category.objects.create(name='Another Category')
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, 'Another Category')
