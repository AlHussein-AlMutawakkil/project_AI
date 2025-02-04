from flask import Flask, request, render_template
import pickle
from security_model import extract_features
import pandas as pd

app = Flask(__name__)

# Load the model
with open('security_model', 'rb') as f:
    model = pickle.load(f)

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <title>تحليل أمان المواقع</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
        }
        .safe {
            background-color: #dff0d8;
            border: 1px solid #d6e9c6;
            color: #3c763d;
        }
        .danger {
            background-color: #f2dede;
            border: 1px solid #ebccd1;
            color: #a94442;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>تحليل أمان المواقع</h1>
        <form method="post">
            <div class="form-group">
                <input type="text" name="url" placeholder="أدخل رابط الموقع هنا" required>
            </div>
            <button type="submit">تحليل الموقع</button>
        </form>
        {% if result %}
        <div class="result {% if result == 'benign' %}safe{% else %}danger{% endif %}">
            <h3>نتيجة التحليل:</h3>
            <p>
                {% if result == 'benign' %}
                    ✅ الموقع آمن
                {% elif result == 'phishing' %}
                    ⚠️ تحذير: موقع تصيد محتمل
                {% elif result == 'defacement' %}
                    ⚠️ تحذير: موقع مشوه أو معدل
                {% elif result == 'malware' %}
                    ⚠️ تحذير: موقع يحتوي على برمجيات خبيثة
                {% endif %}
            </p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        features = extract_features(url)
        df = pd.DataFrame([features])
        result = model.predict(df)[0]
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
