from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    def safe_select(query, attr='text'):
        el = soup.select_one(query)
        if el:
            return el.get(attr) if attr != 'text' else el.text.strip()
        return None

    result = {
        "title": safe_select('h2#hp_hotel_name'),
        "address": safe_select('span.hp_address_subtitle'),
        "rating": safe_select('div.b5cd09854e.d10a6220b4'),
        "review_count": safe_select('div._9c5f726ffb span'),
        "price": safe_select('div.f6431b446c.fbfd7c1165'),
        "image": next((img.get('src') for img in soup.select('img.hotel_image') if img.get('src')), None)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run()
