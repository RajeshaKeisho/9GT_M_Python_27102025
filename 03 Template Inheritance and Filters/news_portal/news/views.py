from django.shortcuts import render
from datetime import datetime
# Create your views here.
news_data = {
    "Technology": [
        {"title": "AI Revolution in 2025", "date": "2025-03-15", "content": "AI is taking over the world..."},
        {"title": "Quantum Computing Breakthrough", "date": "2025-03-10", "content": "A new milestone in quantum computing..."},
    ],
    "Sports": [
        {"title": "Champions League Final", "date": "2025-03-12", "content": "An epic showdown between top teams..."},
        {"title": "Olympics 2025", "date": "2025-03-18", "content": "The biggest sports event of the year..."},
    ],
    "Politics": [
        {"title": "Global Summit 2025", "date": "2025-03-08", "content": "World leaders gather for crucial discussions..."},
        {"title": "New Economic Policy", "date": "2025-03-17", "content": "A game-changing move in economic policy..."},
    ],
}

def home(request):
    context = {
        'news_data':news_data,
        'current_date':datetime.now(),
    }

    return render(request, 'news/home.html', context)

def category_news(request, category):
    category_news_list = news_data.get(category, [])
    return render(request, 'news/category.html', {'category':category, 'news_list':category_news_list})
