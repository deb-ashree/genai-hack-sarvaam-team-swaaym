import base64
import json
import logging
import os, requests,time
from dotenv import load_dotenv
import boto3, botocore
from botocore.config import Config

load_dotenv(os.getcwd()+"/course_creation/local.env")       #/course_creation

# client = Groq(
#     # This is the default and can be omitted
#     api_key=os.getenv("GROQ_API_KEY")
# )

did_api_key = os.getenv("D-ID_API_KEY")

model_gpt="gpt-4o-mini"
model_mixtral="mixtral-8x7b-32768"
model_llama="llama3" #"llama3-8b-8192"
model_tts="tts-1"
model_stt="whisper-1"
#os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY")
# groqLLM_llama = ChatGroq(
#     api_key=os.environ.get("GROQ_API_KEY"), model=model_llama, temperature=0
# )

def makeDir(dirName):
    os.makedirs(dirName,  exist_ok=True)

def getFilePath(path, fileName):
    return os.path.join(path, fileName)

def getS3FilePath(fileName):
    s3_client = boto3.resource(service_name='s3', region_name='us-west-2',
         aws_access_key_id=os.getenv("ACCESS_ID"),
         aws_secret_access_key= os.getenv("ACCESS_KEY"))
    # print(s3_client.meta.client.list_buckets())
    BUCKET = "gen-ai-data"
    print("Uploading to S3 : "+fileName)
    result = s3_client.meta.client.upload_file(Filename=fileName,Bucket=BUCKET,Key=os.path.basename(fileName)) #dest_prefix + 
    # result = s3_client.Bucket(BUCKET).upload_file(fileName, os.path.basename(fileName))
    print(result)
    response = s3_client.Object(BUCKET, os.path.basename(fileName)).get()
    print(response["ResponseMetadata"]["HTTPStatusCode"]) 

    my_config = Config(signature_version = botocore.UNSIGNED)
    url = boto3.client("s3", config=my_config).generate_presigned_url("get_object", ExpiresIn=0, Params={"Bucket": BUCKET, "Key": os.path.basename(fileName)})
    print(url)
    return url

def getGCSFilePath(fileName):
    return
    ## To Be Implemented
    #return url

    # import pandas as pd
    # from io import StringIO
    # or
    # obj = s3.Bucket(BUCKET).Object('foo.csv').get()
    # foo = pd.read_csv(obj['Body'], index_col=0)
    # content = bucket.get_key(fileName).get_contents_as_string()
    # reader = pd.read_csv(StringIO.StringIO(content))

def main():
    getS3FilePath(os.getcwd()+"/Instructor3.jpeg")

if __name__ == "__main__":
     main()

