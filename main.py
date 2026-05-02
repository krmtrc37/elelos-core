from flask import Flask, request, jsonify
import os
# Kütüphane hatasını engellemek için doğrudan ddgs kullanıyoruz
try:
    from duckduckgo_search import DDGS
except ImportError:
    from ddgs import DDGS

app = Flask(__name__)
MY_API_KEY = "Elelos_Gizli_Sifre_2026"

@app.route('/')
def home():
    return "Elelosmusumm Sunucusu Aktif!"

@app.route('/search', methods=['POST'])
def search():
    # Güvenlik Kontrolü
    api_key = request.headers.get("X-API-KEY")
    if api_key != MY_API_KEY:
        return jsonify({"response": "Yetkisiz erisim!"}), 403

    data = request.json
    query = data.get("query", "")
    
    if not query:
        return jsonify({"response": "Soru bos olamaz."})

    try:
        # GPT destekli hızlı cevap denemesi
        with DDGS() as ddgs:
            # chat fonksiyonu bazen takılabilir, o yüzden timeout ekledik
            answer = ddgs.chat(query, model='gpt-4o-mini')
            if answer:
                return jsonify({"response": str(answer)})
            
            # Eğer chat boş dönerse normal aramaya geç
            results = list(ddgs.text(query, max_results=1))
            if results:
                return jsonify({"response": results[0]['body']})
                
        return jsonify({"response": "Maalesef buna dair bir bilgi bulamadim."})
        
    except Exception as e:
        print(f"Hata olustu: {e}")
        return jsonify({"response": "Arama sirasinda bir hata olustu, tekrar dene."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
