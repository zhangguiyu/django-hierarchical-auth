from django.contrib import admin
from django.conf import settings
from django.db.models import get_model

from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.forms import UserChangeForm

try:    
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')    
    User = get_model(app_label, model_name)        
except:
    from django.contrib.auth.models import User
    
try:
    app_label, model_name = settings.AUTH_USER_ADMIN_MODEL.split('.')    
    UserAdmin = get_model(app_label, model_name)
except:
    from django.contrib.auth.admin import UserAdmin

from mptt.forms import TreeNodeMultipleChoiceField

if getattr(settings, 'MPTT_USE_FEINCMS', False):
    from mptt.admin import FeinCMSModelAdmin
    class GroupMPTTModelAdmin(GroupAdmin, FeinCMSModelAdmin):
        pass
else:
    from mptt.admin import MPTTModelAdmin
    class GroupMPTTModelAdmin(GroupAdmin, MPTTModelAdmin):
        pass

admin.site.unregister(Group)
admin.site.register(Group, GroupMPTTModelAdmin)

class UserWithMPTTChangeForm(UserChangeForm):
    groups = TreeNodeMultipleChoiceField(queryset=Group.tree.all())

class UserWithMPTTAdmin(UserAdmin):
    form = UserWithMPTTChangeForm

admin.site.unregister(User)
admin.site.register(User, UserWithMPTTAdmin)
