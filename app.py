from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_ip_info', methods=['GET'])
def get_ip_info():
    api_url = 'https://ipapi.co/json/'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        ip_info = response.json()
        return jsonify(ip_info)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
