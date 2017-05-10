from django.shortcuts import render, redirect

def index(request):
	return render(request, 'survey_form/index.html')

def process(request):
	if not 'count' in request.session:
		request.session['count'] = 0
	if request.method == 'POST':
		request.session['name'] = request.POST['name']
		request.session['location'] = request.POST['location']
		request.session['language'] = request.POST['language']
		request.session['comment'] = request.POST['comment']
		request.session['count'] += 1
		return redirect('/result')
	return redirect('/')

def result(request):
	return render(request, 'survey_form/result.html')