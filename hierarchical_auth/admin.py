from django.contrib import admin
from django.conf import settings
from django.db.models import get_model

from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.forms import UserChangeForm

try:    
    from django.contrib.auth import get_user_model
    User = get_user_model()
except:
    from django.contrib.auth.models import User
    
try:
    module_name, class_name = settings.AUTH_USER_ADMIN_CLASS.rsplit('.', 1)
    mod = __import__(module_name, fromlist=[class_name])
    UserAdmin = getattr(mod, class_name)    
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
