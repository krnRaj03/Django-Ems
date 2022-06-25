from django.shortcuts import render
from . models import *
# Create your views here.

def home(request):
  sliders= slider.objects.all().order_by('-id')[0:3]
  banners= banner.objects.all().order_by('-id')[0:3]
  m_category=main_category.objects.all()
  s_category=sub_category.objects.all()
  ss_category=subsub_category.objects.all()
  prod=product.objects.filter(sec__name="Top Deals of the Day")

  context={'sliders':sliders,'banners':banners,'main_category':m_category,
  'sub_category':s_category,"subsub_category":ss_category, "products":prod}
 
  return render(request,"main/home.html",context)