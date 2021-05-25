from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import csv
import os

app = Flask(__name__)
CORS(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ameertsec'

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

mysql = MySQL(app)

@app.route('/api/upload', methods=['POST'])
def index():
    cur = mysql.connection.cursor()

    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file_name = os.path.basename(file_path)
    
    file.save(file_path)
    cur.execute('INSERT INTO files(filename) VALUES(%s)',(os.path.splitext(file_name)[0],))
    mysql.connection.commit()

    cur.execute('SELECT LAST_INSERT_ID() FROM files')
    last_id_inserted = cur.fetchone()
    with open(file_path) as csv_file:
        csvs = csv.reader(csv_file, delimiter=',')

        for row in csvs:
            cur.execute('INSERT INTO datas(file_id, fName, lName, salary) VALUES(%s,%s,%s,%s)', (last_id_inserted[0], row[0], row[1], row[2],))
        mysql.connection.commit()
    cur.close()

    return jsonify({'success': True, 'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)