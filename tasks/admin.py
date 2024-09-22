from django.contrib import admin

from tasks.models import TaskTag, TaskType, Task, Project

admin.site.register(TaskTag)
admin.site.register(TaskType)
admin.site.register(Task)
admin.site.register(Project)
