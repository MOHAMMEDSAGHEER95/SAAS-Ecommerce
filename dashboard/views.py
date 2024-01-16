from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import connection, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, UpdateView

from cms.models import Blog
from dashboard.forms import DashboardAdminForm, AddStoreProduct, AddBrandForm, AddCategoryForm, AddBlogForm
from orders.forms import OrderEdit
from orders.models import Order
from products.models import Products, Brand, Category
from tenant_schemas.utils import schema_context


# Create your views here.

class IsStaffMixin(PermissionRequiredMixin):
    def has_permission(self):
        # Check if the user is a superuser
        return self.request.user.is_superuser

class DashboardHomeView(PermissionRequiredMixin, TemplateView):
    permission_required = 'auth.view_user'
    login_url = '/dashboard/login'
    template_name = 'dashboard/dashboard_home.html'

    def has_permission(self):
        # Check if the user is a superuser
        return self.request.user.is_superuser


class DashboardLogin(FormView):
    template_name = 'dashboard/dashboard_login.html'
    form_class = DashboardAdminForm
    success_url = '/dashboard'


    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid credentials. Please try again.")
            form.add_error(None, "Invalid credentials")
            return self.form_invalid(form)


class OrderListView(IsStaffMixin, ListView):
    model = Order
    queryset = Order.objects.all()
    context_object_name = 'orders'
    template_name = 'dashboard/orders.html'

    def get_queryset(self):
        if self.request.GET.get('number'):
            return Order.objects.filter(number__icontains=self.request.GET.get('number'))
        return Order.objects.all().order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('number'):
            context['query'] = self.request.GET.get('number')
        return context


class PublicSchemaProductImport(IsStaffMixin, TemplateView):
    model = Products
    context_object_name = 'products'
    template_name = 'dashboard/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collapse_open'] = "show"
        context['page_title'] = "Import Products"
        product_list = []
        filter_kwargs = {}
        if self.request.GET.get("name"):
            filter_kwargs["title__icontains"] = self.request.GET.get("name")

        with schema_context('public'):
            for i in Products.objects.filter(**filter_kwargs):
                product_list.append(i)
            context['items'] = product_list
        return context

    def post(self, request):
        product_ids = request.POST.getlist("ids[]")
        tenant = connection.schema_name
        with schema_context('public'):
            products = Products.objects.filter(id__in=product_ids)
            for product in products:
                with schema_context(tenant):
                    Products.objects.create(title=product.title, public_schema_product_id=product.id,
                                            url=product.url, is_available=product.is_available,
                                            price=product.price, image=product.image,
                                            description=product.description)
        return JsonResponse({"message": "success"})


class StoreProductListView(IsStaffMixin, ListView):
    context_object_name = 'items'
    template_name = 'dashboard/products.html'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collapse_open'] = "show"
        context['page_title'] = "Store Products"
        return context

    def get_queryset(self):
        queryset = Products.objects.order_by('-id')
        filter_kwargs = {}
        if self.request.GET.get("name"):
            filter_kwargs["title__icontains"] = self.request.GET.get("name")
            return queryset.filter(**filter_kwargs)
        return queryset


class OrderEditView(IsStaffMixin, UpdateView):
    model = Order
    form_class = OrderEdit
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/order_edit.html'
    success_url = '/dashboard/orders'


class ChangeProductStatus(IsStaffMixin, View):

    def post(self, request):
        product_id = request.POST.get("product_id")
        status = request.POST.get("status") == "true"
        product = Products.objects.get(id=product_id)
        product.is_available = status
        product.save()
        return JsonResponse({"message": "product marked"})


class ProductContextMixin(object):
    page_title = ""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['collapse_open'] = "show"
        context['page_title'] = self.page_title

        return context


class CreateProductView(IsStaffMixin, ProductContextMixin, FormView):
    form_class = AddStoreProduct
    template_name = 'dashboard/product_create_edit.html'
    success_url = '/dashboard/store-products'
    page_title = "Product Create"




    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):

        return super().form_invalid(form)


class EditProductView(IsStaffMixin, ProductContextMixin, UpdateView):
    form_class = AddStoreProduct
    model = Products
    template_name = 'dashboard/product_create_edit.html'
    success_url = '/dashboard/store-products'
    pk_url_kwarg = 'pk'
    page_title = "Product Edit"




class BrandsListView(IsStaffMixin, ListView):
    model = Brand
    context_object_name = 'objects'
    template_name = 'dashboard/brands.html'
    add_object_url = '/dashboard/create-brand'
    edit_object_url = '/dashboard/edit-brand'
    metadata_value = 'Brand'
    collapse_open = "show"


    def get_queryset(self):
        filter_kwargs = {}
        if self.request.GET.get("title"):
            filter_kwargs = {'title__icontains': self.request.GET.get("title")}
        return self.model.objects.filter(**filter_kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("title"):
            context['query'] = self.request.GET.get("title")
        context['collapse_open'] = self.collapse_open
        context['metadata_value'] = self.metadata_value
        context['add_object_url'] = self.add_object_url
        context['edit_object_url'] = self.edit_object_url
        return context


class AddBrandView(IsStaffMixin, FormView):
    form_class = AddBrandForm
    template_name = 'dashboard/brand_create_edit.html'
    success_url = '/dashboard/brands/'
    metadata_value = 'Brand'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metadata_value'] = self.metadata_value
        context['collapse_open'] = "show"
        return context


class EditBrandView(IsStaffMixin, UpdateView):
    form_class = AddBrandForm
    template_name = 'dashboard/brand_create_edit.html'
    success_url = '/dashboard/brands/'
    pk_url_kwarg = 'pk'
    model = Brand


class CategoryListView(BrandsListView):
    model = Category
    add_object_url = '/dashboard/create-category'
    edit_object_url = '/dashboard/edit-category'
    metadata_value = 'Categories'

class AddCategoryView(AddBrandView):
    form_class = AddCategoryForm
    success_url = '/dashboard/categories/'
    metadata_value = 'Categories'


class EditCategoryView(IsStaffMixin, UpdateView):
    form_class = AddCategoryForm
    template_name = 'dashboard/brand_create_edit.html'
    success_url = '/dashboard/categories/'
    model = Category





class CanPublishMixin(PermissionRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.tenant.can_publish_cms():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("Cannot Publish CMS")


class BlogsListView(CanPublishMixin, BrandsListView):
    model = Blog
    template_name = 'dashboard/blogs.html'
    add_object_url = '/dashboard/create-blogs'
    edit_object_url = '/dashboard/edit-blog'
    metadata_value = 'Blogs'
    collapse_open = ''



class AddBlogsView(CanPublishMixin, IsStaffMixin, FormView):
    form_class = AddBlogForm
    template_name = 'dashboard/blog_create_edit.html'
    success_url = '/dashboard/blogs/'
    pk_url_kwarg = 'pk'
    metadata_value = 'Blogs'
    model = Blog


    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metadata_value'] = self.metadata_value
        return context


class EditBlog(CanPublishMixin, IsStaffMixin, UpdateView):
    form_class = AddBlogForm
    template_name = 'dashboard/blog_create_edit.html'
    success_url = '/dashboard/blogs/'
    model = Blog