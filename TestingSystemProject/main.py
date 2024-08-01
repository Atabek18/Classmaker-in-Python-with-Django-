# # from enum import Enum

# # from fastapi import FastAPI, Query


# # class ModelName(str, Enum):
# #     alexnet = "alexnet"
# #     resnet = "resnet"
# #     lenet = "lenet"


# # app = FastAPI()


# # @app.get("/models/{model_name}")
# # async def get_model(model_name: ModelName):
# #     if model_name is ModelName.alexnet:
# #         return {"model_name": model_name, "message": "Deep Learning FTW!"}

# #     if model_name.value == "lenet":
# #         return {"model_name": model_name, "message": "LeCNN all the images"}

# #     return {"model_name": model_name, "message": "Have some residuals"}


# # @app.get("/files/{file_path:path}")
# # async def read_file(file_path: str):
# #     return {"file_path": file_path}


# # from pydantic import BaseModel


# # class Item(BaseModel):
# #     name: str
# #     description: str | None = None
# #     price: float
# #     tax: float | None = None

# # @app.post("/items/")
# # async def create_item(item: Item):
# #     return item


# # from typing import Annotated


# # @app.get("/items/")
# # async def read_items(q: Annotated[list[str] | None, Query()] = None):
# #     query_items = {"q": q}
# #     return query_items



# # from datetime import datetime


# # class Subscription(BaseModel):
# #     username: str
# #     monthly_fee: float
# #     start_date: datetime


# # @app.webhooks.post("new-subscription")
# # def new_subscription(body: Subscription):
# #     """
# #     When a new user subscribes to your service we'll send you a POST request with this
# #     data to the URL that you register for the event `new-subscription` in the dashboard.
# #     """


# # @app.get("/users/")
# # def read_users():
# #     return ["Rick", "Morty"]

# import requests

# url = 'http://127.0.0.1:9180/apisix/admin/routes/1'
# headers = {
#     'X-API-KEY': 'edd1c9f034335f136f87ad84b625c8f1',
#     'Content-Type': 'application/json'
# }

# data = {
#     "uri": "/my-credit-cards",
#     "plugins": {
#         "pipeline-request": {
#             "nodes": [
#                 {
#                     "url": "https://random-data-api.com/api/v2/credit_cards"
#                 },
#                 {
#                     "url": "http://127.0.0.1:9080/filter"
#                 }
#             ]
#         }
#     }
# }

# response = requests.put(url, headers=headers, json=data)

# print(response.status_code)
# print(response.json())

# from datetime import datetime
# import pytz

# timestamp = 1706118247

# dt_utc = datetime.utcfromtimestamp(timestamp)
# utc_timezone = pytz.timezone('UTC')
# dt_utc = utc_timezone.localize(dt_utc)
# tashkent_timezone = pytz.timezone('Asia/Tashkent')
# dt_tashkent = dt_utc.astimezone(tashkent_timezone)

# print("Timeout timestamp in Tashkent:", dt_tashkent)

# import jwt
# from datetime import datetime, timedelta

# # Your secret key
# SECRET_KEY = 'your_secret_key'

# # User data or any additional payload
# user_data = {
#     'user_id': 123,
#     'email': 'user@example.com',
# }

# # Set the expiration time for the refresh token
# refresh_token_lifetime = timedelta(days=1)  # Set your desired lifetime
# refresh_token_expiration_time = datetime.utcnow() + refresh_token_lifetime

# # Set the expiration time for the access token
# access_token_lifetime = timedelta(minutes=15)  # Set your desired lifetime
# access_token_expiration_time = datetime.utcnow() + access_token_lifetime

# # Build the refresh token payload
# refresh_token_payload = {
#     'exp': refresh_token_expiration_time,
#     **user_data,
# }

# # Build the access token payload
# access_token_payload = {
#     'exp': access_token_expiration_time,
#     **user_data,
# }

# # Create the refresh token
# refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm='HS256')

# # Create the access token
# access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm='HS256')

# # Optionally, rotate refresh tokens
# rotate_refresh_tokens = True
# if rotate_refresh_tokens and refresh_token_expiration_time < datetime.utcnow():
#     new_refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm='HS256')
#     print('New refresh token:', new_refresh_token)

# # Print the access token
# print('Access token:', access_token)

# import youtube_dl

# def download_video(url, output_path):
#     ydl_opts = {
#         'outtmpl': output_path + '.%(ext)s',
#         'format': 'best',  # Specify the preferred format
#         'socket_timeout': 10,  # Set socket timeout to 10 seconds
#         'retries': 5,  # Increase the number of retries
#         'retry_max_sleep': 5,  # Reduce maximum sleep time between retries to 5 seconds
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

# url = "https://www.instagram.com/reel/C38ArShNuZk/?igsh=N3lmczJkMWU2dmNn"
# output_path = "downloaded_video1"
# download_video(url, output_path)



# import json

# class SkillManager:
#     def __init__(self):
#         self.skills = {}

#     def load_skill(self, filename):
#         with open(filename, 'r') as f:
#             skill_data = json.load(f)
#             skill_name = skill_data["name"]
#             self.skills[skill_name] = skill_data

#     def use_skill(self, skill_name, *args, **kwargs):
#         if skill_name in self.skills:
#             skill_data = self.skills[skill_name]
#             # Implement logic to execute the skill based on the loaded JSON data
#             # This will depend on the specific structure of your JSON files
#             # For example:
#             if skill_name == "playfootball":
#                 # Access data like skill_data["type"], skill_data["rules"], etc.
#                 print(f"Executing playfootball skill with parameters: {args}, {kwargs}")
#             elif skill_name == "basketball":
#                 # Access data like skill_data["dribbling"], skill_data["shooting"], etc.
#                 print(f"Executing basketball skill with parameters: {args}, {kwargs}")
#         else:
#             print(f"Skill '{skill_name}' not found.")

# # Example usage
# skill_manager = SkillManager()
# skill_manager.load_skill("playfootball.json")

# skill_manager.use_skill("playfootball", "outdoor", team_size=11)
# skill_manager.use_skill("basketball", "indoor", team_size=5)


# import json
# import os
# import shutil

# class SkillManager:
#     def __init__(self, skills_folder="Skills"):
#         self.skills_folder = skills_folder
#         self.skills = {}
#         os.makedirs(skills_folder, exist_ok=True)

#     def load_skill(self, filepath):
#         with open(filepath, 'r') as f:
#             skill_data = json.load(f)
#             skill_name = skill_data["name"]
#             self.skills[skill_name] = skill_data

#     def save_skill(self, skill_name, approve=False):
#         if skill_name in self.skills:
#             skill_data = self.skills[skill_name]
#             if approve:
#                 skill_data["skill_approved"] = "True"
#                 filename = f"{skill_name}.json"
#                 filepath = os.path.join(self.skills_folder, filename)
#                 with open(filepath, 'w') as f:
#                     json.dump(skill_data, f, indent=4)
#                 print(f"Skill '{skill_name}' saved to {filepath}")
#             else:
#                 print(f"Skill '{skill_name}' not approved, not saving.")
#         else:
#             print(f"Skill '{skill_name}' not found.")

# # Example usage
# skill_manager = SkillManager()
# skill_manager.load_skill("playfootball.json")  # Load from original location
# skill_manager.save_skill("football", approve=True)  # Save with approval to Skills folder

# import datetime

# class DynamicTimeManager:
#     def __init__(self):
#         self.start_point = None
#         self.end_point = None
#         self.limited_time = None
#         self.start_point = self._get_current_time()

#     def start(self, limited_time=None):
#         self.limited_time = limited_time
#         if self.limited_time is not None:
#             self.end_point = self.start_point + self.limited_time
#         # Send start and end points to frontend for time animation

#     def reload_page(self):
#         reloaded_time = self._get_current_time()
#         self.start_point = reloaded_time
#         if self.limited_time is not None:
#             self.end_point = self.start_point + self.limited_time
#         # Send updated end point to frontend

#     def _get_current_time(self):
#         # Use UZB time zone
#         current_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5)))
#         return current_time

# # Example usage
# dynamic_time_manager = DynamicTimeManager()
# dynamic_time_manager.start(limited_time=datetime.timedelta(minutes=30))
# print(dynamic_time_manager.start_point, dynamic_time_manager.end_point)
# # Simulate reload after 15 minutes
# # dynamic_time_manager.reload_page()

import os
import pkg_resources
import importlib.util
import subprocess

def get_installed_packages():
    """Get a list of all installed packages."""
    result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[2:]  # Skip header lines
    packages = [line.split()[0] for line in lines]
    return packages

def get_package_path(package_name):
    """Get the installation path of a package."""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec and spec.origin:
            return os.path.dirname(spec.origin)
        else:
            return None
    except ModuleNotFoundError:
        return None

def get_size(path):
    """Calculate the size of a directory."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_packages_sizes():
    """Get sizes of all installed packages."""
    packages = get_installed_packages()
    package_sizes = []
    for package in packages:
        path = get_package_path(package)
        if path:
            size = get_size(path)
            size_in_mb = size / (1024 ** 2)
            package_sizes.append((package, size_in_mb))
    return package_sizes

# Main function to display package sizes
# if __name__ == "__main__":
#     package_sizes = get_packages_sizes()
#     for package, size in sorted(package_sizes, key=lambda x: x[1], reverse=True):
#         print(f"{package}: {size:.2f} MB")


input = [-6, -5, 1, 2, 3, 4]
output = [1, 4, 9, 16, 25, 36]
length = len(input)
res = []
def sort_and_power(input: list[int]) -> list[int]:
    for index, (left_num, right_num) in enumerate(zip(input, input[1:])):
        if left_num < 0 and right_num >= 0:
            left = index
            right = index + 1

    while left >= 0 and right < length:
        if abs(input[left]) < input[right]:
            res.append(input[left] ** 2)
            left -= 1
        else:
            res.append(input[right] ** 2)
            right += 1

    while left >= 0:
        res.append(input[left]**2)
        left -= 1

    while right < length:
        res.append(input[right] ** 2)
        right += 1



input = [6, 2, 3, 7, 0, 1]
def  solution(input: list[int], k: int) -> list[int]:
    main_length = len(input) - k + 1
    res = {k:[]}
    for i in range(main_length):
        res[k].append(max(input[:i+k]))
    return res[k]


class Stack:
    def __init__(self) -> None:
        self.items = []

    def is_empty(self):
        if self.items == []:
            return True
    def push(self, item):
        self.items.append(item)

import queue
from queue import Empty
from collections import deque
import threading
q = queue.Queue()


# Enqueue elements
q.put('a', block=False)
q.put('b', block=False)
q.put('c', block=False)

print("Queue size:", q.qsize())

# Dequeue elements
print("Dequeued element:",  q.get())
print("Queue size after dequeue:", q.qsize())


class CustomQueue:

    def __init__(self) -> None:
        self.queue = deque()
        self.mutex = threading.Lock()

    def __repr__(self) -> str:
        return str(self.queue)

    def is_empty(self) -> bool:
        with self.mutex:
            return not self.qsize()

    def enqueue(self, item: any) -> None:
        if item is not None:
            self.queue.append(item)
        else:
            raise ValueError("Item cannot be None")

    def dequeue(self) -> any:
        if not self.is_empty():
            return self.queue.popleft()
        else:
            raise Empty

    def qsize(self) -> int:
        return len(self.queue)

q_custom = CustomQueue()

q_custom.enqueue(1)
q_custom.enqueue(2)
q_custom.enqueue(3)
print(q_custom.dequeue())
print(q_custom.dequeue())
print(q_custom.is_empty())


# main branch changed
