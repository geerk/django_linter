"""
Check transforms for factories
"""
import unittest
import factory
from django.db import models
from .models import Category


class Product(models.Model):
    name = models.CharField(max_length=33)

    def __unicode__(self):
        return self.name


class ProductFactory(factory.DjangoModelFactory):

    class Meta:
        model = Product



class ProductFactoryTestCase(unittest.TestCase):

    def test_product_factory(self):
        product = ProductFactory()
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, 'test_name')
        self.assertEqual(product.foobar, 'foobar')


class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Category


class CategoryFactoryTestCase(unittest.TestCase):

    def test_category_factory(self):
        category = CategoryFactory()
        self.assertEqual(category.id, 1)
        self.assertEqual(category.foobar, 'foobar')
