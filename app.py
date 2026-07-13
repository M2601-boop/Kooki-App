from flask import Flask, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

# קוד המסך המעוצב של הצ'אט יושב עכשיו ישירות בתוך פייתון כדי שלא ייעלם
HTML_PAGE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🗣️ פלטפורמת תרגום שיחות</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 20px; text-align: center; color: #333; }
        .chat-box { max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 100px; padding: 12px; box-sizing: border-box; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 6px; font-size: 16px; resize: none; }
        select, button { padding: 12px; width: 100%; margin-bottom: 15px; font-size: 16px; border-radius: 6px; border: 1px solid #ccc; }
        button { background: #007bff; color: white; border: none; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #0056b3; }
        .result { background: #d4edda; color: #155724; padding: 15px; border-radius: 6px; font-weight: bold; margin-top: 15px; display: none; text-align: right; line-height: 1.5; }
    </style>
</head>
<body>
<div class="chat-box">
    <h2>🗣️ תרגום שיחה בזמן אמת</h2>
    <p>כתוב משפט בעברית ובחר לאיזו שפה לתרגם עבור הצד השני:</p>
    <textarea id="userInput" placeholder="הקלד כאן משפט בעברית..."></textarea>
    <select id="langSelect">
        <option value="en">אנגלית (English)</option>
        <option value="es">ספרדית (Español)</option>
        <option value="ar">ערבית (العربية)</option>
        <option value="fr">צרפתית (Français)</option>
        <option value="ru">רוסית (Русский)</option>
    </select>
    <button onclick="sendToTranslate()">תרגם עבור הצד השני</button>
    <div id="resultBox" class="result"></div>
</div>
<script>
    function sendToTranslate() {
        const text = document.getElementById('userInput').value;
        const lang = document.getElementById('langSelect').value;
        const resultBox = document.getElementById('resultBox');
        if(!text || text.trim() === "") { alert("אנא הקלד טקסט לתרגום"); return; }
        resultBox.style.display = "block";
        resultBox.style.background = "#fff3cd";
        resultBox.style.color = "#856404";
        resultBox.innerHTML = "מתרגם כעת... אנא המתן";
        fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text, target_lang: lang })
        })
        .then(res => res.json())
        .then(data => {
            resultBox.style.display = "block";
            if(data.translated_text) {
                resultBox.style.background = "#d4edda";
                resultBox.style.color = "#155724";
                resultBox.innerHTML = `<strong>התרגום המוכן:</strong><br>${data.translated_text}`;
            } else {
                resultBox.style.background = "#f8d7da";
                resultBox.style.color = "#721c24";
                resultBox.innerHTML = "שגיאה בתרגום.";
            }
        }).catch(err => {
            resultBox.style.display = "block";
            resultBox.style.background = "#f8d7da";
            resultBox.style.color = "#721c24";
            resultBox.innerHTML = "שגיאה בתקשורת.";
        });
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    # מחזיר מיד את הדף המעוצב בלי לחפש תיקיות בכלל!
    return HTML_PAGE

@app.route('/translate', methods=['POST'])
def translate_chat():
    data = request.json or {}
    text_to_translate = data.get('text', '').strip()
    target_lang = data.get('target_lang', 'en')
    if not text_to_translate:
        return jsonify({'error': 'No text provided'}), 400
    try:
        encoded_text = urllib.parse.quote(text_to_translate)
        url = f"https://translated.net{encoded_text}&langpair=he|{target_lang}"
        response = requests.get(url, timeout=10)
        result_data = response.json()
        translated_text = result_data.get('responseData', {}).get('translatedText', '')
        return jsonify({'translated_text': translated_text or "לא נמצא תרגום"})
    except Exception as e:
        return jsonify({'translated_text': "שגיאה בחיבור"})

if __name__ == '__main__':
    app.run(debug=True, port=5009)
