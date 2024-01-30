from django.contrib import admin

# Register your models here.
from django.utils.text import slugify

from cms.models import Blog
from onboarding.models import Plan, Onboarding


class PlanAdmin(admin.ModelAdmin):
    model = Plan

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        obj.save()


admin.site.register(Plan, PlanAdmin)
admin.site.register(Onboarding)
admin.site.register(Blog)
