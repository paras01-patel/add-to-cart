from django.db import models

 

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    
    
class Paymentss(models.Model):
    amount = models.CharField(max_length=100 , blank=True)
    order_id = models.CharField(max_length=1000 )
    razorpay_payment_id = models.CharField(max_length=1000 ,blank=True)
    paid = models.BooleanField(default=False)