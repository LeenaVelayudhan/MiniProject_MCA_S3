  
// document.addEventListener('DOMContentLoaded', function () {
//     const languageOptions = {
//         'af': 'afrikaans', 
//         'sq': 'albanian',
//         'am': 'amharic', 
//         'ar': 'arabic', 
//         'hy': 'armenian', 
//         'az': 'azerbaijani', 
//         'eu': 'basque', 
//         'be': 'belarusian', 
//         'bn': 'bengali', 
//         'bs': 'bosnian', 
//         'bg': 'bulgarian', 
//         'ca': 'catalan', 
//         'ceb': 'cebuano', 
//         'ny': 'chichewa', 
//         'zh-cn': 'chinese (simplified)', 
//         'zh-tw': 'chinese (traditional)', 
//         'co': 'corsican', 
//         'hr': 'croatian', 
//         'cs': 'czech', 
//         'da': 'danish', 
//         'nl': 'dutch', 
//         'en': 'english', 
//         'eo': 'esperanto', 
//         'et': 'estonian', 
//         'tl': 'filipino', 
//         'fi': 'finnish', 
//         'fr': 'french', 
//         'fy': 'frisian', 
//         'gl': 'galician', 
//         'ka': 'georgian', 
//         'de': 'german', 
//         'el': 'greek', 
//         'gu': 'gujarati', 
//         'ht': 'haitian creole', 
//         'ha': 'hausa', 
//         'haw': 'hawaiian', 
//         'iw': 'hebrew', 
//         'he': 'hebrew', 
//         'hi': 'hindi', 
//         'hmn': 'hmong', 
//         'hu': 'hungarian', 
//         'is': 'icelandic', 
//         'ig': 'igbo', 
//         'id': 'indonesian', 
//         'ga': 'irish', 
//         'it': 'italian', 
//         'ja': 'japanese', 
//         'jw': 'javanese', 
//         'kn': 'kannada', 
//         'kk': 'kazakh', 
//         'km': 'khmer', 
//         'ko': 'korean', 
//         'ku': 'kurdish (kurmanji)', 
//         'ky': 'kyrgyz', 
//         'lo': 'lao', 
//         'la': 'latin', 
//         'lv': 'latvian', 
//         'lt': 'lithuanian', 
//         'lb': 'luxembourgish', 
//         'mk': 'macedonian', 
//         'mg': 'malagasy', 
//         'ms': 'malay', 
//         'ml': 'malayalam', 
//         'mt': 'maltese', 
//         'mi': 'maori', 
//         'mr': 'marathi', 
//         'mn': 'mongolian', 
//         'my': 'myanmar (burmese)', 
//         'ne': 'nepali', 
//         'no': 'norwegian', 
//         'or': 'odia', 
//         'ps': 'pashto', 
//         'fa': 'persian', 
//         'pl': 'polish', 
//         'pt': 'portuguese', 
//         'pa': 'punjabi', 
//         'ro': 'romanian', 
//         'ru': 'russian', 
//         'sm': 'samoan', 
//         'gd': 'scots gaelic', 
//         'sr': 'serbian', 
//         'st': 'sesotho', 
//         'sn': 'shona', 
//         'sd': 'sindhi', 
//         'si': 'sinhala', 
//         'sk': 'slovak', 
//         'sl': 'slovenian', 
//         'so': 'somali', 
//         'es': 'spanish', 
//         'su': 'sundanese', 
//         'sw': 'swahili', 
//         'sv': 'swedish', 
//         'tg': 'tajik', 
//         'ta': 'tamil', 
//         'te': 'telugu', 
//         'th': 'thai', 
//         'tr': 'turkish', 
//         'uk': 'ukrainian', 
//         'ur': 'urdu', 
//         'ug': 'uyghur', 
//         'uz': 'uzbek', 
//         'vi': 'vietnamese', 
//         'cy': 'welsh', 
//         'xh': 'xhosa', 
//         'yi': 'yiddish', 
//         'yo': 'yoruba', 
//         'zu': 'zulu'
//     };
// const inputLanguageSelect = document.getElementById('input-language');
// const outputLanguageSelect = document.getElementById('output-language');

// for (const [code, language] of Object.entries(languageOptions)) {
// const inputOption = document.createElement('option');
// inputOption.value = code;
// inputOption.textContent = language;
// inputLanguageSelect.appendChild(inputOption);

// const outputOption = document.createElement('option');
// outputOption.value = code;
// outputOption.textContent = language;
// outputLanguageSelect.appendChild(outputOption);
// }     
    
// let recognition;
// let recognizedText = '';

// document.getElementById('start_speaking').addEventListener('click', function (event) {
// event.preventDefault();

// const inputLanguage = document.getElementById('input-language').value;
// const statusElement = document.getElementById('status');
// const resultElement = document.getElementById('translation_result');

// // Initialize SpeechRecognition
// recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
// recognition.lang = inputLanguage;
// recognition.interimResults = false;
// recognition.maxAlternatives = 1;

// statusElement.textContent = 'Status: Listening...';

// recognition.start();

// recognition.onresult = function (event) {
//     recognizedText = event.results[0][0].transcript;
//     console.log("Speech recognized:", recognizedText);
//     statusElement.textContent = 'Status: Speech recognized';
//     resultElement.textContent = `Heard: ${recognizedText}`;
// };

// recognition.onerror = function (event) {
//     console.error('SpeechRecognition error:', event.error);
//     statusElement.textContent = `Error: ${event.error}`;
// };

// recognition.onspeechend = function () {
//     recognition.stop();
//     statusElement.textContent = 'Status: Recognition ended';
//     console.log("Speech recognition ended");
// };
// });

// document.getElementById('stop_speaking').addEventListener('click', function () {
// if (recognition) {
//     recognition.stop();
//     document.getElementById('status').textContent = 'Status: Stopped';
//     console.log("Speech recognition stopped manually");
// }
// });

// document.getElementById('translate_button').addEventListener('click', function () {
// const inputLanguage = document.getElementById('input-language').value;
// const outputLanguage = document.getElementById('output-language').value;
// const resultElement = document.getElementById('translation_result');
// const audioElement = document.getElementById('translated_audio');
// const statusElement = document.getElementById('status');

// if (recognizedText) {
//     console.log("Starting translation for text:", recognizedText);

//     statusElement.textContent = 'Status: Translating...';

//     fetch('/translate_audio/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//             'X-CSRFToken': '{{ csrf_token }}'
//         },
//         body: new URLSearchParams({
//             'input_text': recognizedText,
//             'input_language': inputLanguage,
//             'output_language': outputLanguage
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log("Translation response:", data);

//         if (data.translated_text) {
//             resultElement.textContent = `Translation: ${data.translated_text}`;
//             audioElement.src = data.audio_path;
//             audioElement.style.display = 'block';
//             audioElement.play();
//             statusElement.textContent = 'Status: Translation Complete';
//         } else {
//             resultElement.textContent = 'Translation failed.';
//             statusElement.textContent = 'Status: Error';
//         }
//     })
//     .catch(error => {
//         console.error('Error during translation:', error);
//         resultElement.textContent = 'An error occurred during translation.';
//         statusElement.textContent = 'Status: Error';
//     });
// } else {
//     resultElement.textContent = 'No recognized text to translate. Please start speaking first.';
//     statusElement.textContent = 'Status: Error';
// }
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// const csrftoken = getCookie('csrftoken');
// function translateAudio() {
// const data = {
// input_text: document.getElementById('input-text').value,
// input_language: document.getElementById('input-language').value,
// output_language: document.getElementById('output-language').value,
// };

// fetch('/translate_audio/', {
// method: 'POST',
// headers: {
//     'X-CSRFToken': csrftoken,  // Include the CSRF token here
//     'Content-Type': 'application/json'
// },
// body: JSON.stringify(data)
// })
// .then(response => response.json())
// .then(result => {
// console.log('Success:', result);
// document.getElementById('translation_result').innerText = result.translated_text;
// })
// .catch(error => {
// console.error('Error:', error);
// });
// }

// document.getElementById('translate_button').addEventListener('click', translateAudio);


// });
// });
    
    




document.addEventListener('DOMContentLoaded', function () {
    const languageOptions = {
        'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 
        'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 
        'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 
        'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 
        'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 
        'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 
        'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 
        'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 
        'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 
        'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 
        'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 
        'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 
        'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 
        'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 
        'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 
        'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 
        'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 
        'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 
        'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 
        'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 
        'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 
        'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 
        'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 
        'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 
        'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 
        'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 
        'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu',
    };

    const inputLanguageSelect = document.getElementById('input-language');
    const outputLanguageSelect = document.getElementById('output-language');
    
    // Populate language options for both input and output
    Object.entries(languageOptions).forEach(([code, language]) => {
        const inputOption = new Option(language, code);
        const outputOption = new Option(language, code);
        inputLanguageSelect.appendChild(inputOption);
        outputLanguageSelect.appendChild(outputOption);
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

        fetch('translate_audio/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Include the CSRF token here
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





