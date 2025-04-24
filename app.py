from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import zipfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CLIPBOARD_FILE = os.path.join(UPLOAD_FOLDER, 'clipboard.txt')

# --- Cleanup Functions ---

def delete_old_files():
    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename == 'clipboard.txt':
            continue
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            if now - os.path.getmtime(path) > 24 * 3600:
                os.remove(path)
                print(f"Deleted old file: {filename}")
        elif os.path.isdir(path):
            if now - os.path.getmtime(path) > 24 * 3600:
                os.rmdir(path)
                print(f"Deleted old directory: {filename}")

def delete_clipboard():
    if os.path.exists(CLIPBOARD_FILE):
        if time.time() - os.path.getmtime(CLIPBOARD_FILE) > 4 * 3600:
            os.remove(CLIPBOARD_FILE)
            print("Deleted old clipboard.txt")

# --- Scheduler Setup ---

scheduler = BackgroundScheduler(timezone=pytz.UTC)
scheduler.add_job(delete_old_files, trigger='interval', hours=1)
scheduler.add_job(delete_clipboard, trigger='interval', hours=1)

# --- Clipboard Helpers ---

def read_clipboard():
    if os.path.exists(CLIPBOARD_FILE):
        with open(CLIPBOARD_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

def write_clipboard(content):
    with open(CLIPBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

# --- Utility ---

def get_next_bundle_name():
    base_name = "bundle"
    count = 1
    while True:
        name = f"{base_name}_{count:02d}.zip"
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, name)):
            return name
        count += 1

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'clipboard' in request.form:
        content = request.form['clipboard']
        write_clipboard(content)
        return redirect(url_for('index'))

    files = [f for f in os.listdir(UPLOAD_FOLDER) if f != 'clipboard.txt']
    clipboard_text = read_clipboard()
    return render_template('index.html', files=files, clipboard=clipboard_text)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    files = request.files.getlist('file')
    bundle_name = request.form.get('bundle_name')
    create_bundle = request.form.get('create_bundle') == 'true'

    if create_bundle and not bundle_name:
        bundle_name = get_next_bundle_name()

    if create_bundle:
        zip_path = os.path.join(UPLOAD_FOLDER, bundle_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                if file.filename:
                    filename = '/'.join([secure_filename(part) for part in file.filename.split('/')]).lstrip('/')
                    zipf.writestr(filename, file.read())
    else:
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))

    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if filename == 'clipboard.txt':
        return "Cannot delete clipboard via this route", 403
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(path):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    return "File not found", 404

@app.route('/preview/<filename>')
def preview_file(filename):
    allowed = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    if filename.split('.')[-1].lower() in allowed:
        return send_from_directory(UPLOAD_FOLDER, filename)
    return "Preview not allowed for this file type.", 403

# --- Start App ---

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=5050, debug=True)