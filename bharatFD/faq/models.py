from django.db import models
from django.shortcuts import render
from django.core.cache import cache
from ckeditor.fields import RichTextField
from .translation_service import update_translations

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_translation(self, lang="en"):
        """Retrieve a translated FAQ dynamically"""
        if lang == "en":
            return {"question": self.question, "answer": self.answer}

        cache_key = f"faq_{self.id}_{lang}"
        data = cache.get(cache_key)

        if not data:
            try:
                translation = FAQTranslation.objects.get(faq=self, language=lang)
                data = {"question": translation.question, "answer": translation.answer}
                cache.set(cache_key, data, timeout=24*60*60)
            except FAQTranslation.DoesNotExist:
                # Fallback to English if translation does not exist
                data = {"question": self.question, "answer": self.answer}

        return data
    
    def save(self, *args, **kwargs):
        """Update translations when answer changes"""
        old_faq = None
        if self.pk:
            old_faq = FAQ.objects.filter(pk=self.pk).first()

        super().save(*args, **kwargs)

        if old_faq is None:
            # Create translations for new FAQs
            for lang in ["hi", "bn"]:
                FAQTranslation.objects.create(
                    faq=self,
                    language=lang,
                    question=update_translations(self.question, lang),
                    answer=update_translations(self.answer, lang),
                )

        if old_faq:
            translations = FAQTranslation.objects.filter(faq=self)
            for translation in translations:
                if old_faq.question != self.question:
                    translation.question = update_translations(self.question, translation.language)
                if old_faq.answer != self.answer:
                    translation.answer = update_translations(self.answer, translation.language)
                translation.save()

        # Preload new translations
        self.preload_translations()



    def preload_translations(self):
        """Preload all available translations into Redis"""
        translations = FAQTranslation.objects.filter(faq=self)
        for translation in translations:
            cache_key = f"faq_{self.id}_{translation.language}"
            data = {"question": translation.question, "answer": translation.answer}
            cache.set(cache_key, data, timeout=24*60*60)

    def __str__(self):
        return self.question


class FAQTranslation(models.Model):
    faq = models.ForeignKey(FAQ, related_name="translations", on_delete=models.CASCADE)
    language = models.CharField(max_length=10)
    question = models.TextField()
    answer = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
