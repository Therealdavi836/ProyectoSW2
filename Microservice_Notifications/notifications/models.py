from django.db import models

# Create your models here.

class Notification(models.Model):
    user_id = models.IntegerField()  # viene del Auth MS (no FK real)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type_choices = [
        ('info', 'Info'), 
        ('warning', 'Warning'), 
        ('success', 'Success'),
        ('error', 'Error'),
        ('publication', 'Publication'),
        ('sales', 'Sales'),
        ('system', 'System'),
    ]
    type = models.CharField(max_length=50, choices=type_choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} -> User {self.user_id}"