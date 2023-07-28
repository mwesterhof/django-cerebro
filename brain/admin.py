from django.contrib import admin

from .models import VisitorBehavior


class VisitorBehaviorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'conversion_target_a', 'conversion_target_b')
    list_filter = ('conversion_target_a', 'conversion_target_b')


admin.site.register(VisitorBehavior, VisitorBehaviorAdmin)
