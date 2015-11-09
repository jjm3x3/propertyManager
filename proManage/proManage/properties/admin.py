from django.contrib import admin

from .models import Property
from .models import Unit
from .models import TenantInfo
from .models import UnitGroup 

admin.site.register(Property)
admin.site.register(Unit)
admin.site.register(TenantInfo)
admin.site.register(UnitGroup)
