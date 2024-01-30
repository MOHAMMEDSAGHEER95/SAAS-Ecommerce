from django.views.generic import ListView, DetailView

from cms.models import Blog
from dashboard.views import CanPublishMixin


class BlogListView(CanPublishMixin, ListView):
    model = Blog
    template_name = 'dashboard/blogslist.html'
    context_object_name = 'blogs'
    queryset = Blog.objects.filter(status=Blog.PUBLISHED)
    permission_required = 'auth.view_user'

    def get_queryset(self):
        if self.request.GET.get('q'):
            return Blog.objects.filter(status=Blog.PUBLISHED, title__icontains=self.request.GET.get('q'))
        return Blog.objects.filter(status=Blog.PUBLISHED)


class BlogDetailView(CanPublishMixin, DetailView):
    model = Blog
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/blogdetails.html'
    permission_required = 'auth.view_user'
