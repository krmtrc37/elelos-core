from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import os

app = Flask(__name__)
MY_API_KEY = "Elelos_Gizli_Sifre_2026"

@app.route('/')
def home():
    return "Elelosmusumm Sistemi Aktif!"

@app.route('/search', methods=['POST'])
def search():
    api_key = request.headers.get("X-API-KEY")
    if api_key != MY_API_KEY:
        return jsonify({"error": "Yetkisiz erisim!"}), 403
    data = request.json
    query = data.get("query", "")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            return jsonify({"response": results[0]['body'] if results else "Bilgi bulamadim."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
