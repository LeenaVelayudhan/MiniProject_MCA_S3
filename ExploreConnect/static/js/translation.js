document.addEventListener('DOMContentLoaded', function () {
    const languageOptions = {
        'af': 'afrikaans', 
        'sq': 'albanian',
        'am': 'amharic', 
        'ar': 'arabic', 
        'hy': 'armenian', 
        'az': 'azerbaijani', 
        'eu': 'basque', 
        'be': 'belarusian', 
        'bn': 'bengali', 
        'bs': 'bosnian', 
        'bg': 'bulgarian', 
        'ca': 'catalan', 
        'ceb': 'cebuano', 
        'ny': 'chichewa', 
        'zh-cn': 'chinese (simplified)', 
        'zh-tw': 'chinese (traditional)', 
        'co': 'corsican', 
        'hr': 'croatian', 
        'cs': 'czech', 
        'da': 'danish', 
        'nl': 'dutch', 
        'en': 'english', 
        'eo': 'esperanto', 
        'et': 'estonian', 
        'tl': 'filipino', 
        'fi': 'finnish', 
        'fr': 'french', 
        'fy': 'frisian', 
        'gl': 'galician', 
        'ka': 'georgian', 
        'de': 'german', 
        'el': 'greek', 
        'gu': 'gujarati', 
        'ht': 'haitian creole', 
        'ha': 'hausa', 
        'haw': 'hawaiian', 
        'iw': 'hebrew', 
        'he': 'hebrew', 
        'hi': 'hindi', 
        'hmn': 'hmong', 
        'hu': 'hungarian', 
        'is': 'icelandic', 
        'ig': 'igbo', 
        'id': 'indonesian', 
        'ga': 'irish', 
        'it': 'italian', 
        'ja': 'japanese', 
        'jw': 'javanese', 
        'kn': 'kannada', 
        'kk': 'kazakh', 
        'km': 'khmer', 
        'ko': 'korean', 
        'ku': 'kurdish (kurmanji)', 
        'ky': 'kyrgyz', 
        'lo': 'lao', 
        'la': 'latin', 
        'lv': 'latvian', 
        'lt': 'lithuanian', 
        'lb': 'luxembourgish', 
        'mk': 'macedonian', 
        'mg': 'malagasy', 
        'ms': 'malay', 
        'ml': 'malayalam', 
        'mt': 'maltese', 
        'mi': 'maori', 
        'mr': 'marathi', 
        'mn': 'mongolian', 
        'my': 'myanmar (burmese)', 
        'ne': 'nepali', 
        'no': 'norwegian', 
        'or': 'odia', 
        'ps': 'pashto', 
        'fa': 'persian', 
        'pl': 'polish', 
        'pt': 'portuguese', 
        'pa': 'punjabi', 
        'ro': 'romanian', 
        'ru': 'russian', 
        'sm': 'samoan', 
        'gd': 'scots gaelic', 
        'sr': 'serbian', 
        'st': 'sesotho', 
        'sn': 'shona', 
        'sd': 'sindhi', 
        'si': 'sinhala', 
        'sk': 'slovak', 
        'sl': 'slovenian', 
        'so': 'somali', 
        'es': 'spanish', 
        'su': 'sundanese', 
        'sw': 'swahili', 
        'sv': 'swedish', 
        'tg': 'tajik', 
        'ta': 'tamil', 
        'te': 'telugu', 
        'th': 'thai', 
        'tr': 'turkish', 
        'uk': 'ukrainian', 
        'ur': 'urdu', 
        'ug': 'uyghur', 
        'uz': 'uzbek', 
        'vi': 'vietnamese', 
        'cy': 'welsh', 
        'xh': 'xhosa', 
        'yi': 'yiddish', 
        'yo': 'yoruba', 
        'zu': 'zulu'
        
    };

    
    // Populate language dropdowns
    const inputLanguageSelect = document.getElementById('input-language');
    const outputLanguageSelect = document.getElementById('output-language');

    for (const [code, language] of Object.entries(languageOptions)) {
        const inputOption = document.createElement('option');
        inputOption.value = code;
        inputOption.textContent = language;
        inputLanguageSelect.appendChild(inputOption);

        const outputOption = document.createElement('option');
        outputOption.value = code;
        outputOption.textContent = language;
        outputLanguageSelect.appendChild(outputOption);
    }

    document.getElementById('start_speaking').addEventListener('click', function(event) {
        event.preventDefault();  // Prevent page refresh

        const inputLanguage = document.getElementById('input-language').value;
        const outputLanguage = document.getElementById('output-language').value;
        const statusElement = document.getElementById('status');
        const resultElement = document.getElementById('translation_result');
        const audioElement = document.getElementById('translated_audio');

        // Initialize SpeechRecognition
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = inputLanguage;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        statusElement.textContent = 'Status: Listening...';

        recognition.start();

        recognition.onresult = function(event) {
            const inputText = event.results[0][0].transcript;
            console.log("Speech recognized:", inputText);  // Log recognized text
            statusElement.textContent = 'Status: Processing...';
            resultElement.textContent = `Heard: ${inputText}`;  // Display recognized text before translation

            // Send the recognized speech to the Django view for translation
            fetch('/translate-audio/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: new URLSearchParams({
                    'input_text': inputText,
                    'input_language': inputLanguage,
                    'output_language': outputLanguage
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.translated_text) {
                    resultElement.textContent = `Translation: ${data.translated_text}`;
                    audioElement.src = data.audio_path;
                    audioElement.style.display = 'block';
                    audioElement.play();
                    statusElement.textContent = 'Status: Translation Complete';
                } else {
                    resultElement.textContent = 'Translation failed.';
                    statusElement.textContent = 'Status: Error';
                }
            })
            .catch(error => {
                console.error('Error during translation:', error);
                resultElement.textContent = 'An error occurred during translation.';
                statusElement.textContent = 'Status: Error';
            });
            
        };

        recognition.onerror = function(event) {
            console.error('SpeechRecognition error:', event.error);  // Log recognition errors
            statusElement.textContent = `Error: ${event.error}`;
        };

        recognition.onspeechend = function() {
            recognition.stop();
            statusElement.textContent = 'Status: Processing...';
            console.log("Speech recognition ended");  // Log when speech recognition ends
        };
    });
});
    
    
    



    
        
    