from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from flask_cors import CORS
import os

# Your imports from local src files
from src.plant_data import handle_query, get_plants_dict, DEFAULT_USER_UID

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS globally (for chatbot access across devices)

# =======================
#      PAGE ROUTES
# =======================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/purpose.html")
def purpose_html():
    return render_template("purpose.html")

@app.route("/auth.html")
def auth_html():
    return render_template("auth.html")

@app.route('/count.html')
def count_html():
    user_uid = session.get('user_uid', DEFAULT_USER_UID)
    if get_plants_dict(uid=user_uid):
         return render_template("dashboard.html")
    else:
        return render_template("count.html")

@app.route('/upload.html')
def upload_html():
    user_uid = session.get('user_uid', DEFAULT_USER_UID)
    if get_plants_dict(uid=user_uid):
        return render_template("dashboard.html")
    else:
        return render_template("upload.html")

@app.route("/dashboard.html")
def dashboard_html():
    return render_template("dashboard.html")

@app.route("/search")
def search_page():
    return render_template("search.html")

@app.route("/voice_assistant")
def voice_assistant_html():
    return render_template("voice_assistant.html")

@app.route('/plant_db_public.json')
def plant_db_public():
    return send_from_directory('.', 'plant_database.json', mimetype='application/json')

# =======================
#      CHATBOT API
# =======================

@app.route("/ask", methods=["POST"])
def ask():
    """POST { query: ... } → AI chatbot response."""
    user_input = request.json.get("query")
    response = handle_query(user_input, uid=DEFAULT_USER_UID)
    return jsonify({"response": response})

# =======================
#      MAIN ENTRY
# =======================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
