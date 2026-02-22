from flask import Flask, render_template, request
import requests
import os
import re

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

def shorten_url(url):
    # Coba TinyURL dulu (gratis, no key)
    try:
        r = requests.get(
            f"https://tinyurl.com/api-create.php",
            params={"url": url},
            timeout=10
        )
        if r.status_code == 200 and r.text.startswith("http"):
            return {"short": r.text.strip(), "provider": "TinyURL"}
    except Exception as e:
        print(f"TinyURL error: {e}")

    # Fallback: is.gd
    try:
        r = requests.get(
            "https://is.gd/create.php",
            params={"format": "simple", "url": url},
            timeout=10
        )
        if r.status_code == 200 and r.text.startswith("http"):
            return {"short": r.text.strip(), "provider": "is.gd"}
    except Exception as e:
        print(f"is.gd error: {e}")

    return None

def is_valid_url(url):
    return re.match(r'https?://.+\..+', url) is not None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    input_url = ""

    if request.method == "POST":
        input_url = request.form.get("url", "").strip()
        if not input_url:
            error = "Masukkan URL terlebih dahulu."
        elif not is_valid_url(input_url):
            error = "URL tidak valid. Pastikan URL diawali dengan http:// atau https://"
        elif len(input_url) > 2000:
            error = "URL terlalu panjang."
        else:
            result = shorten_url(input_url)
            if not result:
                error = "Gagal mempersingkat URL. Coba lagi."

    return render_template("index.html", result=result, error=error, input_url=input_url)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run(debug=True)
