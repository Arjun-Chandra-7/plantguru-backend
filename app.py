from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from plant_common_names import latin_to_english # ✅ Import from your separate file

app = Flask(__name__)
CORS(app)

API_KEY = "2b10NizC5IUi7rNLawqkIutNju"

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

        if 'results' in result and result['results']:
            best_match = result['results'][0]
            species = best_match.get('species', {})
            latin_name = species.get('scientificNameWithoutAuthor', 'Unknown')
            common_names = species.get('commonNames', [])

            # Try to find an English common name
            english_name = None
            for name in common_names:
                if name.isascii() and name.strip() and not any(c in name for c in 'éèçαλ'):
                    english_name = name.title()
                    break

            # Use dictionary fallback if needed
            if not english_name:
                english_name = latin_to_common.get(latin_name, "No English name found")

            return jsonify({
                'plant': latin_name,
                'common': english_name,
                'score': round(best_match.get('score', 0.0) * 100, 2)
            })

        return jsonify({'error': 'No plant found'}), 404

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'API request failed', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
