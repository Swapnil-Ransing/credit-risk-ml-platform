
from pathlib import Path
import boto3

AWS_PROFILE = "credit-risk-learning"
AWS_REGION = "ap-southeast-2"

BUCKET_NAME = "credit-risk-learning-184286897267"

LOCAL_FILE = Path(
    "data/raw/sample_credit_applications.csv"
)

S3_KEY = "raw/sample_credit_applications.csv"


def get_s3_client():
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )
    return session.client("s3")


def upload_file():
    if not LOCAL_FILE.exists():
        raise FileNotFoundError(LOCAL_FILE)

    s3 = get_s3_client()

    s3.upload_file(
        str(LOCAL_FILE),
        BUCKET_NAME,
        S3_KEY,
    )

    print(f"Uploaded to s3://{BUCKET_NAME}/{S3_KEY}")
    

def download_file():
    s3 = get_s3_client()

    destination = Path(
        "data/processed/downloaded_sample.csv"
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    s3.download_file(
        BUCKET_NAME,
        S3_KEY,
        str(destination),
    )

    print("Downloaded:", destination)
    
def inspect_object():
    s3 = get_s3_client()

    response = s3.head_object(
        Bucket=BUCKET_NAME,
        Key=S3_KEY,
    )

    print("Object size:", response["ContentLength"])
    print("Encryption:", response.get("ServerSideEncryption"))
    print("Last modified:", response["LastModified"])


if __name__ == "__main__":
    # upload_file()
    # download_file()
    inspect_object()