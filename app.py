# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

PLANTNET_API_KEY = "2b10jzAcrteKEXCPI5pdX8edzu"
PLANTNET_API_URL = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_API_KEY}"

@app.route('/identify', methods=['POST'])
def identify_plant():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    files = {
        'images': (image_file.filename, image_file.stream, image_file.mimetype)
    }

    response = requests.post(PLANTNET_API_URL, files=files)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to identify plant'}), 500

    data = response.json()
    if not data.get('results'):
        return jsonify({'plant': None, 'message': 'No plant identified'}), 200

    top_result = data['results'][0]
    plant_name = top_result['species']['scientificNameWithoutAuthor']
    score = round(top_result['score'] * 100, 2)
    images = top_result.get('images')
    image_url = images[0]['url'].replace("&amp;", "&") if images else None

    return jsonify({
        'plant': plant_name,
        'score': score,
        'image': image_url
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
