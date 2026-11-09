import boto3

session = boto3.Session(
    profile_name="credit-risk-learning",
    region_name="ap-south-1",
)

sts = session.client("sts")
identity = sts.get_caller_identity()

print("AWS authentication successful!")
print("Account:", identity["Account"])
print("User ID:", identity["UserId"])
print("ARN:", identity["Arn"])