from django.shortcuts import render
from faker import Faker
from .firebase import Firebase, TITLE_COLLECTION, OUTLINE_COLLECTION
from django.http import HttpResponse, JsonResponse
import string
import random
# Create your views here.


def save_in_firebase(data, action='title', fetch_record=True):
    FB = Firebase()
    if action == 'title':
        FB.set_collection(TITLE_COLLECTION)
    elif action == 'outline':
        FB.set_collection(OUTLINE_COLLECTION)
    else:
        FB.set_collection(TITLE_COLLECTION)
    return FB.save_data(fetch_record=fetch_record, **data)


def save_batch_in_firebase(data, action='title'):
    FB = Firebase()
    if action == 'title':
        FB.set_collection(TITLE_COLLECTION)
    elif action == 'outline':
        FB.set_collection(OUTLINE_COLLECTION)
    else:
        FB.set_collection(TITLE_COLLECTION)
    return FB.batch_save_data(data)


def fetch_data_firebase(condition=None, action='title'):
    FB = Firebase()
    if action == 'title':
        FB.set_collection(TITLE_COLLECTION)
    elif action == 'outline':
        FB.set_collection(OUTLINE_COLLECTION)
    else:
        FB.set_collection(TITLE_COLLECTION)

    return FB.fetch_data(condition=condition)


def fetch_outlines(text=None):
    condition = None
    if text:
        condition = {
            "field": 'text',
            "oprator": "==",
            "value": text
        }
    return fetch_data_firebase(condition, action='outline')


def fetch_titles(text=None):
    condition = None
    if text:
        condition = {
            "field": 'text',
            "oprator": "==",
            "value": text
        }
    return fetch_data_firebase(condition, action='title')


def index(request):
    DATA = {}
    DATA["titles"] = fetch_titles(None)
    DATA["outlines"] = fetch_titles(None)

    return JsonResponse(DATA)


def add_title_and_outline(request):
    fake = Faker()

    title = {
        "name": fake.name(),
        "text": fake.text()
    }

    outline = {
        "name": fake.name(),
        "text": fake.text()
    }

    print(save_in_firebase(title))
    print(save_in_firebase(outline, action='outline'))

    return HttpResponse("Saved record!!")


def add_multiple_title_and_outline(request):
    fake = Faker()

    titles = [
        {
            "name": fake.name(),
            "text": fake.text()
        },
        {
            "name": fake.name(),
            "text": fake.text()
        },
        {
            "name": fake.name(),
            "text": fake.text()
        },
    ]

    outlines = [
        {
            "name": fake.name(),
            "text": fake.text()
        },
        {
            "name": fake.name(),
            "text": fake.text()
        },
        {
            "name": fake.name(),
            "text": fake.text()
        }
    ]

    save_batch_in_firebase(titles)
    save_batch_in_firebase(outlines, action='outline')

    return HttpResponse("Saved batch record!!")
