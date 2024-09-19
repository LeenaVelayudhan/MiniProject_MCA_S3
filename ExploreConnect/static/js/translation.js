document.addEventListener('DOMContentLoaded', function () {
    const languageOptions = {
        'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 
        'hy': 'Armenian', 'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian', 
        'bn': 'Bengali', 'bs': 'Bosnian', 'bg': 'Bulgarian', 'ca': 'Catalan', 
        'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinese (Simplified)', 
        'zh-tw': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian', 
        'cs': 'Czech', 'da': 'Danish', 'nl': 'Dutch', 'en': 'English', 
        'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino', 'fi': 'Finnish', 
        'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian', 
        'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole', 
        'ha': 'Hausa', 'haw': 'Hawaiian', 'iw': 'Hebrew', 'he': 'Hebrew', 
        'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian', 'is': 'Icelandic', 
        'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian', 
        'ja': 'Japanese', 'jw': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 
        'km': 'Khmer', 'ko': 'Korean', 'ku': 'Kurdish', 'ky': 'Kyrgyz', 
        'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian', 'lt': 'Lithuanian', 
        'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy', 'ms': 'Malay', 
        'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi', 
        'mn': 'Mongolian', 'my': 'Burmese', 'ne': 'Nepali', 'no': 'Norwegian', 
        'or': 'Odia', 'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 
        'pt': 'Portuguese', 'pa': 'Punjabi', 'ro': 'Romanian', 'ru': 'Russian', 
        'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian', 'st': 'Sesotho', 
        'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 
        'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 
        'sw': 'Swahili', 'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 
        'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 
        'ur': 'Urdu', 'uz': 'Uzbek', 'vi': 'Vietnamese', 'cy': 'Welsh', 
        'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu',
    };

    const inputLanguageSelect = document.getElementById('input-language');
    const outputLanguageSelect = document.getElementById('output-language');
    const inputLanguageTextBox = document.getElementById('input-language-text');  // Input language textbox
    const outputLanguageTextBox = document.getElementById('output-language-text');  // Output language textbox

    // Populate language options for both input and output
    Object.entries(languageOptions).forEach(([code, language]) => {
        const inputOption = new Option(language, code);
        const outputOption = new Option(language, code);
        inputLanguageSelect.appendChild(inputOption);
        outputLanguageSelect.appendChild(outputOption);
    });

    // Update textbox with selected languages
    inputLanguageSelect.addEventListener('change', () => {
        inputLanguageTextBox.value = inputLanguageSelect.options[inputLanguageSelect.selectedIndex].text;
    });
    outputLanguageSelect.addEventListener('change', () => {
        outputLanguageTextBox.value = outputLanguageSelect.options[outputLanguageSelect.selectedIndex].text;
    });

    let recognition;
    let recognizedText = '';

    document.getElementById('start_speaking').addEventListener('click', function (event) {
        event.preventDefault();

        const inputLanguage = inputLanguageSelect.value;
        const statusElement = document.getElementById('status');
        const resultElement = document.getElementById('translation_result');

        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = inputLanguage;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        statusElement.textContent = 'Status: Listening...';
        recognition.start();

        recognition.onresult = (event) => {
            recognizedText = event.results[0][0].transcript;
            statusElement.textContent = 'Status: Speech recognized';
            resultElement.textContent = `Heard: ${recognizedText}`;
        };

        recognition.onerror = (event) => {
            statusElement.textContent = `Error: ${event.error}`;
        };

        recognition.onspeechend = () => {
            recognition.stop();
            statusElement.textContent = 'Status: Recognition ended';
        };
    });

    document.getElementById('stop_speaking').addEventListener('click', function () {
        if (recognition) {
            recognition.stop();
            document.getElementById('status').textContent = 'Status: Stopped';
        }
    });

    document.getElementById('translate_button').addEventListener('click', function () {
        const inputLanguage = inputLanguageSelect.value;
        const outputLanguage = outputLanguageSelect.value;
        const resultElement = document.getElementById('translation_result');
        const audioElement = document.getElementById('translated_audio');
        const statusElement = document.getElementById('status');

        if (!recognizedText) {
            resultElement.textContent = 'No recognized text to translate. Please start speaking first.';
            statusElement.textContent = 'Status: Error';
            return;
        }

        statusElement.textContent = 'Status: Translating...';

        fetch('/translate_audio/', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  
            },
            body: new URLSearchParams({
                'input_text': recognizedText,
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
            resultElement.textContent = 'An error occurred during translation.';
            statusElement.textContent = 'Status: Error';
        });
    });

    // Helper function to retrieve CSRF token
    function getCookie(name) {
        const cookies = document.cookie.split(';').map(cookie => cookie.trim());
        for (const cookie of cookies) {
            if (cookie.startsWith(`${name}=`)) {
                return decodeURIComponent(cookie.slice(name.length + 1));
            }
        }
        return null;
    }
});
