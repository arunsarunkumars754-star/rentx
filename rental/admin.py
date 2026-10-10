from django.contrib import admin
from .models import CUSTOMERS, VEHICLES, VEHICLE_CATEGORY, BOOKING, REPORT, PAYMENT, RENTAL, CANCELLATION

admin.site.register(CUSTOMERS)
admin.site.register(VEHICLES)
admin.site.register(VEHICLE_CATEGORY)
admin.site.register(BOOKING)
admin.site.register(REPORT)
admin.site.register(PAYMENT)
admin.site.register(RENTAL)
admin.site.register(CANCELLATION)
