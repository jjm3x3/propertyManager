from django.contrib import admin

from .models import Property
from .models import Unit
from .models import TenantInfo
from .models import UnitGroup
from .models import PropertyGroup
from .models import WorkOrder 

admin.site.register(Property)
admin.site.register(Unit)
admin.site.register(TenantInfo)
admin.site.register(UnitGroup)
admin.site.register(PropertyGroup)
admin.site.register(WorkOrder)
