from django.contrib import admin
from .models import Bag, BagItem

# Register Bag model
admin.site.register(Bag)

# Register BagItem model
admin.site.register(BagItem)
