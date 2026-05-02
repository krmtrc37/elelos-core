from flask import Flask, request, jsonify
import os
import logging

# DuckDuckGo kütüphanesini en güvenli şekilde içe aktar
try:
    from duckduckgo_search import DDGS
except ImportError:
    # Eğer kütüphane ismi değişmişse alternatif olarak ddgs dene
    try:
        from ddgs import DDGS
    except ImportError:
        DDGS = None

app = Flask(__name__)

# Güvenlik Anahtarı (Roblox tarafındakiyle aynı olmalı)
MY_API_KEY = "Elelos_Gizli_Sifre_2026"

@app.route('/')
def home():
    return "Elelosmusumm API Sistemi Aktif! Baglanti saglandi."

@app.route('/search', methods=['POST'])
def search():
    # 1. Güvenlik Kontrolü
    api_key = request.headers.get("X-API-KEY")
    if api_key != MY_API_KEY:
        return jsonify({"response": "Yetkisiz erisim hatasi!"}), 403

    # 2. Veri Kontrolü
    data = request.json
    if not data or "query" not in data:
        return jsonify({"response": "Sorgu gonderilmedi."}), 400

    query = data.get("query", "")
    print(f"Gelen Sorgu: {query}")

    if not DDGS:
        return jsonify({"response": "Arama kütüphanesi yüklü degil."}), 500

    try:
        with DDGS() as ddgs:
            # ÖNCE: Yapay zeka (Chat) cevabı dene (En mantıklı cevap budur)
            try:
                # model='gpt-4o-mini' en hızlı ve stabil olanıdır
                answer = ddgs.chat(query, model='gpt-4o-mini')
                if answer and len(str(answer)) > 5:
                    return jsonify({"response": str(answer)})
            except Exception as chat_error:
                print(f"Chat hatasi: {chat_error}, normal aramaya geciliyor...")

            # SONRA: Eğer Chat çalışmazsa normal web araması yap
            results = list(ddgs.text(query, max_results=1))
            if results and 'body' in results[0]:
                return jsonify({"response": results[0]['body']})
            
            return jsonify({"response": "Maalesef buna dair bir bilgi bulamadim."})

    except Exception as e:
        print(f"Genel Hata: {e}")
        return jsonify({"response": "Arama sirasinda teknik bir sorun oluştu."}), 500

if __name__ == "__main__":
    # Render port ayarı
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
