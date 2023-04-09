from django.http import HttpResponse, Http404
from .models import Article
from django.shortcuts import render, redirect
import logging



def home(request):
    return HttpResponse('Привет, Мир!')
def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})
def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"],
                'title': request.POST["title"],
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                logic = bool(Article.objects.all().filter(title=form["title"]))
                if not logic:
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    arr = Article.objects.all()
                    return redirect('get_article', article_id=arr[len(arr) - 1].id)
                else:
                    form['errors'] = u"Такакя статья уже существует"
                    return render(request, 'create_post.html', {'form': form})
            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404