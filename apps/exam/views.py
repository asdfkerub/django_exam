from django.shortcuts import render, redirect
from .models import User, Quote, Favorite
from django.contrib import messages
# Create your views here.
def index(request):
    return redirect('/main')

def home(request):
    return render(request,'exam/index.html')

def register(request):
    user = User.objects.register(request.POST)
    if 'error' in user:
        for validation_error in user['error']:
            messages.error(request,validation_error)
        return redirect('/main')
    if 'the_user' in user:
        messages.success(request,'Successfully registered')
        return redirect('/main')

def login(request):
    if request.method == 'POST':
        user = User.objects.login(request.POST)
        if 'error' in user:
            for validation_error in user['error']:
                messages.error(request,validation_error)
            return redirect('/main')
        if 'the_user' in user:
            if 'logged_in' not in request.session:
                request.session['logged_in'] = 'null'
            request.session['logged_in'] = user["the_user"].id
            print request.session['logged_in']
            return redirect('/quotes')

def logout(request):
    request.session['logged_in'] = 'null'
    messages.success(request,'Successfully Logged Out')
    return redirect('/main')

def quotes(request):
    user = User.objects.get(id=request.session['logged_in'])
    context = {
        'user' : User.objects.get(id=request.session['logged_in']),
        'quotes' : Quote.objects.exclude(favorite_quote__user=user).order_by('-created_at'),
        # 'quotes' : Quote.objects.all(),
        'favorites' : Favorite.objects.filter(user=user).order_by('-created_at')
    }
    return render(request,'exam/quotes.html', context)

def add_quote(request):
    quote = Quote.objects.qval(request.POST)
    if 'error' in quote:
        for validation_error in quote['error']:
            messages.error(request,validation_error)
        return redirect('/quotes')
    if 'the_quote' in quote:
        user = User.objects.get(id=request.session['logged_in'])
        quote = Quote.objects.create(name=request.POST['quote_by'],content=request.POST['message'],user=user)
        messages.success(request,'Successfully Added a quote')
        return redirect('/quotes')

def add_favorite(request, quote_id):
    user = User.objects.get(id=request.session['logged_in'])
    quote = Quote.objects.get(id=quote_id)
    Favorite.objects.create(quote=quote,user=user)
    messages.success(request,'Successfully added a quote to your favorites')
    return redirect('/quotes')

def remove_favorite(request,quote_id):
    user = User.objects.get(id=request.session['logged_in'])
    quote = Quote.objects.get(id=quote_id)
    Favorite.objects.filter(user=user).filter(quote=quote).delete()
    messages.success(request,'Successfully removed a quote from your favorites')
    return redirect('/quotes')

def show_user(request,user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user' : User.objects.get(id=user_id),
        'count' : Favorite.objects.filter(user=user).count(),
        'quotes' : Favorite.objects.filter(user=user),
    }
    return render(request,'exam/user.html', context)
