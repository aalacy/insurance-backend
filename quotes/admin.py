from django.contrib import admin

# Register your models here.
from .models import QuoteShell, Quote, Driver, Vehicle

admin.site.register(QuoteShell)
admin.site.register(Quote)
admin.site.register(Driver)
admin.site.register(Vehicle)
