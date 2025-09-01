from functools import wraps

from rest_framework.response import Response

from .models import UserRole, AccessRoleRule, BusinessElement


def has_permission(user, element_code, action, own_only=False):
    if not user or not user.is_authenticated:
        return False

    try:
        element = BusinessElement.objects.get(code=element_code)
    except BusinessElement.DoesNotExist:
        return False

    role_ids = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
    rules = AccessRoleRule.objects.filter(role_id__in=role_ids, element=element)

    for rule in rules:
        if action == 'read' and rule.can_read:
            if own_only and not rule.can_read_all:
                return False
            return True

        if action == 'create' and rule.can_create:
            return True

        if action == 'update' and rule.can_update:
            if own_only and not rule.can_update_all:
                return False
            return True

        if action == 'delete' and rule.can_delete:
            if own_only and not rule.can_delete_all:
                return False
            return True

    return False


def permission_required(element_code, action, own_only=False):
    def decorator(view_funk):
        @wraps(view_funk)
        def wrapper(view_instance, request, *args, **kwargs):
            if not has_permission(request.user, element_code, action, own_only):
                return Response({'error': 'Forbidden'}, status=403)
            return view_funk(view_instance, request, *args, **kwargs)
        return wrapper
    return decorator