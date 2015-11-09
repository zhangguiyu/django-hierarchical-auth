from django.contrib import admin
from django.conf import settings


from models import Group, User  # this takes care of custom users Etc.
from django.contrib.auth.admin import GroupAdmin

try:
    module_name, class_name = settings.AUTH_USER_ADMIN_CLASS.rsplit('.', 1)
    mod = __import__(module_name, fromlist=[class_name])
    UserAdmin = getattr(mod, class_name)
except:
    from django.contrib.auth.admin import UserAdmin

UserChangeForm = UserAdmin.form

try:
    from django.utils.encoding import force_text
except ImportError:  # pragma: no cover (Django 1.4 compatibility)
    from django.utils.encoding import force_unicode as force_text
from django.utils.translation import ugettext as _

from mptt.forms import TreeNodeMultipleChoiceField

if getattr(settings, 'MPTT_USE_FEINCMS', False):
    from mptt.admin import FeinCMSModelAdmin as MasterModelAdmin
else:
    from mptt.admin import MPTTModelAdmin as MasterModelAdmin


class GroupMPTTModelAdmin(GroupAdmin, MasterModelAdmin):
    list_display = ['name', 'id', 'parent']
    list_filter = ['name', 'parent']
    ordering = ['id',]
    pass
    def delete_selected_tree(self, modeladmin, request, queryset):
        """
        kuiyu: copied from MPTTModelAdmin.py, needed for batch deletes 
        """
        # If this is True, the confirmation page has been displayed
        if request.POST.get('post'):
            n = 0
            #with queryset.model.objects.delay_mptt_updates():
            for obj in queryset:
                if self.has_delete_permission(request, obj):
                    obj.delete()
                    n += 1
                    obj_display = force_text(obj)
                    self.log_deletion(request, obj, obj_display)
            self.message_user(
                request,
                _('Successfully deleted %(count)d items.') % {'count': n})
            # Return None to display the change list page again
            return None
        else:
            # (ab)using the built-in action to display the confirmation page
            return super(GroupMPTTModelAdmin, self).delete_selected_tree(self, request, queryset)

admin.site.unregister(Group)
admin.site.register(Group, GroupMPTTModelAdmin)

class UserWithMPTTChangeForm(UserChangeForm):
    groups = TreeNodeMultipleChoiceField(queryset=Group.objects.all())

class UserWithMPTTAdmin(UserAdmin):
    form = UserWithMPTTChangeForm

admin.site.unregister(User)
admin.site.register(User, UserWithMPTTAdmin)
