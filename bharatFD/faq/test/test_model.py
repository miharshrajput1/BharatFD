import pytest
from faq.models import FAQ, FAQTranslation  # Replace faq_app with your actual app name

@pytest.mark.django_db
def test_faq_creation():
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python-based web framework."
    )
    
    assert faq.question == "What is Django?"
    assert faq.answer == "Django is a Python-based web framework."
    assert faq.created_at is not None

@pytest.mark.django_db
def test_faq_translation_creation():
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python-based web framework."
    )
    
    # Create translation for the FAQ in Hindi
    translation = FAQTranslation.objects.create(
        faq=faq,
        language="hi",
        question="डjango क्या है?",
        answer="Django एक पायथन-आधारित वेब फ्रेमवर्क है।"
    )

    assert translation.language == "hi"
    assert translation.question == "डjango क्या है?"
    assert translation.answer == "Django एक पायथन-आधारित वेब फ्रेमवर्क है।"
    assert translation.faq == faq

@pytest.mark.django_db
def test_faq_translation_fallback():
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a Python-based web framework."
    )
    
    # No translation for French, so it should fallback to the default language (English)
    translation = FAQTranslation.objects.create(
        faq=faq,
        language="fr",  # French translation
        question="Qu'est-ce que Django?",
        answer="Django est un framework web basé sur Python."
    )

    # Testing fallback in the get_translation method
    translated_data = faq.get_translation(lang="fr")
    assert translated_data["question"] == "Qu'est-ce que Django?"
    assert translated_data["answer"] == "Django est un framework web basé sur Python."
