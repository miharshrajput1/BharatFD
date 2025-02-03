from googletrans import Translator
from django.core.cache import cache

translator = Translator()

def generate_translation(faq, lang):
    """Translate FAQ dynamically if not available"""
    from .models import FAQTranslation
    translated_question = translator.translate(faq.question, dest=lang).text
    translated_answer = translator.translate(faq.answer, dest=lang).text

    # Save in the database
    translation = FAQTranslation.objects.create(faq=faq, language=lang, question=translated_question, answer=translated_answer)

    # Cache the translation
    cache_key = f"faq_{faq.id}_{lang}"
    cache.set(cache_key, {"question": translated_question, "answer": translated_answer}, timeout=24*60*60)

    return {"question": translated_question, "answer": translated_answer}


def update_translations(text, lang):
    """Update translations for a FAQ"""
    return translator.translate(text, dest=lang).text.strip()