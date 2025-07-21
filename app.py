from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "2b10NizC5IUi7rNLawqkIutNju"  # Replace with your real PlantNet API key

@app.route('/')
def home():
    return '✅ Plant Identification API running!'

@app.route('/identify', methods=['POST'])
def identify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    url = "https://my-api.plantnet.org/v2/identify/all"
    params = {"api-key": API_KEY}
    files = {'images': (image.filename, image.stream, image.content_type)}
    data = {'organs': 'leaf'}

    try:
        response = requests.post(url, files=files, data=data, params=params)
        response.raise_for_status()
        result = response.json()

        if isinstance(result.get('results'), list) and result['results']:
            best_match = result['results'][0]
            species = best_match.get('species', {})

            latin_name = species.get('scientificNameWithoutAuthor') or species.get('scientificName') or "Unknown"
            common_names = species.get('commonNames', [])
            score = best_match.get('score', 0.0)

            return jsonify({
                'plant': latin_name,
                'common': common_names[0].title() if common_names else "No common name found",
                'score': round(score * 100, 2)
            })

        return jsonify({'error': 'No plant found'}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'API request failed', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # 🔥 This makes it visible on your local network (phones, laptops)
    app.run(host='0.0.0.0', port=port, debug=True)
