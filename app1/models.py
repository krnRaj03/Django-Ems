from distutils.command.upload import upload
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class slider(models.Model):
  dis_deal=(('Hot deals','Hot deals'),('New arrivals','New arrivals'))

  image=models.ImageField(upload_to='media/slider_imgs')
  discount_deal=models.CharField(choices=dis_deal, max_length=100)
  sale=models.IntegerField()
  brand_name=models.CharField(max_length=200)
  discount= models.IntegerField()
  link=models.CharField(max_length=200)
  def __str__(self):
    return self.brand_name

class banner(models.Model):
  image=models.ImageField(upload_to='media/banner_imgs')
  discount_deal=models.CharField(max_length=100)
  quote=models.CharField(max_length=100)
  discount= models.IntegerField()
  link=models.CharField(max_length=200, null=True)
  def __str__(self):
    return self.quote

class main_category(models.Model):
  name=models.CharField(max_length=200)
  def __str__(self):
    return self.name

class sub_category(models.Model):
  main_category1= models.ForeignKey(main_category,on_delete=models.CASCADE)
  name=models.CharField(max_length=200)
  def __str__(self):
    return self.name+"--"+ self.main_category1.name

class subsub_category(models.Model):
  sub_category1= models.ForeignKey(sub_category,on_delete=models.CASCADE)
  name=models.CharField(max_length=200)
  def __str__(self):
    return self.sub_category1.main_category1.name+"--"+self.sub_category1.name+"--"+self.name

class section(models.Model):
  name=models.CharField(max_length=100)
  def __str__(self):
    return self.name

class product(models.Model):
  total_quantity=models.IntegerField()
  availability=models.IntegerField()
  featured_image=models.CharField(max_length=200)
  product_name=models.CharField(max_length=200)
  price=models.IntegerField()
  discount=models.IntegerField()
  product_info=RichTextField()
  model_name=models.CharField(max_length=200)
  s_category=models.ForeignKey(sub_category,on_delete=models.CASCADE)
  tags=models.CharField(max_length=200)
  description=RichTextField(null=True)
  sec=models.ForeignKey(section, on_delete=models.CASCADE)
  def __str__(self):
    return self.product_name

class product_image(models.Model):
  prod=models.ForeignKey(product,on_delete=models.CASCADE)
  image_url=models.CharField(max_length=200)

class additional_info(models.Model):
  prod=models.ForeignKey(product,on_delete=models.CASCADE)
  specification=models.CharField(max_length=200)
  detail=models.CharField(max_length=200)