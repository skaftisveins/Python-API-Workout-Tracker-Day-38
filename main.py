from config import *
import requests
from datetime import datetime as dt

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": nutrutionix_app_id,
    "x-app-key": nutritionix_api_key,
}

sheety_headers = {
    "Authorization": f"Bearer {sheety_bearer_token}"
}

nutritionix_params = {
    "query": exercise_text,
    "gender": gender,
    "weight_kg": weight_kg,
    "height_cm": height_cm,
    "age": age
}


response = requests.post(url=nutritionix_endpoint,
                         json=nutritionix_params, headers=headers)
result = response.json()
print(result)

TODAY = dt.now().strftime("%d/%m/%Y")
TIME = dt.now().strftime("%X")


def get_workout_track():
    response = requests.get(sheety_endpoint, headers=sheety_headers)
    print(response.json())


def add_to_workout_track():
    for exercise in result["exercises"]:
        sheet_inputs = {
            "workout": {
                "date": TODAY,
                "time": TIME,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"],
            }
        }

        sheet_response = requests.post(
            url=sheety_endpoint, json=sheet_inputs, headers=sheety_headers)

        print(sheet_response.text)


add_to_workout_track()
get_workout_track()
