from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Connect to Railway Postgres
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

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

    fields = (
        data.get('nombre'),
        data.get('personas'),
        data.get('bus_ida'),
        data.get('bus_vuelta'),
        data.get('hora_marcha'),
        data.get('alergia'),
        data.get('detalle_alergia')
    )

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO formulario (nombre, personas, bus_ida, bus_vuelta, hora_marcha, alergia, detalle_alergia)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    ''', fields)
    conn.commit()
    cur.close()
    conn.close()

    return {'status': 'success'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
