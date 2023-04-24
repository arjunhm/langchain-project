import requests

from django.conf import settings
from api.models import Post


def create_linkedin_post(post):
    BASE_URL = ""
    data = {}
    try:
        response = requests.post(BASE_URL, data=data)
        if response.status_code == 201:
            post.is_posted = True
            post.save()
        return response.json()
    except Exception as e:
        return {}
