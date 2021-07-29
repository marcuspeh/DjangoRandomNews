from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User, History
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from newsapi import NewsApiClient

from random import choice, randint
from django.http.response import HttpResponse

from .apiKey import key

API = NewsApiClient(api_key=key)
SOURCES = ['abc-news', 'abc-news-au', 'al-jazeera-english', 'ars-technica', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 'business-insider-uk', 'buzzfeed', 'cbc-news', 'cbs-news', 'cnn', 'crypto-coins-news', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 'football-italia', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'google-news', 'google-news-au', 'google-news-ca', 'google-news-in', 'google-news-uk', 'hacker-news', 'ign', 'independent', 'mashable', 'medical-news-today', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 'national-review', 'nbc-news', 'news24', 'new-scientist', 'news-com-au', 'newsweek', 'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'politico', 'polygon', 'recode', 'reddit-r-all', 'reuters', 'rte', 'talksport', 'techcrunch', 'techradar', 'the-american-conservative', 'the-globe-and-mail', 'the-hill', 'the-hindu', 'the-huffington-post', 'the-irish-times', 'the-jerusalem-post', 'the-lad-bible', 'the-next-web', 'the-sport-bible', 'the-times-of-india', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'the-washington-times', 'time', 'usa-today', 'vice-news', 'wired']

# Create your views here.
def indexView(request):
    # if user is authenticated, search for news viewed in the past
    if (request.user.is_authenticated):
        history = History.objects.filter(user=request.user).order_by('-time')
    else:
        history = None
    return render(request, "website/index.html", {"history": history})

@login_required
def getNews(request):
    # if generate news button in home page is clicked
    if request.POST:
        # check if category is selected
        category = request.POST['category']
        if (category == "random"):
            # Sources to generate the news is random
            news = API.get_top_headlines(sources=choice(SOURCES), language='en')
        else:
            news = API.get_top_headlines(category=category, language='en')
    else:
        # if getnews url is typed in directly
        news = API.get_top_headlines(sources=choice(SOURCES), language='en')
    
    # in case the newsAPI did not return any news
    if (len(news['articles']) == 0):
        return render(request, "website/news.html")

    # Select a random news from the 20 returned by the API
    index = randint(0, len(news['articles']) - 1)

    # Saved the news selected so that the user can view history
    obj = History()
    obj.user = request.user
    obj.title = news['articles'][index]['title'] or ""
    obj.description = news['articles'][index]['description'] or ""
    obj.date = news['articles'][index]['publishedAt'].split('T')[0] or ""
    obj.author = news['articles'][index]['author'] or ""
    obj.image = news['articles'][index]['urlToImage'] or ""
    obj.url = news['articles'][index]['url'] or ""
    obj.save()

    return render(request, "website/news.html", {
        'title': obj.title,
        'description': obj.description,
        'date': obj.date,
        'author': obj.author,
        'image': obj.image,
        'url': obj.url
    })


def loginView(request):
    # User should not be able to login view if he is logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if submit button for login form is clicked
    if request.method == "POST":
        # getting all the input from the field
        username = request.POST["inputUsername"]
        password = request.POST["inputPassword"]
        
        # Raising an errorMessage if any of the field is empty
        if not username or not password:
            return render(request, "website/login.html", {
                "errorMessage": "Both username and password is required."
            })

        # attempt to log in the the user
        user = authenticate(request, username=username, password=password)

        # checks if it successful or not
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "website/login.html", {
                "errorMessage": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")
        
def registerView(request):
    
    # User should not be able to register view if he is logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    # if submit button for registering new button is clicked
    if request.method == "POST":
        # getting all the input from the field
        username = request.POST["inputUsername"]
        email = request.POST["inputEmail"]
        password = request.POST["inputPassword"]
        password2 = request.POST["inputPassword2"]

        # Raising an errorMessage if any of the field is empty
        if not username or not email or not password or not password2:
            return render(request, "website/register.html", {
                "errorMessage": "All the fields are required."
            })
        
        # Raising an errorMessage if password field dont match
        if password != password2:
            return render(request, "website/register.html", {
                "errorMessage": "Passwords must match."
            })

        # Create the user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except:
            return render(request, "website/register.html", {
                "errorMessage": "Username already taken."
            })

        # log in the user
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "website/register.html")

def logoutView(request):
    # logouts the user
    try:
        logout(request)
    except:
        pass
    return HttpResponseRedirect(reverse("index"))