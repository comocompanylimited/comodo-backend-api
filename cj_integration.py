from fastapi import APIRouter
import requests

cj_router = APIRouter(tags=["CJ Dropshipping"])

CJ_API_KEY = "PASTE_MY_CJ_API_KEY_HERE"


@cj_router.get("/cj/test-token")
def get_cj_token():
    url = "https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken"
    response = requests.post(
        url,
        json={"apiKey": CJ_API_KEY},
        headers={"Content-Type": "application/json"},
    )
    return response.json()
