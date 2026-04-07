from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # הפונקציה הזו אומרת לפייתון לחפש את הקובץ index.html בתוך תיקיית templates
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
