import cv2
import boto3
import os
from SendEmail import *
import serial 

ser=serial.Serial('COM3',9600,timeout=0.5)
ser.close()
ser.open()

accessKey='' # ask admin to share access key
secretAccessKey='' # ask admin to share secret access
region='us-east-1'
family=os.listdir('family/')
dFlag=0

client=boto3.client('rekognition',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)

def takeSnapshot():
    print('Taking Photo')
    cam=cv2.VideoCapture(0)
    while True:
        res,frame=cam.read()
        if res:
            cv2.imshow('result',frame)
            cv2.imwrite('test.jpg',frame)
            # cv2.waitKey(1)
            break

    cv2.destroyAllWindows()
    cam.release()
    print('Snapshot Taken')

while True:
    if ser.inWaiting()>0:
        data=ser.readline().decode('utf-8')
        if data.startswith('#door'):
            takeSnapshot()
            for i in family:
                imageSource=open('test.jpg','rb')
                imageTarget=open('family/'+i,'rb')
                response=client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imageSource.read()},TargetImage={'Bytes':imageTarget.read()})

                try:
                    if response['FaceMatches']:
                        dFlag=1
                        result=i.split('.')[0]
                        print('Face Identified as ' + result)
                        send_email('otp.service@makeskilled.com','ravalimandalapu802@gmail.com','Face Identified as '+ result, 'Hi Hello, Your Bot Bot Here','test.jpg')
                except:
                    dFlag=0

            if(dFlag==0):
                print('Stranger Found')
                send_email('otp.service@makeskilled.com','ravalimandalapu802@gmail.com','Face Identified as Stranger', 'Hi Hello, Your Door Bot Here','test.jpg')