import boto3


LEAGUEFORM_BUCKET = "leagueform.com"


def upload_file(file_path):
    """Uploads the file with the given file_path to the leagueform.com Amazon S3 bucket."""
    boto3.client("s3").upload_file(file_path, LEAGUEFORM_BUCKET, file_path, ExtraArgs={"ContentType": "text/html"})


upload_file("stats.html")
