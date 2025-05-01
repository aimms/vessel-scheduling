# This is a sample Python script.
# The purpoose of this script is to demo and test the service 'solveVesselScheduling'
# implemented in AIMMS and published on an AIMMS Cloud

import requests
#import pandas as pd
import time
#import json
import datetime


import os
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script's directory
os.chdir(script_dir)
# Now you can run your code with the current directory set to the script's location
now = datetime.datetime.now()
cwd = os.getcwd()
print(f"start: {now} cwd: {cwd}")

# The config folder is a folder next to the app containing config info for the tests at hand.
config_folder = '../config/'

# Going to use the localhost or an AIMMS Cloud.
with open(config_folder + 'using_AIMMS_cloud.txt', 'r') as using_AIMMS_cloud_file:
    using_AIMMS_cloud = int(using_AIMMS_cloud_file.readline())

# Read in ingredients of the URLs to be used.
with open(config_folder + 'app.txt', 'r') as app_file:
    app = app_file.readline()
# app = 'VesselScheduling' # most environments.
# app = 'SchedulingVessels' # environment user-support.aimms-dev
# service = 'solveVesselSchedulingExcel'
# using_AIMMS_cloud = 1
# port=12003

with open(config_folder + 'ver.txt', 'r') as ver_file:
    ver = ver_file.readline()

with open(config_folder + 'service.txt', 'r') as service_file:
    service = service_file.readline()

if using_AIMMS_cloud:
    with open(config_folder + 'cloud.txt', 'r') as cloud_file:
        cloud = cloud_file.readline()

    with open(config_folder + 'apikey.txt', 'r') as apikey_file:
        headers_apikey = apikey_file.readline()
    Headers = {"apiKey": headers_apikey}
    port = 0
else:
    cloud = ""
    Headers = {}
    with open(config_folder + 'port.txt', 'r') as port_file:
        port = int(port_file.readline())


# The URL prefix is the fixed part of the URL's used.
# On Cloud, we need to include the name of the cloud,
# On localhost, we need the port number (8080 unless specified otherwise).
url_prefix = ''
if using_AIMMS_cloud:
    url_prefix = f"https://{cloud}/pro-api/v2/tasks/"
else:
    url_prefix = f"http://localhost:{port}/api/v2/tasks/"

# To submit a task a POST is required to the URL for submitting a task.
# On Cloud, we also need to specify the app, version, and service name.
# On localhost, only the service name is needed.
url_submit = ''
if using_AIMMS_cloud:
    url_submit = url_prefix + app + '/' + service
else:
    url_submit = url_prefix + service
print(f"URL submit task: {url_submit}")


if service == 'solveVesselSchedulingExcel':

    # Source
    # Specify input file.
    
    #vessel_input_filename = '..\AIMMS Project\data\VS_5Vessel_15Cargo.xlsx'
    #vessel_input_filename = '..\AIMMS Project\data\VS_7Vessel_20Cargo.xlsx'

    #vessel_input_filename = 'VS_15Vessel_30Cargo.xlsx'
    #vessel_input_filename = 'VS_40Vessel_50Cargo.xlsx'
    #vessel_input_filename = 'VS_70Vessel_100Cargo.xlsx'
    vessel_input_filename = 'VS_120Vessel_150Cargo.xlsx'
    #vessel_input_filename = 'VS_150Vessel_200Cargo 10 day wait.xlsx'
    
    # Open the file in binary mode.
    with open(vessel_input_filename, 'rb') as file:
        vessel_schedule_files = {'file': (vessel_input_filename, file, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

        # Kick off the task -   Send the POST request with the Excel data as JSON payload
        submit_response = requests.post(url_submit, files=vessel_schedule_files, headers=Headers)

elif service == 'solveVesselSchedulingCSV':

    vessel_input_filename = 'VS_5Vessel_15Cargo-csv.zip'

    with open(vessel_input_filename, 'rb') as file:
        # Send the POST request with the zip file as the body
        submit_response = requests.post(url_submit, data=file, headers=Headers)

    #raise Exception("not yet implemented")
    
elif service == 'solveVesselSchedulingParquet':

    # delete results .zip file if it exists.
    if os.path.exists("VS_5Vessel_15Cargo_Results-parquet.zip"):
        os.remove("VS_5Vessel_15Cargo_Results-parquet.zip")

    vessel_input_filename = 'VS_7Vessel_20Cargo-parquet.zip'

    with open(vessel_input_filename, 'rb') as file:
        # Send the POST request with the zip file as the body
        submit_response = requests.post(url_submit, data=file, headers=Headers)

elif service == 'solveVesselSchedulingSharedFiles':

    vessel_input_filename = 'VS_7Vessel_20Cargo-sharedFiles.json'

    with open(vessel_input_filename, 'rb') as file:
        # Send the POST request with the zip file as the body
        submit_response = requests.post(url_submit, data=file, headers=Headers)

else:

    raise Exception(f"{service} not supported")

print(f"Submit response code: {submit_response.status_code}")

# Get the response id
task_id = submit_response.json()['id']
print("Task id: " + task_id)


# Wait until the task is finished, polling every five seconds
url_poll = url_prefix + task_id
print("URL for status updates: " + url_poll)

state = ""
print("Task state:")
while state != 'completed' and state != 'failed':
    time.sleep(5)
    poll_response = requests.get(url_poll, headers=Headers)
    state = poll_response.json()['state']
    print("    " + state)

# Finished. Obtain the final result.
url_task_response = url_prefix + task_id + '/response'
print(f"URL Task Response: {url_task_response}")

task_response = requests.get(url_task_response, headers=Headers)
print(f"task response code: {task_response.status_code}")
# print(f"task response json: {task_response.json()}")

if task_response.status_code==200:
    vessel_result_filename = vessel_input_filename.replace('Cargo','Cargo_Results')
else:
    vessel_result_filename = vessel_input_filename.replace('xlsx','errorinfo.txt')

if service == 'solveVesselSchedulingExcel':

    open(vessel_result_filename, 'wb').write(task_response.content)

elif service == 'solveVesselSchedulingCSV':

    open(vessel_result_filename, 'wb').write(task_response.content)

elif service == 'solveVesselSchedulingParquet':

    open(vessel_result_filename, 'wb').write(task_response.content)

elif service == 'solveVesselSchedulingSharedFiles':

    open(vessel_result_filename, 'wb').write(task_response.content)
    # print("Please check the output files.")

else:
    raise Exception(f"{service} not supported")

# now = datetime.datetime.now()
# print(f"finished at: {now}")

# service = 'stopsoon'
# if using_AIMMS_cloud:
#     url_submit = url_prefix + app + '/' + service
# else:
#     url_submit = url_prefix + service
# print(f"URL submit task: {url_submit}")
#submit_response = requests.post(url_submit,  headers=Headers)

now = datetime.datetime.now()
print(f"finished at: {now}")

# Attic:
# Tips and old code:
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.