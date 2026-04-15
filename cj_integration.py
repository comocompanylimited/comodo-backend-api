from fastapi import APIRouter
import requests

router = APIRouter()

CJ_API_KEY = "PASTE_MY_API_KEY_HERE"


@router.get("/cj/test-token")
def get_cj_token():
    url = "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken"

    payload = {
        "apiKey": CJ_API_KEY
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
