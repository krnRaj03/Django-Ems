from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(slider)
admin.site.register(banner)
admin.site.register(main_category)
admin.site.register(sub_category)
admin.site.register(subsub_category)
#####

class prod_img(admin.TabularInline):
  model=product_image

class add_info(admin.TabularInline):
  model=additional_info

class product_admin(admin.ModelAdmin):
  inlines= (prod_img,add_info)
  list_display=('product_name','price','s_category','sec')
  list_editable=('s_category','sec')

admin.site.register(section)
admin.site.register(product,product_admin)
admin.site.register(product_image)
admin.site.register(additional_info)