from django.contrib.auth.models import User # get_user_model  User = get_user_model()
User.objects.create_superuser('admin', 'admin@myproject.com', '111')
print('\n\nADMIN created\n\n')