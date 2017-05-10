from django.shortcuts import render
import datetime
now= datetime.datetime.now()
def index(request):
    context = {
    "date": now.strftime("%A, %B %d,%Y"),
    "time": now.strftime("%H:%M %p")
    }
    return render(request,'timedisplay/index.html', context)
    # Create your views here.
