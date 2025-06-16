from google.cloud import storage


credentials_path = "/home/kevin/projects/tread-events-python/tread-media-f50f10bbaaf3.json"
bucket_name= "tread_media_images"

def upload_to_bucket(
    source_file_path, destination_blob_name
):
    # Initialize the client with credentials
    storage_client = storage.Client.from_service_account_json(credentials_path)

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a blob object from the bucket
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to {destination_blob_name}.")


# upload_to_bucket(
#     "tread_media_images",
#     "/home/kevin/projects/tread-events-python/notes.txt",
#     "notes.txt",
# )
