"""
Management command for initial system setup
"""
import os
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
import getpass

class Command(BaseCommand):
    help = 'Initial system setup including creating admin user'

    def validate_password_match(self, password1, password2):
        """Validate that passwords match"""
        if password1 != password2:
            raise ValidationError("Passwords don't match")
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        return True

    def get_valid_input(self, prompt, validator=None, password=False):
        """Get and validate user input"""
        while True:
            try:
                if password:
                    value = getpass.getpass(prompt)
                else:
                    value = input(prompt)
                
                if validator:
                    validator(value)
                return value
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f"Error: {e.message}"))
            except KeyboardInterrupt:
                self.stdout.write("\nSetup cancelled.")
                sys.exit(1)

    def handle(self, *args, **options):
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists. Skipping initial setup.'))
            return

        self.stdout.write(self.style.SUCCESS('Starting initial system setup...'))
        
        try:
            # Get email
            email = self.get_valid_input(
                'Enter admin email: ',
                validate_email
            )

            # Get username
            username = self.get_valid_input(
                'Enter admin username: ',
                lambda x: None if len(x) >= 3 else ValidationError("Username must be at least 3 characters long")
            )

            # Get and confirm password
            while True:
                password1 = self.get_valid_input(
                    'Enter admin password: ',
                    password=True
                )
                password2 = self.get_valid_input(
                    'Confirm admin password: ',
                    password=True
                )
                
                try:
                    self.validate_password_match(password1, password2)
                    break
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f"Error: {e.message}"))

            # Create superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password1
            )

            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
            
            # Create .env file if it doesn't exist
            env_path = os.path.join(settings.BASE_DIR, '.env')
            if not os.path.exists(env_path):
                with open(env_path, 'w') as f:
                    f.write(f"DJANGO_SUPERUSER_EMAIL={email}\n")
                    f.write(f"DJANGO_SUPERUSER_USERNAME={username}\n")
                
                self.stdout.write(self.style.SUCCESS('.env file created with admin email and username'))

        except KeyboardInterrupt:
            self.stdout.write("\nSetup cancelled.")
            sys.exit(1)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during setup: {str(e)}'))
            sys.exit(1)
