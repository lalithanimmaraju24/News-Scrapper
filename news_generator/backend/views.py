from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.models import User, SavedNews
import json
from backend.new_scraper import scrape_news
from backend.utilites import sort_by_user_interest, add_user_data
import pandas as pd
import os


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def return_data(status, message, data=None):
    if data is None:
        return {"status": status, "message": message}
    else:
        return {"status": status, "message": message, "data": data}


@csrf_exempt
def register(request):
    # print(request.data)
    if request.method == "POST":
        print(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user_obj = User(email=email, password=password)
        user_obj.save()
        return JsonResponse(return_data(status=200, message="User has been created"))
    return JsonResponse(return_data(status=400, message="User has not been created"))


def login(request):
    if request.method == "GET":
        email = request.GET.get("email")
        password = request.GET.get("password")
        try:
            user_obj = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return JsonResponse(return_data(status=400, message="Login failed"))
        return JsonResponse(return_data(status=200, message="Login successful", data=user_obj.id))


def get_news(request):
    if request.method == "GET":
        new_news = request.GET.get("new_news")
        user_id = request.GET.get("user_id")
        if new_news == 1 or new_news == "1":
            scrape_news()

        with open("./static/news.json", "r", encoding="utf8") as f:
            news_data = json.load(f)
        news_data = sort_by_user_interest(news_data, user_id)
        for i in range(len(news_data)):
            news_data[i]['like'] = False
            news_data[i]['save'] = False
        news_data = {
            "data": news_data
        }
        print(type(news_data))
        return JsonResponse(news_data)


def get_saved_news(request):
    if request.method == "GET":
        user_id = request.GET.get("user_id")
        user_saved_news = SavedNews.objects.filter(user_id=user_id)
        li = []
        for news in user_saved_news:
            item = {
                'url': news.url,
                "title": news.news_title,
                "description": news.news_description,
                "source": news.news_source
            }
            li.append(item)
        user_saved_news = {
            "data": li
        }
        return JsonResponse(user_saved_news)


@csrf_exempt
def save_news(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        news_id = int(request.POST['news_id'])
        with open("./static/news.json", "r", encoding="utf8") as f:
            news_data = json.load(f)

        for news in news_data:
            if news['id'] == int(news_id):
                url = news['url']
                title = news['title']
                description = news['description']
                source = news['source']['name']
                break
        user_obj = User.objects.get(id=int(user_id))
        saved_obj = SavedNews(user_id=user_obj, url=url, news_title=title, news_description=description,
                              news_source=source)
        saved_obj.save()
        add_user_data(user_id, title, description)
        return JsonResponse(return_data(status=200, message="News has been saved"))
    else:
        return JsonResponse(return_data(status=400, message="Wrong details"))


@csrf_exempt
def like_open(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        news_id = int(request.POST['news_id'])
        with open("./static/news.json", "r", encoding="utf8") as f:
            news_data = json.load(f)
        title = ""
        description = ""
        for news in news_data:
            if news['id'] == int(news_id):
                title = news['title']
                description = news['description']
                break
        add_user_data(user_id, title, description)
        return JsonResponse(return_data(status=200, message="News has been saved"))
    else:
        return JsonResponse(return_data(status=400, message="Wrong details"))
