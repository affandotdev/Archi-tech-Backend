"""
Django management command to create an admin superuser.
Usage: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates an admin superuser with predefined credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='admin@architech.com',
            help='Email address for the admin user'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password for the admin user'
        )
        parser.add_argument(
            '--first-name',
            type=str,
            default='Admin',
            help='First name for the admin user'
        )
        parser.add_argument(
            '--last-name',
            type=str,
            default='User',
            help='Last name for the admin user'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing admin user if it already exists'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']
        update = options['update']

        # Check if admin already exists
        if User.objects.filter(email=email).exists():
            if update:
                admin = User.objects.get(email=email)
                admin.set_password(password)
                admin.is_staff = True
                admin.is_superuser = True
                admin.is_active = True
                admin.is_verified = True
                admin.role = "admin"
                admin.first_name = first_name
                admin.last_name = last_name
                admin.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Admin password updated successfully!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  Admin user with email "{email}" already exists! '
                        f'Use --update flag to update the password.'
                    )
                )
                return
        else:
            # Create admin superuser
            try:
                admin = User.objects.create_superuser(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role="admin",
                    is_verified=True,
                    is_active=True,
                )
                self.stdout.write(
                    self.style.SUCCESS('✅ Admin superuser created successfully!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creating admin: {str(e)}')
                )
                return

        # Display credentials
        self.stdout.write(self.style.SUCCESS('\n📋 Admin Login Credentials:'))
        self.stdout.write(self.style.SUCCESS(f'   Email: {email}'))
        self.stdout.write(self.style.SUCCESS(f'   Password: {password}'))
        self.stdout.write(self.style.SUCCESS('\n🔗 Access Django Admin at: http://localhost:8000/admin/'))

