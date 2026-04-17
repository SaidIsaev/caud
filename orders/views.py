from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet
from products.views import get_user_role


def order_list(request):
    user_role = get_user_role(request.user) if request.user.is_authenticated else 'guest'
    
    if user_role in ['client', 'manager', 'admin']:
        if user_role == 'client':
            orders = Order.objects.filter(user=request.user)
        else:
            orders = Order.objects.all()
        
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
            'user_role': user_role,
        }
        return render(request, 'orders/order_list.html', context)
    else:
        messages.warning(request, 'У вас нет прав для просмотра заказов.')
        return redirect('products:product_list')


@login_required
def order_create(request):
    user_role = get_user_role(request.user)
    if user_role not in ['client', 'admin']:
        messages.error(request, 'У вас нет прав для создания заказа.')
        return redirect('products:product_list')

    if request.method == 'POST':
        formset = OrderItemFormSet(request.POST)
        if formset.is_valid():
            order = Order(user=request.user, status='pending')
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, 'Заказ успешно создан.')
            return redirect('orders:order_list')
    else:
        formset = OrderItemFormSet()

    return render(request, 'orders/order_form.html', {
        'formset': formset,
        'title': 'Создать заказ',
        'user_role': user_role,
    })


@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    user_role = get_user_role(request.user)
    
    can_edit = (user_role == 'client' and order.user == request.user) or user_role in ['manager', 'admin']
    if not can_edit:
        messages.error(request, 'У вас нет прав для редактирования этого заказа.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Заказ успешно обновлен.')
            return redirect('orders:order_list')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Редактировать заказ',
        'order': order,
        'user_role': user_role,
    })


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    user_role = get_user_role(request.user)
    
    can_delete = (user_role == 'client' and order.user == request.user) or user_role in ['manager', 'admin']
    if not can_delete:
        messages.error(request, 'У вас нет прав для удаления этого заказа.')
        return redirect('orders:order_list')

    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Заказ успешно удален.')
        return redirect('orders:order_list')

    return render(request, 'orders/order_confirm_delete.html', {
        'order': order,
        'user_role': user_role,
    })

