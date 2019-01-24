import json
import boto3
import datetime
import time


ec2 = boto3.client('ec2', region_name='us-east-1')

def lambda_handler(event, context):
    count = 0
    #### Retention days #####
    Retention_period_days=1   # Modify this value if you want to change the retention period, according to this value  the code will delete the AMIs if their creation date (Day) is greater than Retention_period_days variable.
    date_now = datetime.datetime.now()    
    image_idd= "none"
    # Filtering Image by Tag 
    image = ec2.describe_images(
        Filters=[
            {     #Modify the Name and Values according to  the Tag assigned to AMI 
        'Name': 'tag:RetencionH',
        'Values': [
            'DiasX1'     
            ]
        },
    ]
        )
    response2=json.dumps(image)
    array = []
    i =0
    count4=0
    count5=0
    for i2 in image["Images"]:
        count4 = count4 +1
        Date_Image = i2["CreationDate"]
        image_idd = i2["ImageId"]
        Date_Image= Date_Image.replace('T','-')
        Date_Image= Date_Image.replace(':','-')
        Date_Image = Date_Image.split('-')
        difference_date = (int(date_now.day) - int(Date_Image[2]) )
        difference_date = abs(difference_date)
        difference_hour = abs(int(Date_Image[3]) - int(date_now.hour) )
        
        if (difference_date >= Retention_period_days) and (difference_hour==0) :
            count5 = count5 +1
            print(" The AMI "+image_idd+"  wil be deregistered" )
            ec2.deregister_image(
               ImageId = image_idd
              )
           
            try:
              for snaps in i2["BlockDeviceMappings"] :
                   ec2.delete_snapshot(
                     SnapshotId= snaps["Ebs"]["SnapshotId"]
                     )
              
            except KeyError as error:
            
               print "Error captured"
            except Exception as exception:

                print "exception action executed"
                
          
    print "The number of AMIs that were deleted are ",count5
   
   
    return {
        'statusCode': 200,
        'body': json.dumps('Function successfully executed')
    }

