from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import csv
import os

app = Flask(__name__)
DATA_FILE = 'data/submissions.csv'

# Ensure data folder exists
os.makedirs('data', exist_ok=True)

@app.route('/')
def index():
    pdfs = os.listdir('static')
    pdfs = [pdf for pdf in pdfs if pdf.endswith('.pdf')]
    return render_template('index.html', pdfs=pdfs)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=True)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    fields = [
        data.get('nombre'),
        data.get('personas'),
        data.get('bus_ida'),
        data.get('bus_vuelta'),
        data.get('hora_marcha'),
        data.get('alergia'),
        data.get('detalle_alergia')
    ]

    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    return {'status': 'success'}, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
