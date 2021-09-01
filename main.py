import boto3
from botocore.config import Config
import pprint
'''
my_config = Config(
    region_name = 'ap-southeast-2',
)
'''
session = boto3.Session(profile_name='default')
ec2_client = session.client('ec2')
#get All SGs with Group (SG) rule where the source is 0.0.0.0/0 and the port is 22 (ssh)
def lambda_handler():
    response = ec2_client.describe_security_groups(Filters=[
        {
            'Name': 'ip-permission.from-port',
            'Values': [
                '22',
            ]
        },
        {
            'Name': 'ip-permission.cidr',
            'Values': [
                '0.0.0.0/0',
            ]
        },
    ])
    
    
    
    for sg in response['SecurityGroups']:
        print(sg['GroupName'])
        # Remove SG Rule
        ec2 = boto3.resource('ec2')
        security_group = ec2.SecurityGroup(sg['GroupId'])
        print ('removing insecure SG rule from ->' + (sg['GroupId']))
        security_group.revoke_ingress(IpProtocol="tcp", CidrIp="0.0.0.0/0", FromPort=22, ToPort=22)
        
lambda_handler();
