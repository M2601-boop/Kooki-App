from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_chat():
    data = request.json
    text_to_translate = data.get('text', '')
    target_lang = data.get('target_lang', 'en')
    
    if not text_to_translate:
        return jsonify({'error': 'No text provided'}), 400
        
    try:
        # שימוש במנוע תרגום פתוח ויציב (MyMemory API) שאינו דורש הרשמה
        url = f"https://translated.net{text_to_translate}&langpair=he|{target_lang}"
        response = requests.get(url).json()
        translated_text = response.get('responseData', {}).get('translatedText', '')
        
        if not translated_text:
            translated_text = "שגיאה בקבלת התרגום. נסה שוב."
            
        return jsonify({
            'original_text': text_to_translate,
            'translated_text': translated_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
