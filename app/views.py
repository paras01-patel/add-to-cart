from django.shortcuts import render, redirect
from .models import Product

def landing(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        color = request.POST.get('color')
        gender = request.POST.get('gender')
        quality = request.POST.get('quality')
        price = request.POST.get('price')
        category = request.POST.get('category')

        Product.objects.create(
            name=name,
            description=description,
            color=color,
            gender=gender,
            quality=quality,
            price=price,
            category=category
        )

        return redirect('show')   # 👈 yaha bhej raha hai dusre page pe

    return render(request, 'landing.html')


def show(request):
    data = Product.objects.all()
    return render(request, 'show.html', {'data': data})



def save(req,pk):
    cart=req.session.get('cart',[])
    print(cart)
    if pk in cart:
        data = Product.objects.all()
        return render(req,'show.html',{'data':data})
    else:
        cart.append(pk)
        print(cart)
        req.session['cart']=cart
        data = Product.objects.all()
        return render(req,'show.html',{'data':data})


def show_cart(req):
    return render(req,'show_cart.html')

def delete(req,pk):
    data=Product.objects.get(pk=id)
    data.delete()
    return redirect('show_cart')



    
    
