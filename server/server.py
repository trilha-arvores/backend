import mimetypes

from services import FlaskService, DirectoryService
from controllers import trails_controller, admin_controller
from flask_cors import CORS
from flask import request, jsonify
from minio import Minio
from minio.error import S3Error
import os

FlaskService.setup_app()
app = FlaskService.app
CORS(app)

minio_client = Minio(
    "minio:9000",
    access_key="YEv9LUqnG9Q87TPj7cbI",
    secret_key="62ijOcUlbkIKs20jm0l8TiZUYtHC3ESDkcuOVErZ",
    secure=False
)

bucket_name = "mybucket"

# Create bucket if it does not exist
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)


app.register_blueprint(trails_controller, url_prefix="/trails")
app.register_blueprint(admin_controller, url_prefix="/admin")


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {}, 200


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_name = file.filename
    tmp_dir = DirectoryService.absolute_path_from_project('tmp')
    file_path = os.path.join(tmp_dir, file_name)
    file.save(file_path)

    # Determine the file's content type
    content_type, _ = mimetypes.guess_type(file_name)

    try:
        # Upload the file with the correct content type
        minio_client.fput_object(
            bucket_name,
            file_name,
            file_path,
            content_type=content_type
        )

        os.remove(file_path)  # Remove the file after upload
        return jsonify({"message": "File uploaded successfully"}), 200
    except S3Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/getUrl/<file_name>', methods=['GET'])
def download_file(file_name):
    # Generate a pre-signed URL valid for 7 days
    url = minio_client.presigned_get_object(bucket_name, file_name)

    return jsonify(url), 200


if __name__ == "__main__":
    FlaskService.run_app()
