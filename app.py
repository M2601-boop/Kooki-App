from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    # מציג את מסך שיחת התרגום למשתמש
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_chat():
    data = request.json
    text_to_translate = data.get('text', '')
    target_lang = data.get('target_lang', 'en') # ברירת מחדל לאנגלית
    
    if not text_to_translate:
        return jsonify({'error': 'No text provided'}), 400
        
    try:
        # מבצע את התרגום האוטומטי
        translated = translator.translate(text_to_translate, dest=target_lang)
        return jsonify({
            'original_text': text_to_translate,
            'translated_text': translated.text,
            'detected_lang': translated.src
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
