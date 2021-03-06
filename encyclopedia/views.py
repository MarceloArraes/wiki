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
    title = forms.CharField(label="title", initial='')
    body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}), label='')
    edition = forms.BooleanField(widget=forms.HiddenInput(),
                                 initial=False, label="edition", required=False)


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
            "notice": "Page not Found.",
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
        title = "wiki/"+search.upper()
        return render(request, "wiki/titles.html", {
            "title": title,
            "page": Markdown().convert(text),
            "randomPage": randoness().randoInst2(),
        })


def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            titleo = form.cleaned_data["title"]
            bodyo = form.cleaned_data["body"]
            edit = form.cleaned_data["edition"]
            if util.get_entry(form.cleaned_data["title"]) != None and not edit:
                return render(request, "wiki/errorpage.html", {
                    "title": form.cleaned_data["title"].upper(),
                    "randomPage": randoness().randoInst2(),
                })
            util.save_entry(titleo, bodyo)
            return HttpResponseRedirect(f"{titleo}")
    return render(request, "wiki/newPage.html", {
        "newPageForm": NewPageForm(),
        "randomPage": randoness().randoInst2(),
    })


def editpage(request, pagename):
    form = NewPageForm()
    entrada = util.get_entry(pagename)
    form.fields['body'].initial = entrada
    form.fields["title"].initial = pagename
    form.fields["edition"].initial = True
    return render(request, "wiki/newPage.html", {
        "form": form,
        "pagename": pagename,
    })
