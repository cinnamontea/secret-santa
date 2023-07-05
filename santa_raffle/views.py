from django.shortcuts import render

# Create your views here.

def home_feed(request):
    return render(request, 'santa_raffle/home_feed.html', {})