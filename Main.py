import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
# Tambahkan baris ini (bebas isi string apa saja)
app.secret_key = 'temukampus_unesa_secret_key_2026'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('MYSQLHOST', 'localhost'),
        user=os.getenv('MYSQLUSER', 'root'),
        password=os.getenv('MYSQLPASSWORD', ''),
        database=os.getenv('MYSQLDATABASE', 'temukampus'),
        port=int(os.getenv('MYSQLPORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. KETIKA SUBMIT LAPORAN
    if request.method == 'POST':
        status = request.form.get('status_laporan')
        nama_barang = request.form.get('nama_barang')
        lokasi = request.form.get('lokasi')
        nomor_kontak = request.form.get('nomor_kontak')
        
        file = request.files.get('foto_barang')
        foto_path = "https://images.unsplash.com/photo-1563214561-1372b647f12c?auto=format&fit=crop&w=400&q=80"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_save_path)
            foto_path = f"/uploads/{filename}"

        insert_query = "INSERT INTO laporan (id_kategori, status_laporan, nama_barang, lokasi, nomor_kontak, foto_barang) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (1, status, nama_barang, lokasi, nomor_kontak, foto_path))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    # 2. PENCARIAN & FILTER
    search_query = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()

    sql = "SELECT * FROM laporan WHERE 1=1"
    params = []

    if search_query:
        sql += " AND (nama_barang LIKE %s OR lokasi LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if status_filter in ['hilang', 'ditemukan', 'selesai']:
        sql += " AND status_laporan = %s"
        params.append(status_filter)

    sql += " ORDER BY created_at DESC"

    cursor.execute(sql, tuple(params))
    laporan_list = cursor.fetchall()

    # FORMAT TIMESTAMP
    for item in laporan_list:
        if item.get('created_at'):
            item['waktu_format'] = item['created_at'].strftime("%d %b %Y, %H:%M WIB")
        else:
            item['waktu_format'] = "-"

    # 3. QUERY STATISTIK MINI (DENGAN STRING BIASA)
    stats_query = "SELECT COALESCE(SUM(CASE WHEN status_laporan = 'hilang' THEN 1 ELSE 0 END), 0) AS total_hilang, COALESCE(SUM(CASE WHEN status_laporan = 'ditemukan' THEN 1 ELSE 0 END), 0) AS total_ditemukan, COALESCE(SUM(CASE WHEN status_laporan = 'selesai' THEN 1 ELSE 0 END), 0) AS total_selesai FROM laporan"
    cursor.execute(stats_query)
    stats_data = cursor.fetchone()

    statistik = {
        'hilang': int(stats_data['total_hilang']) if stats_data else 0,
        'ditemukan': int(stats_data['total_ditemukan']) if stats_data else 0,
        'selesai': int(stats_data['total_selesai']) if stats_data else 0
    }

    cursor.close()
    conn.close()

    return render_template(
        'index.html', 
        feed_barang=laporan_list, 
        current_search=search_query, 
        current_status=status_filter,
        stats=statistik
    )

# ROUTE TANDAI SELESAI
@app.route('/selesai/<int:id_laporan>', methods=['POST'])
def tandai_selesai(id_laporan):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE laporan SET status_laporan = 'selesai' WHERE id_laporan = %s", (id_laporan,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# ROUTE HAPUS LAPORAN
@app.route('/hapus/<int:id_laporan>', methods=['POST'])
def hapus_laporan(id_laporan):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT foto_barang FROM laporan WHERE id_laporan = %s", (id_laporan,))
    item = cursor.fetchone()
    if item and item['foto_barang'] and item['foto_barang'].startswith('/uploads/'):
        filename = item['foto_barang'].replace('/uploads/', '')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    cursor.execute("DELETE FROM laporan WHERE id_laporan = %s", (id_laporan,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)