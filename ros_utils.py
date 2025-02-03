import os
import time
import xmltodict
import requests
from dotenv import load_dotenv
from base64 import b64encode

from config import ROS_URL

load_dotenv()


def ros_login():
    ''' Login to ROS 
    - Returns a Basic Auth Token 

    '''
    ros_username = os.environ.get('ROS_USERNAME')
    ros_password = os.environ.get('ROS_PASSWORD')
    ros_token = b64encode(f"{ros_username}:{ros_password}".encode('utf-8')).decode("ascii")

    return f"Basic {ros_token}"


def get_ros_record_by_id(ros_record_id, ros_token):
    ''' Get an individual ros record by ros id
    Inputs:
        - ros_base_url: url domain of ros instance
        - token: auth token
        - ros_record_id: id of the ros record
    Returns: 
        - JSON export of the item
    '''

    # GET RECORD
    record_get_url = f"{ROS_URL}/secure-api/v6.13/equipment/records/manual/{ros_record_id}"
    headers = {'Authorization': ros_token}

    response = requests.request("GET", record_get_url, headers=headers)
    time.sleep(1)

    return xmltodict.parse(response.content)
