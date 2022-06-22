from rest_framework.permissions import IsAdminUser
class OrderUpsertPermission(IsAdminUser):
    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                _id = request.POST.get("_id",None)
            except:
                return super().has_permission(request, view)


            if _id :
                return super().has_permission(request, view)
            else:
                return True
        else:
            return False