from flask import Flask, request, render_template, redirect, url_for
from google.cloud import storage
import os

app = Flask(__name__)

# Configure the GCS bucket name
GCS_BUCKET_NAME = "bucket-salesdata"

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Upload file to Google Cloud Storage
            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
            return f"File {file.filename} uploaded to GCS bucket {GCS_BUCKET_NAME} successfully."
    return render_template('index.html')

if __name__ == "__main__":
    # Ensure the environment variable for the GCS service account key is set
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'
    app.run(debug=True)
