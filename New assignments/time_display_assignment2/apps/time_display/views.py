from django.shortcuts import render
import datetime

def index(request):
        current = {
                "time":datetime.datetime.now()
        }
        return render(request, 'time_display/index.html', current)
