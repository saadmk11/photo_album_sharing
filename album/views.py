from django.shortcuts import render


def index(request):
    return render(request, "album/index.html", {})
