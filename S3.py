import boto3

def get_env_var():
    load_dotenv('s3_bucket.env')
    POSTGRES_USER = os.getenv('aws_access_key_id')
    POSTGRES_PASSWORD = os.getenv('aws_secret_access_key')
    POSTGRES_DB = os.getenv('region_name')
    return aws_access_key_id, aws_secret_access_key, region_name

def connect_bucket(aws_access_key_id, aws_secret_access_key, region_name):
    s3 = boto3.resource(
        's3',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name = region_name
    )
    return s3

def upload_data(s3, bucket, data, filename):
    s3.Bucket('my-bucket').put_object(Key=filename, Body=data)