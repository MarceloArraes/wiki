import requests
from django.shortcuts import render
from django import forms
from markdown import Markdown, markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
import random

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="title")
    body = forms.CharField(widget=forms.Textarea(), label="body")


class randoness():
    def randoInst(self):
        listed = util.list_entries()
        random.seed()
        rand = random.randint(0, 10)
        randomizedTitle = random.choice(listed).upper()

        txt1 = "wiki/{randomized}".format(randomized=randomizedTitle)
        return txt1

    def randoInst2(self):
        listed = util.list_entries()
        random.seed()
        rand = random.randint(0, 10)
        randomizedTitle = random.choice(listed).upper()

        txt2 = "{randomized}".format(randomized=randomizedTitle)
        return txt2


def index(request):
    return render(request, "wiki/index.html", {
        "entries": util.list_entries(),
        "randomPage": randoness().randoInst(),
        "randomnumber": randoness().randoInst(),
    })


def titles(request, title):
    text = util.get_entry(title)
    if text != None:

        return render(request, "wiki/titles.html", {
            "title": title,
            "page": Markdown().convert(text),
            "randomPage": randoness().randoInst2()
        })
    else:
        return render(request, "wiki/index.html", {
            "title": title,
            "notice": "Page not Found.",
            "entries": util.list_entries(),
            "randomPage": randoness().randoInst2()
        })


def search(request):
    search = request.GET.get('q', '')

    ListOfWord = util.list_entries()
    locallis = []

    for x in ListOfWord:
        if search.upper() in x.upper():
            locallis.append(x)

    if util.get_entry(search) is None:
        return render(request, "wiki/searchresult.html", {
            "title": search,
            "notice": "Page not Found",
            "entries": util.list_entries(),
            "locallis": locallis,
            "randomPage": randoness().randoInst2(),
        })
    else:
        text = util.get_entry(search)
        return render(request, "wiki/titles.html", {
            "title": search.upper(),
            "page": Markdown().convert(text),
            "randomPage": randoness().randoInst2(),
        })


def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            titleo = form.cleaned_data["title"]
            bodyo = form.cleaned_data["body"]
            if util.get_entry(form.cleaned_data["title"]) != None:
                return render(request, "wiki/errorpage.html", {
                    "title": form.cleaned_data["title"].upper(),
                    "randomPage": randoness().randoInst2(),
                })
            with open(f'entries/{titleo}.md', 'bw+') as f:
                f.write('# {}\n'.format(titleo).encode('utf-8'))
                f.write('* {}\n'.format(bodyo).encode('utf-8'))
            return HttpResponseRedirect(f"{titleo}")
    return render(request, "wiki/newPage.html", {
        "newPageForm": NewPageForm(),
        "randomPage": randoness().randoInst2(),
    })
