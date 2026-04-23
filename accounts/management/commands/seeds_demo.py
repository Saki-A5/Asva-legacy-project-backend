from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="demo").exists():
            User.objects.create_user(
                username="demo",
                email="demo@gmail.com",
                password="demo1234"
            )
            self.stdout.write(self.style.SUCCESS("Demo user created"))
        else:
            self.stdout.write("Demo user already exists")