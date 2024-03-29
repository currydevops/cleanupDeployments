import boto3
import time


def upload_file(bucket_name, file_key, file_contents):
    try:
        session = boto3.Session(profile_name='localstack')
        s3_client = session.client('s3', endpoint_url='http://localhost:4566')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=file_contents
        )
        print(f"Uploaded file '{file_key}' successfully.")
    except Exception as e:
        print(f"Failed to upload file '{file_key}'. Error: {e}")


def create_sample_data(bucket_name):
    # Upload sample files to the bucket with sleep between uploads
    upload_delay = 5  # Adjust the delay as needed (in seconds)

    upload_file(bucket_name, 'deployhash112/index.html', '<html><body><h1>Hello, World!</h1></body></html>')
    upload_file(bucket_name, 'deployhash112/css/font.css', 'body { font-family: Arial, sans-serif; }')
    upload_file(bucket_name, 'deployhash112/images/hey.png', 'binary_data_of_hey.png')
    time.sleep(upload_delay)

    upload_file(bucket_name, 'dsfsfsl9074/root.html', '<html><body><h1>Welcome!</h1></body></html>')
    upload_file(bucket_name, 'dsfsfsl9074/styles/font.css', 'h1 { color: blue; }')
    upload_file(bucket_name, 'dsfsfsl9074/img/hey.png', 'binary_data_of_hey.png')
    time.sleep(upload_delay)

    upload_file(bucket_name, 'delkjlkploy3/base.html', '<html><body><p>This is a base page.</p></body></html>')
    upload_file(bucket_name, 'delkjlkploy3/fonts/font.css', 'p { font-size: 16px; }')
    upload_file(bucket_name, 'delkjlkploy3/png/hey.png', 'binary_data_of_hey.png')
    time.sleep(upload_delay)

    # Additional deployments
    upload_file(bucket_name, 'klljkjkl123/index.html',
                '<html><body><h1>Hello, World from klljkjkl123!</h1></body></html>')
    upload_file(bucket_name, 'klljkjkl123/css/font.css', 'body { font-family: Arial, sans-serif; }')
    upload_file(bucket_name, 'klljkjkl123/images/hey.png', 'binary_data_of_hey.png')
    time.sleep(upload_delay)

    upload_file(bucket_name, 'dsfff1234321/root.html', '<html><body><h1>Welcome to dsfff1234321!</h1></body></html>')
    upload_file(bucket_name, 'dsfff1234321/styles/font.css', 'h1 { color: blue; }')
    upload_file(bucket_name, 'dsfff1234321/img/hey.png', 'binary_data_of_hey.png')
    time.sleep(upload_delay)


if __name__ == "__main__":
    bucket_name = 'deployments'

    # Upload sample data to the bucket with sleep between uploads
    create_sample_data(bucket_name)
