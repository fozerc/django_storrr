from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from shop_app.forms import RegisterForm, PurchaseForm, ReturnForm
from shop_app.mixins import SuperUserRequiredMixin
from shop_app.models import Product, Purchase, Return


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    queryset = Product.objects.all()
    extra_context = {'form': PurchaseForm}


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        result = super().form_valid(form=form)
        login(self.request, self.object)
        return result


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    queryset = Product.objects.all()
    form_class = PurchaseForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        purchase = form.save(commit=False)
        user = self.request.user
        product = form.product
        purchase.user = user
        purchase.product = product
        product.amount -= purchase.quantity
        user.user_wallet -= purchase.quantity * product.price
        with transaction.atomic():
            product.save()
            purchase.save()
            user.save()
            return super().form_valid(form=form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('index'))


class ProfileListView(LoginRequiredMixin, ListView):
    model = 'ProfileListView'
    template_name = 'profile.html'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


class ReturnCreateView(LoginRequiredMixin, CreateView):
    form_class = ReturnForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        ret = form.save(commit=False)
        ret.purchase = form.purchase
        ret.save()
        return super().form_valid(form=form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('profile'))
    
    
class ReturnApproveDeleteView(SuperUserRequiredMixin, LoginRequiredMixin, DeleteView):
    queryset = Return.objects.all()
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        ret = self.object
        product = ret.purchase.product
        user = ret.purchase.user
        product.amount += ret.purchase.quantity
        user.user_wallet += ret.purchase.quantity * product.price
        with transaction.atomic():
            user.save()
            product.save()
            return super().form_valid(form=form)


class ReturnDeclineDeleteView(SuperUserRequiredMixin, LoginRequiredMixin, DeleteView):
    queryset = Return.objects.all()
    success_url = reverse_lazy('index')
    

class ProductCreateView(SuperUserRequiredMixin, LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'create_product.html'
    success_url = reverse_lazy('index')
    
    
class ReturnListView(SuperUserRequiredMixin, LoginRequiredMixin, ListView):
    queryset = Return.objects.all()
    template_name = 'returns_list.html'
