
from django.shortcuts import render, redirect

def index(request):
	return render(request, 'disappearing_ninjas/index.html')

def show(request, color):
	turtles = {
		'blue':'disappearing_ninjas/images/leonardo.jpg',
		'orange':'disappearing_ninjas/images/michelangelo.jpg',
		'red':'disappearing_ninjas/images/raphael.jpg',
		'purple':'disappearing_ninjas/images/donatello.jpg',
		'all':'disappearing_ninjas/images/tmnt.png'
	}
	if color in turtles:
		context = {
			'image': turtles[color]
		}
	else:
		context = {
			'image':'disappearing_ninjas/images/notapril.jpg'
		}
	return render(request, 'disappearing_ninjas/show.html', context)
