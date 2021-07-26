import random

from django.shortcuts import redirect
from django.shortcuts import render
from markdown2 import Markdown

from . import util
from .forms import CreateForm


def index(request):
    entries = util.list_entries()
    query_params = request.GET
    search = None

    if 'q' in query_params:
        search = query_params['q']

    if search in entries:
        return redirect('show', search)

    return render(request, "encyclopedia/index.html", {
        "q": search,
        "entries": entries
    })


def show(request, name):
    entry = util.get_entry(name)
    markdowner = Markdown()

    if entry is None:
        return redirect('404')

    return render(request, "encyclopedia/show.html", {
        "name": name,
        "entry": markdowner.convert(entry)
    })


def random_entry(request):
    entries = util.list_entries()
    return redirect('show', random.choice(entries))


def create(request):
    entries = util.list_entries()
    generic_error = None

    if request.method == 'POST':
        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']

            if title in entries:
                generic_error = 'Entry already exists, please, change the Title'
                return render(request, "encyclopedia/create.html", {
                    'form': form,
                    'generic_error': generic_error
                })

            util.save_entry(title, form.cleaned_data['content'])

            return redirect('show', title)
        else:
            return render(request, "encyclopedia/create.html", {
                'form': form
            })
    else:
        form = CreateForm()

        return render(request, "encyclopedia/create.html", {
            'form': form
        })


def edit(request, name):
    entries = util.list_entries()
    generic_error = None

    if request.method == 'POST':
        form = CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']

            if title in entries and name != title:
                generic_error = 'Entry already exists, please, change the Title'
                return render(request, "encyclopedia/edit.html", {
                    'form': form,
                    'generic_error': generic_error,
                    'name': name
                })

            util.save_entry(title, form.cleaned_data['content'])

            return redirect('show', title)
        else:
            return render(request, "encyclopedia/edit.html", {
                'form': form,
                'name': name
            })
    else:
        content = util.get_entry(name)
        fields = {'title': name, 'content': content}
        form = CreateForm(fields)

        return render(request, "encyclopedia/edit.html", {
            'form': form,
            'name': name
        })


def not_found(request):
    return render(request, "encyclopedia/404.html")
