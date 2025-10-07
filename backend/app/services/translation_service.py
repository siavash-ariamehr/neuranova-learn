import os
from typing import List, Dict
import httpx
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class TranslationService:
    def __init__(self):
        self.supported_languages = [
            "en", "zh", "es", "hi", "ar", "fr", "bn", "pt", "ru", "ur",
            "id", "de", "ja", "tr", "fa", "it", "pl", "nl", "sv", "fi", "no"
        ]
        self.model_name = "facebook/m2m100_418M"
        self.model = None
        self.tokenizer = None
        
    async def load_model(self):
        if self.model is None:
            self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
            self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
    
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> str:
        if source_lang not in self.supported_languages or target_lang not in self.supported_languages:
            raise ValueError(f"Unsupported language. Supported: {self.supported_languages}")
        
        if source_lang == target_lang:
            return text
        
        await self.load_model()
        
        self.tokenizer.src_lang = source_lang
        encoded = self.tokenizer(text, return_tensors="pt")
        
        generated_tokens = self.model.generate(
            **encoded,
            forced_bos_token_id=self.tokenizer.get_lang_id(target_lang)
        )
        
        translated = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        return translated
    
    async def detect_language(self, text: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://translation.googleapis.com/language/translate/v2/detect",
                    params={"key": os.getenv("GOOGLE_TRANSLATE_API_KEY", "")},
                    json={"q": text}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["data"]["detections"][0][0]["language"]
        except Exception:
            pass
        
        return "en"
    
    async def batch_translate(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str
    ) -> List[str]:
        translations = []
        for text in texts:
            translated = await self.translate(text, source_lang, target_lang)
            translations.append(translated)
        return translations

translation_service = TranslationService()
