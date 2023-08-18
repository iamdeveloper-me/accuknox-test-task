from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db.models import UniqueConstraint


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Convert email to lowercase before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.email)
    

class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    recepient = models.ForeignKey(
        User, related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recepient')
