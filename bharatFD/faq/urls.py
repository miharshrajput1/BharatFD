from django.urls import path
from .views import FAQListView, index
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'faqs', FAQListView, basename='faq')

urlpatterns = [
    path("", index, name="index"),
    path("api/faqs/", FAQListView.as_view(), name="faq-list"),
]
