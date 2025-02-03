from django.contrib import admin
from .models import FAQ, FAQTranslation
from .forms import FAQTranslationForm

class FAQTranslationInline(admin.TabularInline):
    """
    Inline model to allow adding translations directly in the FAQ admin panel.
    """
    model = FAQTranslation
    form = FAQTranslationForm
    extra = 0
    list_display = ("language", "question")


class FAQAdmin(admin.ModelAdmin):
    """
    Custom admin panel for managing FAQs.
    """
    list_display = ("question", "created_at")  # Display these fields in the list view
    search_fields = ("question",)  # Enable search functionality for questions
    list_filter = ("created_at",)  # Filter FAQs based on creation date
    inlines = [FAQTranslationInline]  # Include translations inline in the FAQ admin page


admin.site.register(FAQ, FAQAdmin)
