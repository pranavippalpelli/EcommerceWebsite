from django.db import models

#data base is written in models page

# Create your models here.
#write code here and after saving write two commands:-> python manage.py makemigrations , python manage.py migrate
#register model in admin.py
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email =models.EmailField()
    desc = models.TextField(max_length=500)
    phonenumber = models.IntegerField()

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default = "")
    subcategory = models.CharField(max_length=50, default = "")
    price = models.IntegerField(default = 0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/images')

    def __str__(self):
        return self.product_name
    


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=110)
    address = models.CharField(max_length=110)
    city = models.CharField(max_length=110)
    state = models.CharField(max_length=110)
    zip_code = models.CharField(max_length=110)
    phone = models.CharField(max_length=110)
    def __str__(self):
        return self.name
    

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.update_desc[0:7] + "..."


    