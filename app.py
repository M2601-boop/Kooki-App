from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_chat():
    data = request.json or {}
    text_to_translate = data.get('text', '').strip()
    target_lang = data.get('target_lang', 'en')
    
    if not text_to_translate:
        return jsonify({'error': 'No text provided'}), 400
        
    try:
        # מקודד את הטקסט בעברית בצורה בטוחה כדי שלא יגרום לשגיאה 400
        encoded_text = urllib.parse.quote(text_to_translate)
        
        # שימוש בכתובת תרגום ישירה ויציבה
        url = f"https://translated.net{encoded_text}&langpair=he|{target_lang}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({'translated_text': f"שגיאת שרת: {response.status_code}"})
            
        result_data = response.json()
        translated_text = result_data.get('responseData', {}).get('translatedText', '')
        
        if not translated_text:
            translated_text = "לא נמצא תרגום, נסה שוב."
            
        return jsonify({
            'original_text': text_to_translate,
            'translated_text': translated_text
        })
    except Exception as e:
        return jsonify({'translated_text': f"שגיאה בתקשורת: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
