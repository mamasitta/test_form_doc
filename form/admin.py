from django.contrib import admin
from .models import Form, FormFields, Application, ApplicationFields

# Register your models here.
admin.site.register(Form),
admin.site.register(FormFields),
admin.site.register(Application),
admin.site.register(ApplicationFields),


