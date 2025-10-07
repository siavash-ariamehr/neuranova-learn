import { createContext, useContext, useState, ReactNode } from 'react';

interface LanguageContextType {
  currentLanguage: string;
  setLanguage: (lang: string) => void;
  supportedLanguages: { code: string; name: string }[];
  translateText: (text: string, targetLang?: string) => Promise<string>;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

const languageNames: { [key: string]: string } = {
  en: 'English',
  zh: 'Chinese (Mandarin)',
  es: 'Spanish',
  hi: 'Hindi',
  ar: 'Arabic',
  fr: 'French',
  bn: 'Bengali',
  pt: 'Portuguese',
  ru: 'Russian',
  ur: 'Urdu',
  id: 'Indonesian',
  de: 'German',
  ja: 'Japanese',
  tr: 'Turkish',
  fa: 'Persian',
  it: 'Italian',
  pl: 'Polish',
  nl: 'Dutch',
  sv: 'Swedish',
  fi: 'Finnish',
  no: 'Norwegian'
};

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const supportedLanguages = Object.keys(languageNames).map(code => ({
    code,
    name: languageNames[code]
  }));

  const setLanguage = (lang: string) => {
    setCurrentLanguage(lang);
    localStorage.setItem('preferred_language', lang);
  };

  const translateText = async (text: string, targetLang?: string): Promise<string> => {
    const target = targetLang || currentLanguage;
    
    if (target === 'en') {
      return text;
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/translation/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text,
          source_lang: 'en',
          target_lang: target
        })
      });

      if (response.ok) {
        const data = await response.json();
        return data.translated_text;
      }
    } catch (error) {
      console.error('Translation failed:', error);
    }

    return text;
  };

  return (
    <LanguageContext.Provider value={{ currentLanguage, setLanguage, supportedLanguages, translateText }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
