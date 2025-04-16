from flask import Flask, render_template, jsonify
from datetime import datetime
import random
import nltk
import requests
from sklearn.ensemble import IsolationForest

nltk.download('punkt')

app = Flask(__name__)

def preprocess(posts):
    from nltk.tokenize import word_tokenize
    return [" ".join(word_tokenize(post.lower())) for post in posts if isinstance(post, str)]

def get_live_cyber_posts():
    api_key = "cc8b74ca866148ff929c1be49b963824"  
    url = f"https://newsapi.org/v2/everything?q=cybersecurity&apiKey={api_key}"
    try:
        res = requests.get(url)
        articles = res.json().get("articles", [])
        posts = [a.get("title", "") for a in articles[:5]]
        posts.append("Massive ransomware attack leaks bank data in the US")
        return posts
    except:
        return ["Could not fetch live news."]

def get_darkweb_posts():
    posts = [
        "Selling fresh credit card dumps from UK banks",
        "New zero-day exploit for Windows 11 available",
        "Cheap ransomware as a service for hire",
        "Selling 1M Facebook user accounts database",
        "Hacked PayPal accounts available",
        "Latest phishing kit for bank logins",
        "New botnet for DDoS attacks 500Gbps",
        "Exploit for Apache Log4j vulnerability",
        "Stealer malware targeting Android phones",
        "No threat, just a random discussion on dark web."
    ]
    return random.sample(posts, 7)

def extract_features(data):
    features, levels = [], []
    high = ["zero-day", "exploit", "ransomware", "botnet", "critical"]
    medium = ["hack", "phishing", "stealer", "malware"]
    low = ["leak", "database", "credit card"]
    for text in data:
        if "no threat" in text:
            features.append([len(text), 0])
            levels.append("Low")
            continue
        count, level = 0, "Low"
        if any(w in text for w in high):
            level, count = "High", 5
        elif any(w in text for w in medium):
            level, count = "Medium", 3
        elif any(w in text for w in low):
            count = 1
        features.append([len(text), count])
        levels.append(level)
    return features, levels

def build_model(X):
    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X)
    return model

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/live")
def api_live():
    posts = get_live_cyber_posts()
    keywords = ["attack", "ransomware", "exploit", "hack", "leak", "breach", "malware", "phishing"]
    return jsonify([
        {"post": post, "status": "Threat" if any(k in post.lower() for k in keywords) else "Safe"}
        for post in posts
    ])

@app.route("/api/darkweb/raw")
def api_raw():
    return jsonify(get_darkweb_posts())

@app.route("/api/darkweb")
def api_darkweb():
    posts = get_darkweb_posts()
    processed = preprocess(posts)
    features, levels = extract_features(processed)
    model = build_model(features)
    preds = model.predict(features)
    return jsonify([
        {
            "post": post,
            "status": "Threat" if pred == -1 else "Safe",
            "threat_level": level if pred == -1 else "-",
            "time": datetime.now().strftime("%H:%M:%S")
        }
        for post, pred, level in zip(posts, preds, levels)
    ])

if __name__ == "__main__":
    app.run(debug=True)
