from django.shortcuts import render, redirect

def index(request):
	return render(request, 'survey_form/index.html')

def process(request):
        if not 'count' in request.session:
            request.session['count'] = 0
        if request.session['count'] ='POST'
            request.session['location'] = request.POST ['location']
            request.session['language'] = request.POST ['language']
            request.session['comment'] = request.POST ['comment']
            request.session['count'] = request.POST += 1
            return redirect('/result')
        return redirect('/')

def result(request):
        return render (request, 'survey_form/result.html')
# Create your views here.
