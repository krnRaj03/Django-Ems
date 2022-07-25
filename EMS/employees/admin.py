from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.
@admin.register(employeeDetails)
class empDetailsAdmin(ImportExportModelAdmin):
  pass

admin.site.register(employeeEducation)
admin.site.register(employeeExperience)
admin.site.register(employeeImage)