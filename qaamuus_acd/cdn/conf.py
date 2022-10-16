import os

from decouple import config
AWS_ACCESS_KEY_ID="DO00QBBDKQZHJH7DX3G6"
AWS_SECRET_ACCESS_KEY= "zyb8shFkk/69XwBOKOhjqEor9yw/NwOeEF/aJlKK+wo"
AWS_STORAGE_BUCKET_NAME="qaamuusstaticfiles"
AWS_S3_ENDPOINT_URL="https://sgp1.digitaloceanspaces.com"

AWS_S3_OBJECT_PARAMETERS={
    "CacheControl": "max-age=86400",
     "ACL": "public-read"
}

AWS_LOCATION="https://qaamuusstaticfiles.sgp1.digitaloceanspaces.com"

DEFAULT_FILE_STORAGE = "qaamuus_acd.cdn.backends.MediaRootS3Boto3Storage"
# STATICFILES_STORAGE = "qaamuus_acd.cdn.backends.StaticRootS3Boto3Storage"