import string
import random
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
url_database = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()
        url_database[short_code] = long_url
        short_url = request.host_url + short_code
    return render_template_string('''
        <h2>Simple URL Shortener</h2>
        <form method="POST">
            Enter Long URL: <input type="text" name="long_url" style="width:300px;" required>
            <input type="submit" value="Shorten">
        </form>
        {% if short_url %}
            <p>Shortened URL: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a></p>
        {% endif %}
    ''', short_url=short_url)

@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = url_database.get(short_code)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
