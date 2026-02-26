from django.contrib.auth.decorators import user_passes_test

def es_supervisor(user):
    if not user.is_authenticated:
        return False
    return (
        user.is_superuser
        or user.is_staff
        or user.groups.filter(name="supervisores").exists()
    )

solo_supervisor = user_passes_test(es_supervisor)