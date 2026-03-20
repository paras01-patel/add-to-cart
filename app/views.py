from django.shortcuts import render
from .models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def landing(req):
    return render(req,'landing.html')



def add_to_cart(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        category = request.POST.get("category")

        Product.objects.create(
            name=name,
            description=description,
            color=color,
            quantity=quantity,
            price=price,
            category=category
        )

        return render(request, "landing.html")  

    return render(request, "landing.html")


def show(request):
    data = Product.objects.all()
    cart = request.session.get('cart', [])
    count_c = len(cart)   
    return render(request, "my_cart.html", {
        "data": data,
        "count": count_c
    })

def save(req,pk):
    cart=req.session.get('cart',[])
    print(cart)
    if pk in cart:
        data = Product.objects.all()
        cart = req.session.get('cart', [])
        count_c = len(cart) 
        return render(req,'cart.html',{'data':data,'count':count_c})
    else:
        cart.append(pk)
        print(cart)
        req.session['cart']=cart
        data = Product.objects.all()
        cart = req.session.get('cart', [])
        count_c = len(cart) 
        return render(req,'cart.html',{'data':data,'count':count_c})


def my_cart(req):
    cart = req.session.get('cart', [])
    all_cart = []
    grand_total = 0  

    for i in cart:
        data = Product.objects.get(id=i)
        d_data = model_to_dict(data)

        item_total = float(data.price) * int(data.quantity)
        d_data['item_total'] = item_total

        grand_total += item_total  

        all_cart.append(d_data)

    return render(req, 'show_user_cart.html', {
        'all_cart': all_cart,
        'grand_total': grand_total
    })



def delete_cart_item(request, id):
    cart = request.session.get('cart', [])

    if id in cart:
        cart.remove(id) 

    request.session['cart'] = cart  

    return redirect('my_cart')  


def pay(req):
    client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
    data = { "amount": 50000, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data) 
    return render(req,'show_user_cart.html',{'payment':payment})


def payment(request):
    if request.method == "POST":
        
        amount = int(float(request.POST.get('amount'))) * 100
        
        client = razorpay.Client(auth=("rzp_test_pr99iascS1WRtU", "UTDIzPGwICnAssu3Q3lk7zUi"))
        
        data = {"amount": amount, "currency": "INR", "receipt": "order_rcptid_11"}
        payment = client.order.create(data=data)
        print(payment)

        Paymentss.objects.create(amount=amount, order_id=payment['id'])

        cart = request.session.get('cart', [])
        quantity = request.session.get('quantity', [])

        alldata = []
        total = 0
 
        for cart_id, qty in zip(cart, quantity):
            product = Product.objects.get(id=cart_id)

            total = total + (product.price)*quantity[cart_id]


            alldata.append({
                'id': product.id,
                'item_name': product.name,
                'item_desc': product.description,
                'item_price': product.price,
                'item_quantity': qty
            })

        return render(request, 'show_user_cart.html', {
            'key': alldata,
            'grand_total': total,
            'payment': payment
        })
    

        
@csrf_exempt
def payment_status(request):
    if request.method=="POST": 
        response = request.POST
        # print(response) 
        # print(payment)

        razorpay_data = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }

        # client instance
        client = razorpay.Client(auth =("rzp_test_pr99iascS1WRtU" , "UTDIzPGwICnAssu3Q3lk7zUi"))

        try:
            status = client.utility.verify_payment_signature(razorpay_data)
            product = Product.objects.get(order_id=response['razorpay_order_id'])
            product.razorpay_payment_id = response ['razorpay_payment_id']
            product.paid = True
            product.save()
            
            return render(request, 'succes.html', {'status': True})
        except:
            return render(request, 'succes.html', {'status': False})