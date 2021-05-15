from config import *
import requests
from datetime import datetime as dt

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
}

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"
}

nutritionix_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}


response = requests.post(url=NUTRITIONIX_ENDPOINT,
                         json=nutritionix_params, headers=headers)
result = response.json()
print(result)

TODAY = dt.now().strftime("%d/%m/%Y")
TIME = dt.now().strftime("%X")


def get_workout_track():
    response = requests.get(SHEETY_ENDPOINT, headers=sheety_headers)
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
        url=SHEETY_ENDPOINT, json=sheet_inputs, headers=sheety_headers)

    print(sheet_response.text)


get_workout_track()
add_to_workout_track()
