from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase, Cart, CartItem
from .forms import CustomUserCreationForm


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        cart, created = Cart.objects.get_or_create(user_id=request.user.id)
        cart_item, item_created = CartItem.objects.get_or_create(cart_id=cart.id, product_id=product.id)
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('index')
    else:
        pass


@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'shop/view_cart.html', {'cart': cart, 'cart_items': cart_items})


def login_view(request):
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    return redirect('view_cart')


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
