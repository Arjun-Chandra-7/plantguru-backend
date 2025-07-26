from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enables CORS for all domains

# ✅ Replace this with your actual PlantNet API key
API_KEY = "2b10NizC5IUi7rNLawqkIutNju"

@app.route('/')
def home():
    return jsonify({'message': '✅ PlantNet Flask API is live!'})

@app.route('/identify', methods=['POST'])
def identify():
    try:
        # Check if image part exists
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image = request.files['image']
        if image.filename == '':
            return jsonify({'error': 'Empty image file'}), 400

        # Prepare API request
        url = "https://my-api.plantnet.org/v2/identify/all"
        params = {"api-key": API_KEY}
        files = {
            'images': (image.filename, image.stream, image.content_type)
        }
        data = {
            'organs': 'leaf'  # or 'flower', 'fruit', 'bark', etc.
        }

        # Send request to PlantNet API
        response = requests.post(url, files=files, data=data, params=params)
        response.raise_for_status()
        result = response.json()

        # Extract top match
        if 'results' in result and result['results']:
            top = result['results'][0]
            species = top.get('species', {})
            latin = species.get('scientificNameWithoutAuthor', 'Unknown')
            common = species.get('commonNames', ['No common name'])[0]
            score = round(top.get('score', 0.0) * 100, 2)

            return jsonify({
                'plant': latin,
                'common': common.title(),
                'score': score
            })
        else:
            return jsonify({'error': 'No plant match found'}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Request to PlantNet failed', 'details': str(e)}), 502
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
