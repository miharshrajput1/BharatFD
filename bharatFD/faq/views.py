from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from .models import FAQ
from .translation_service import generate_translation
from .serializers import FAQSerializer
from django.shortcuts import render

def index(request):
    return render(request, "faq_index.html")


class FAQListView(APIView):
    """
    REST API for fetching FAQs with multilingual support.
    
    Features:
    - Fetches a list of FAQs.
    - Supports language-based translations.
    - Returns data in JSON format.
    - If a language is provided (via query params), it returns the translated version.
    
    Query Parameters:
    - `lang`: (Optional) Specify the language code (e.g., `en`, `fr`, `hi`) to get FAQs in a specific language.
    - If no language is provided, it defaults to English.
    """
    permission_classes = []

    def get(self, request):
        lang = request.GET.get("lang", "en")  # Default to English
        faq_ids = FAQ.objects.values_list("id", flat=True)  # Fetch only IDs to minimize DB hits
        response_data = []

        for faq_id in faq_ids:
            cache_key = f"faq_{faq_id}_{lang}"
            data = cache.get(cache_key)  # Check the cache first

            if data:
                print(f"❄️ CACHE HIT: FAQ {faq_id} (Language: {lang})")
            else:
                print(f"🔥 DB HIT: Fetching FAQ {faq_id} (Language: {lang})")
                faq = FAQ.objects.get(id=faq_id)  # Query DB only if cache misses
                
                if lang == "en":
                    data = FAQSerializer(faq).data
                else:
                    data = faq.get_translation(lang)
                    if data["question"] == faq.question:
                        data = generate_translation(faq, lang)

                cache.set(cache_key, data, timeout=24*60*60)  # Cache for 24 hours
                print(f"🛠️ CACHE SET: Stored FAQ {faq_id} (Language: {lang})")

            response_data.append(data)

        return Response({"faqs": response_data})
