from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import CustomLoginForm, ProductForm
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

class StaffRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            # Redirect to a different URL or show an error message
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomLoginForm()  
        return context
    
    def post(self, request, **kwargs):
        #SQL Injection
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not user.is_staff:
                    return redirect('customer_home')
                else:
                    return redirect('product_list')

            else:
                form.add_error(None, "Invalid username or password.")
        return self.render_to_response(self.get_context_data(form=form))

class CustomerHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'customer_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class ProductListView(StaffRequiredMixin, TemplateView):
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class ProductAddView(StaffRequiredMixin, TemplateView):
    template_name = 'product_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            return self.render_to_response(self.get_context_data(form=form, form_errors=form.errors))


class ProductEditView(StaffRequiredMixin, TemplateView):
    template_name = 'product_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        context['product'] = product
        context['form'] = ProductForm(instance=product)
        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            return self.render_to_response(self.get_context_data(form=form, form_errors=form.errors))

class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')