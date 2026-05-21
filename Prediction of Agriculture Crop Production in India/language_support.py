"""
Multilingual Support Module
Provides translations in multiple Indian languages
"""

class LanguageManager:
    def __init__(self, default_language: str = 'english'):
        """Initialize language manager"""
        self.current_language = default_language
        self.translations = {
            'english': {
                'welcome': 'Welcome to Smart Agriculture System',
                'login': 'Login',
                'signup': 'Sign Up',
                'logout': 'Logout',
                'prediction': 'Crop Production Prediction',
                'disease': 'Disease Detection',
                'irrigation': 'Smart Irrigation',
                'fertilizer': 'Fertilizer Recommendation',
                'weather': 'Weather Information',
                'chatbot': 'Farmer Assistant',
                'report': 'Generate Report',
                'profile': 'My Profile',
                'enter_crop': 'Enter Crop Name',
                'enter_area': 'Enter Farm Area (hectares)',
                'enter_rainfall': 'Enter Annual Rainfall (mm)',
                'enter_temperature': 'Enter Temperature (°C)',
                'predict': 'Predict Production',
                'result': 'Prediction Result',
                'tons': 'tons',
                'confidence': 'Confidence Score',
                'success': 'Success',
                'error': 'Error',
                'loading': 'Loading...',
            },
            'hindi': {
                'welcome': 'स्मार्ट कृषि प्रणाली में आपका स्वागत है',
                'login': 'लॉगिन',
                'signup': 'साइन अप',
                'logout': 'लॉगआउट',
                'prediction': 'फसल उत्पादन पूर्वानुमान',
                'disease': 'रोग पहचान',
                'irrigation': 'स्मार्ट सिंचाई',
                'fertilizer': 'उर्वरक सुझाव',
                'weather': 'मौसम की जानकारी',
                'chatbot': 'किसान सहायक',
                'report': 'रिपोर्ट जेनरेट करें',
                'profile': 'मेरी प्रोफाइल',
                'enter_crop': 'फसल का नाम दर्ज करें',
                'enter_area': 'खेत का क्षेत्र दर्ज करें (हेक्टेयर)',
                'enter_rainfall': 'वार्षिक वर्षा दर्ज करें (मिमी)',
                'enter_temperature': 'तापमान दर्ज करें (°C)',
                'predict': 'उत्पादन की भविष्यवाणी करें',
                'result': 'भविष्यवाणी परिणाम',
                'tons': 'टन',
                'confidence': 'विश्वास स्कोर',
                'success': 'सफलता',
                'error': 'त्रुटि',
                'loading': 'लोड हो रहा है...',
            },
            'tamil': {
                'welcome': 'ஸ்மார்ட் விவசாய வணக்கம்',
                'login': 'உள்நுழைவு',
                'signup': 'பதிவு செய்யவும்',
                'logout': 'வெளியேறு',
                'prediction': 'பயிர் உற்பादन முன்னறிவிப்பு',
                'disease': 'நோய் கண்டறிதல்',
                'irrigation': 'நினைவுரை நீர் பாசனம்',
                'fertilizer': 'உரம் பரிந்துरை',
                'weather': 'வானிலை தகவல்',
                'chatbot': 'விவசாயி உதவி',
                'report': 'அறிக்கை உருவாக்கவும்',
                'profile': 'என் சுயவிவரம்',
                'enter_crop': 'பயிர் பெயரை உள்ளிடவும்',
                'enter_area': 'பண்ணை பகுதি உள்ளிடவும் (ஹெக்டேர்)',
                'enter_rainfall': 'வার்ષिक வर्षा உள்ளிடவும் (மிமी)',
                'enter_temperature': 'வெப்பநிலை உள்ளிடவும் (°C)',
                'predict': 'உற்பादன முன்னறிவிப்பு',
                'result': 'முன்னறிவிப்பு முடிவு',
                'tons': 'டன்',
                'confidence': 'நம்பிக்கை மதிப்பெண்',
                'success': 'வெற்றி',
                'error': 'பிழை',
                'loading': 'ஏற்றுகிறது...',
            },
            'telugu': {
                'welcome': 'స్మార్ట్ కృషि వ్యవస్థకు స్వాగతం',
                'login': 'ప్రవేశించండి',
                'signup': 'సైన్ అప్ చేయండి',
                'logout': 'లాగ్ అవుట్ చేయండి',
                'prediction': 'పంట ఉత్పత్తి ప్రిడిక్షన్',
                'disease': 'వ్యాధి సনాక్తీకరణ',
                'irrigation': 'స్మార్ట్ నీటిపాచన',
                'fertilizer': 'ఫర్టిలైజర్ సిఫారసు',
                'weather': 'వాతావరణ సమాచారం',
                'chatbot': 'రైతు సహాయक',
                'report': 'నివేదిక రూపొందించండి',
                'profile': 'నా ప్రొఫైల్',
                'enter_crop': 'పంట పేరు నమోదు చేయండి',
                'enter_area': 'పొలం ప్రాంతం నమోదు చేయండి',
                'enter_rainfall': 'వార్షిక వర్షపాతం నమోదు చేయండి',
                'enter_temperature': 'ఉష్ణోగ్రత నమోదు చేయండి',
                'predict': 'ఉత్పత్తిని అంచనా వేయండి',
                'result': 'ప్రిడిక్షన్ ఫలితం',
                'tons': 'టన్నులు',
                'confidence': 'విశ్వాస స్కోర్',
                'success': 'విజయం',
                'error': 'లోపం',
                'loading': 'లోడ్ చేస్తున్నది...',
            }
        }
    
    def get_text(self, key: str, language: str = None) -> str:
        """
        Get translated text
        
        Args:
            key: Translation key
            language: Language code (if None, uses current language)
        
        Returns:
            Translated text or key if not found
        """
        lang = language or self.current_language
        return self.translations.get(lang, {}).get(key, key)
    
    def set_language(self, language: str):
        """Set current language"""
        if language in self.translations:
            self.current_language = language
            return True
        return False
    
    def get_available_languages(self) -> list:
        """Get list of available languages"""
        return list(self.translations.keys())
    
    def translate_prediction_result(self, result: dict, language: str = None) -> dict:
        """Translate prediction result to target language"""
        lang = language or self.current_language
        
        translated = {
            'crop': result.get('crop', ''),
            'predicted_production': f"{result.get('predicted_production', 0):.2f} {self.get_text('tons', lang)}",
            'confidence': f"{result.get('confidence', 0):.2%}",
            'result_label': self.get_text('result', lang),
        }
        
        return translated
    
    def translate_disease_result(self, result: dict, language: str = None) -> dict:
        """Translate disease detection result"""
        lang = language or self.current_language
        
        translated = {
            'disease': result.get('detected_disease', ''),
            'confidence': f"{result.get('confidence', 0):.2%}",
            'treatment': result.get('treatment', ''),
            'disease_label': self.get_text('disease', lang),
        }
        
        return translated
    
    def get_crop_names_translated(self, language: str = None) -> dict:
        """Get common crop names in target language"""
        lang = language or self.current_language
        
        crop_translations = {
            'english': ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Cotton', 'Groundnut', 'Soybean'],
            'hindi': ['चावल', 'गेहूँ', 'मकई', 'गन्ना', 'कपास', 'मूंगफली', 'सोयाबीन'],
            'tamil': ['அரிசி', 'கோதுமை', 'சோளம்', 'கரும்பு', '棉', 'நிலக்கடலை', 'சோயாபீன்'],
            'telugu': ['గోధుమ', 'వీట్', 'మక్క', 'చెరకు', 'పత్తి', 'వేరుశనగ', 'సోయాబీన్'],
        }
        
        return crop_translations.get(lang, crop_translations['english'])
    
    def get_month_names(self, language: str = None) -> list:
        """Get month names in target language"""
        lang = language or self.current_language
        
        months = {
            'english': ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'],
            'hindi': ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
                     'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'],
            'tamil': ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
                     'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'],
            'telugu': ['జనవరి', 'ఫిబ్రవరి', 'మార్చి', 'ఏప్రిల్', 'మే', 'జూన్',
                      'జూలై', 'ఆగస్టు', 'సెప్టెంబర్', 'అక్టోబర్', 'నవంబర్', 'డిసెంబర్'],
        }
        
        return months.get(lang, months['english'])

# Initialize
language_manager = LanguageManager()
