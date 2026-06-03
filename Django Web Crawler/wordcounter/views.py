from django.shortcuts import render
from .forms import inputform
from .models import Mail
import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

def index(request):
    form = inputform()
    
    if request.method == "POST":
        url = request.POST.get('url')
        
        # check cache 
        cached = Mail.objects.filter(url=url).first()
        if cached:
            return render(request, 'send.html', {'words': cached.words, 'url': url})
        
        # proceceing 3 line 
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        words = ' '.join(p.get_text() for p in soup.find_all('p')).lower().split()
        word_count = Counter(w.strip(punctuation) for w in words if len(w.strip(punctuation)) > 1)
        
        #save and visualizing 
        Mail.objects.create(url=url, words=word_count.most_common())
        return render(request, 'send.html', {'words': word_count.most_common(), 'url': url})
    
    return render(request, 'home.html', {'form': form})