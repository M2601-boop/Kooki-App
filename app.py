from flask import Flask, render_template, request, jsonify
import requests
import urllib.parse
import os

# הגדרה שאומרת לפייתון לחפש את הקבצים בכל מקום בפרויקט
app = Flask(__name__, template_folder='.', static_folder='.')

@app.route('/')
def home():
    # בודק אם הקובץ נמצא בתיקיית templates או בעמוד הראשי
    if os.path.exists('templates/index.html'):
        return render_template('templates/index.html')
    elif os.path.exists('index.html'):
        return render_template('index.html')
    else:
        return "שגיאה: קובץ הממשק index.html לא נמצא בפרויקט שלך!", 404

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
    # מפעיל אוטומטית על פורט פתוח ובטוח
    app.run(debug=True, port=5005)
