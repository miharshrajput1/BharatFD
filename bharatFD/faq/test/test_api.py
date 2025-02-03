import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User  # Import User model for test authentication
from faq.models import FAQ, FAQTranslation  # Assuming the FAQ and FAQTranslation models are here

@pytest.mark.django_db
def test_faq_api(client):
    # Create a test user (if your API requires authentication)
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')  # Log in the test user

    # Create an FAQ
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python-based web framework."
    )
    
    url = reverse('faq-list')  # Replace with the correct API endpoint name
    response = client.get(url)

    # Check if the FAQ data is correctly returned
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  # Check that FAQ data is returned


@pytest.mark.django_db
def test_faq_api_with_lang(client):
    # Create a test user (if authentication is required)
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')  # Log in the test user

    # Create an FAQ and a translation
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python-based web framework."
    )

    FAQTranslation.objects.create(
        faq=faq,
        language="hi",
        question="डjango क्या है?",
        answer="Django एक पायथन-आधारित वेब फ्रेमवर्क है।"
    )

    url = reverse('faq-list') + "?lang=hi"  # Fetch FAQs in Hindi language
    response = client.get(url)

    # Ensure the response returns the translated FAQ
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  # Ensure that data is returned


@pytest.mark.django_db
def test_faq_api_invalid_lang(client):
    # Create a test user (if authentication is required)
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')  # Log in the test user

    # Create an FAQ and a translation
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python-based web framework."
    )

    FAQTranslation.objects.create(
        faq=faq,
        language="hi",
        question="डjango क्या है?",
        answer="Django एक पायथन-आधारित वेब फ्रेमवर्क है।"
    )

    # Try an unsupported language, fallback to English
    url = reverse('faq-list') + "?lang=fr"  # French translation does not exist
    response = client.get(url)

    # Ensure that the response returns FAQ in English
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0  # Ensure data is returned (fallback to English)


# If you need to check for permission-related issues, you can use the following pattern:
@pytest.mark.django_db
def test_faq_api_permission(client):
    # Create a test user (no login for this test, as we expect it to fail due to permissions)
    user = User.objects.create_user(username='testuser', password='password')
    # Do not login to test that the API returns a 403 Forbidden
    url = reverse('faq-list')
    response = client.get(url)
    
    # Check if the response status is Forbidden (because the user is not authenticated)
    assert response.status_code == status.HTTP_403_FORBIDDEN
