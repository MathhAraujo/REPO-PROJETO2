from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Sponsor)
admin.site.register(Course)