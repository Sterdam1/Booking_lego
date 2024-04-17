from django.contrib import admin
from .models import NewField, Profile

class NewFieldAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
            if request.user.is_superuser:
                return ()
            return ('created_by',) 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь не является суперпользователем, фильтруем объекты по создавшему их пользователю
        if not request.user.is_superuser:
            qs = qs.filter(created_by=request.user)
        return qs
     
    def has_change_permission(self, request, obj=None):
        # Проверяем, имеет ли пользователь право на изменение объекта
        if obj is not None and not request.user.is_superuser and obj.created_by != request.user:
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.save()

# Register your models here.
admin.site.register(NewField, NewFieldAdmin)
admin.site.register(Profile)