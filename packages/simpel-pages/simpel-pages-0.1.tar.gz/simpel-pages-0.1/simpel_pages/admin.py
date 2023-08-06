from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import PageForm
from .models import Page, PageGallery


class PageGalleryInline(admin.StackedInline):
    model = PageGallery
    extra = 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ("url", "title")
    list_filter = ("sites", "registration_required")
    search_fields = ("url", "title")
    inlines = [PageGalleryInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "url",
                    "title",
                    "thumbnail",
                    "content",
                    "summary",
                    "allow_comments",
                    "registration_required",
                    "sites",
                )
            },
        ),
        (_("SEO Settings"), {"fields": ("template", "seo_title", "seo_description")}),
    )
