import requests
import subprocess
import os
import statistics
from time import time
from torchvision import models

SERVER_URL = 'http://localhost:5000/predict'
CLASSES_URL = 'https://raw.githubusercontent.com/xmartlabs/caffeflow/master/examples/imagenet/imagenet-classes.txt'
CLASSES_FILE = 'imagenet-classes.txt'
PICS_DIR = './pics'

# Prints a list as comma-seperated elements
def list_to_csv(list):
    list = [str(element) for element in list]
    list = ', '.join(list)
    return list

# Gets positive integer input with error checking
def get_positive_integer():
    while True:
        try:
            value = int(input())
            if value >= 0:
                return value
            else:
                print("Invalid input. Please enter a positive integer: ")
        except ValueError:
            print("Invalid input. Please enter a positive integer: ")

# Download imagenet-classes.txt if it doesn't exist
if not os.path.exists(CLASSES_FILE):
    print("Downloading ImageNet classes file...")
    subprocess.run(['wget', CLASSES_URL])

"""
# TODO: Need to only list models that can be called in the server
# Print the models the user can choose from
model_list = dir(models)
print(f"MODELS: {list_to_csv(model_list)}")

# Get user choice of model
user_model = input("\nChoose a model: ")
while user_model not in model_list:
    user_model = input("That's not a valid model, please try again: ")
print(f"\nSending request with model {user_model}...")
"""

# Print the pics the user can choose from
pic_list = os.listdir(PICS_DIR)
print(f"PICS: {list_to_csv(pic_list)}")

# Get user choice of pic
user_pic = input("\nChoose a pic: ")
while user_pic not in pic_list:
    user_pic = input("That's not a valid pic, please try again: ")

# Get number of requests
print("\nChoose the number of requests to send: ", end='')
num_requests = get_positive_integer()

pic_path = PICS_DIR + '/' + user_pic
execution_times = []
files = {'image': (user_pic, open(pic_path, 'rb'), 'image/jpeg')}
# data = {'model': user_model}

# Send POST request to the server
for i in range(num_requests):
    print(f"\nSending request {i+1} for pic {user_pic}...")
    try:
        start_time = time()
        response = requests.post(SERVER_URL, files=files)
        elapsed_time = time() - start_time
        execution_times.append(elapsed_time)
        if response.ok:
            result = response.json()
            print(f'Predicted class: {result["class"]}, confidence: {result["confidence"]}')
            print(f"Execution time: {round(elapsed_time, 4)}s")
        else:
            print(f"An error occurred with code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending the request!")
        print(f"Error: {str(e)}")
        exit(1)

average_time = statistics.mean(execution_times)
print(f"\nAverage execution time: {round(average_time, 4)}s")
