from django.test import TestCase
from shop.models import Product, Cart, Purchase, CartItem
from django.contrib.auth.models import User
from django.urls import reverse


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="book", price="740")
        Product.objects.create(name="pencil", price="50")

    def test_correctness_types(self):
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, int)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, int)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="book").price == 740)
        self.assertTrue(Product.objects.get(name="pencil").price == 50)


class CartTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', password='12345')
        Cart.objects.create(user=user)

    def test_cart_creation(self):
        user = User.objects.get(username='test_user')
        cart = Cart.objects.get(user=user)
        self.assertEqual(cart.user.username, 'test_user')


class PurchaseTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', password='12345')
        cart = Cart.objects.create(user=user)
        Purchase.objects.create(
            cart=cart, person='John Doe', address='123 Main St')

    def test_purchase_creation(self):
        purchase = Purchase.objects.get(person='John Doe')
        self.assertEqual(purchase.address, '123 Main St')


class CartItemTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user', password='12345')
        cart = Cart.objects.create(user=user)
        product = Product.objects.create(name='test_product', price=100)
        CartItem.objects.create(cart=cart, product=product, quantity=2)

    def test_cart_item_creation(self):
        cart_item = CartItem.objects.get(product__name='test_product')
        self.assertEqual(cart_item.quantity, 2)


class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='12345')
        self.client.login(username='test_user', password='12345')
        Cart.objects.create(user=self.user)
        Product.objects.create(name='test_product', price=100)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_view(self):
        product = Product.objects.get(name='test_product')
        response = self.client.post(
            reverse('add_to_cart', kwargs={'product_id': product.id}))
        # Перенаправление на index после добавления товара в корзину
        self.assertEqual(response.status_code, 302)

    def test_view_cart_view(self):
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        # Перенаправление на index после выхода из аккаунта
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_remove_from_cart_view(self):
        product = Product.objects.get(name='test_product')
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=1)
        response = self.client.get(
            reverse('remove_from_cart', kwargs={'item_id': cart_item.id}))
        # Перенаправление на view_cart после удаления товара из корзины
        self.assertEqual(response.status_code, 302)
