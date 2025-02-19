from flask import Flask, request, send_from_directory, render_template, redirect, url_for, send_file
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import zipfile
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Auto-delete files after 24 hours
def delete_old_files():
    now = time.time()
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if now - file_mtime > 24 * 3600:
                os.remove(file_path)
                print(f"Deleted old file: {filename}")
        elif os.path.isdir(file_path):
            dir_mtime = os.path.getmtime(file_path)
            if now - dir_mtime > 24 * 3600:
                os.rmdir(file_path)
                print(f"Deleted old bundle: {filename}")

scheduler = BackgroundScheduler(timezone=pytz.UTC)  # Use UTC timezone (or your preferred timezone)
scheduler.add_job(func=delete_old_files, trigger='interval', hours=1)

def get_next_bundle_name():
    base_name = "bundle"
    count = 1
    while True:
        bundle_name = f"{base_name}_{count:02d}.zip"
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, bundle_name)):
            return bundle_name
        count += 1

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    files = request.files.getlist('file')
    bundle_name = request.form.get('bundle_name')
    create_bundle = request.form.get('create_bundle') == 'true'

    if create_bundle and not bundle_name:
        bundle_name = get_next_bundle_name()

    # Create zip file instead of a folder
    if create_bundle:
        zip_path = os.path.join(UPLOAD_FOLDER, bundle_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                if file.filename == '':
                    continue
                filename = secure_filename(file.filename)
                zipf.writestr(filename, file.read())  # Write file content directly into the zip
    else:
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    else:
        return "File not found", 404

@app.route('/preview/<filename>')
def preview_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    file_ext = filename.split('.')[-1].lower()
    if file_ext not in allowed_extensions:
        return "Preview not allowed for this file type.", 403
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
