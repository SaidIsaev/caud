from django.contrib.auth.models import Group

def current_user_role(request):
    user = request.user
    if not user.is_authenticated:
        return {'current_user_role': 'guest'}
    if user.is_superuser:
        return {'current_user_role': 'admin'}
    elif user.groups.exists():
        # Return first group name as role
        role = user.groups.first().name
        return {'current_user_role': role}
    return {'current_user_role': 'guest'}
