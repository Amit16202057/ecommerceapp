from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, CartItem, Order, DailyData, UserProfile
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer, DailyDataSerializer, UserProfileSerializer
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  # Redirect to the product list or another page
    else:
        form = UserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': form})


@login_required
def product_list(request):
    products = Product.objects.all()
    
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    return render(request, 'product_list.html', {'products':  products_page})
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# def product_list(request):
#     products = Product.objects.all()

#     paginator = Paginator(products, 12)  # Show 12 products per page
#     page = request.GET.get('page')
#     products_page = paginator.get_page(page)

#     return render(request, 'product_list.html', {'products': products_page})

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(detail=False, methods=['POST'])
    def checkout(self, request):
        user = self.request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total amount based on cart items
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create an order
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Associate cart items with the order and clear the cart
        order.cart_items.set(cart_items)
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class DailyDataViewSet(viewsets.ModelViewSet):
    queryset = DailyData.objects.all()
    serializer_class = DailyDataSerializer
