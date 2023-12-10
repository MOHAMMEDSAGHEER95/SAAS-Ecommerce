from django.contrib import admin

# Register your models here.
from django.utils.text import slugify

from onboarding.models import Plan


class PlanAdmin(admin.ModelAdmin):
    model = Plan

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        obj.save()


admin.site.register(Plan, PlanAdmin)
