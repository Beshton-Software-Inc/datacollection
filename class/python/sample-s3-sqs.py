import traceback
import logging
import time
import json 
import collections 
import sys 
import os
import re 
import boto3
import requests

output_handler = logging.StreamHandler()
formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
output_handler.setFormatter(formatter)
LOG = logging.getLogger()
while len(LOG.handlers) > 0:
    LOG.handlers.pop()
LOG.addHandler(output_handler) 
LOG.setLevel(logging.INFO)
LOG.propagate = False 

SQS_QUEUE_URL_PREFIX = os.getenv("SQS_QUEUE_URL_PREFIX","https://sqs.us-west-1.amazonaws.com/700188841304/")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME","coldword-cstage-test1")
SQS_QUEUE_URL = "%s%s"%(SQS_QUEUE_URL_PREFIX,SQS_QUEUE_NAME) 
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "webex-ai-meeting-assets-cstage-uswest2-0")
REGION = os.getenv("REGION", "us-west-1")  
aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')

class s3sqsDemo(threading.Thread):
    
    def __init__(self, name, queue=None):
        super().__init__(group=None, name=name)
        self.__name__ = name
        LOG.info({"message":"Initializing endpoint sharder %s on process %s" % (SQS_QUEUE_URL, name) } )
        self.__sqs__ = boto3.client(
            'sqs',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID',''),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY',''),
            region_name=REGION)
        self.__s3__ = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID',''),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY',''),
            region_name=REGION) 
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "") =="":
            credential = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
            with open('/tmp/gsa.json', 'wb') as outfile:
                outfile.write(base64.b64decode(credential, ))
                outfile.close()
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/gsa.json"

    def getMessage(self):
        try:
            # LOG.info("receive message from %s as user %s" % (SQS_QUEUE_URL, aws_access_key_id) )
            response = self.__sqs__.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                AttributeNames=[ 'All' ],
                MessageAttributeNames=[ "filename" ],
                MaxNumberOfMessages=1,
                # VisibilityTimeout=1800,
                # WaitTimeSeconds=2,
                # ReceiveRequestAttemptId="1"
            )
            message = response['Messages'][0]
            body = message["Body"]
            LOG.info({"message":"message received %s" % body})
            receipt_handle = message['ReceiptHandle']
            success = self.process_message(body)
            if success:
                # Delete received message from queue
                # LOG.info("start delete message")
                self.__sqs__.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=receipt_handle
                )
                # LOG.info({"message":'Received and deleted message'} )

        except Exception as ex:
            LOG.info({"message": "no message recevied %s"} % str(ex))

    def downloadFile(self, bucket, key, meetingId):
        success = False
        try:
            #bug: if the uploaded is a wav file, then original file name is the same as wavefile.
            fileType = key.split(".")[-1]
            if "?" in fileType:
                fileType = fileType.split("?")[0]

            originFile = AUDIO_FOLDER + meetingId + ".orig." + fileType
            LOG.info({"message":"download file from s3 bucket %s for VOICEA_MEETING_ID: %s \
                file: %s" %(meetingId, bucket, originFile)})
            waveFile = AUDIO_FOLDER + meetingId + ".wav"
            #only download when not exist already
            if not (os.path.isfile(originFile) and os.path.exists(originFile)):
               with open(originFile, 'wb') as data:
                    self.__s3__.download_fileobj(bucket, key, data)
        except Exception as ex:
            LOG.warning({"message":"failed to download file from s3 bucket %s: for VOICEA_MEETING_ID %s, \
                exception: %s" % (meetingId, bucket, str(ex)),\
                    "VOICEA_MEETING_ID": meetingId})

        return success

    def uploadFileToS3(self, bucket, key, file):
    
        return None 
        
def main():
    demo = s3sqsDemo()
    msg = ""
    demo.post_message(msg)
    msg2 = demo.get_message()
    print("received Message {}".format(msg2))
    #bucket
    bucket = "myfirstmybucket" 
    target_file = "myfile.flac"
    demo.downloadFileFromS3(bucket, "from", target_file)
    demo.uploadFileToS3(bucket, "to", target_file)
    
    
if __name__ == '__main__':
    main( )