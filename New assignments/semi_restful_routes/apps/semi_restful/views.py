from django.shortcuts import render, redirect
from models import Product

def products(request):
	if request.method == 'POST':
		return create(request)
	else:
		return index(request)

def index(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'index.html', context)

def create(request):
	print request.POST
	product = {
		'name': request.POST['name'],
		'description': request.POST['description'],
		'price': request.POST['price']
	}
	newProduct = Product(**product)
	newProduct.save()
	return redirect('/products')

def products_w_id(request, id):
	if request.method == 'POST':
		return update(request, id)
	else:
		return show(request, id)

def show(request, id):
	product = Product.objects.get(id=id)
	context = {'product': product}
	return render(request, 'show.html', context)

def update(request, id):
	product = Product.objects.get(id=id)
	product['name'] = request.POST['name']
	product['description'] = request.POST['description']
	product['price'] = request.POST['price']
	product.save()
	return redirect('/products')

def new(request):
	return render(request, 'create.html')

def edit(request, id):
	product = Product.objects.get(id=id)
	context = {'product': product}
	return render(request, 'edit.html', context)

def destroy(request, id):
	product = Product.objects.get(id=id)
	product.delete()
	return redirect('/products')
