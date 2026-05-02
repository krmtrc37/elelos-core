from flask import Flask, request, jsonify
from duckduckgo_search import DDGS
import os

app = Flask(__name__)

# Şifreyi burada kontrol et
MY_API_KEY = "Elelos_Gizli_Sifre_2026"

@app.route('/')
def home():
    return "Elelosmusumm Sistemi Aktif! Baglanti basarili."

@app.route('/search', methods=['POST', 'GET']) # GET ekledik ki tarayıcıdan bakınca hata vermesin
def search():
    if request.method == 'GET':
        return "Search hatti calisiyor, ama Roblox'tan veri bekliyorum."
        
    api_key = request.headers.get("X-API-KEY")
    if api_key != MY_API_KEY:
        return jsonify({"error": "Yetkisiz erisim!"}), 403

    data = request.json
    if not data:
        return jsonify({"error": "Veri gonderilmedi"}), 400
        
    query = data.get("query", "")
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results:
                return jsonify({"response": results[0]['body']})
            return jsonify({"response": "Maalesef buna dair bir bilgi bulamadim."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
