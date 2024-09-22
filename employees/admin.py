from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employees.models import Employee, Position, Team


admin.site.register(Employee, UserAdmin)
admin.site.register(Position)
admin.site.register(Team)
