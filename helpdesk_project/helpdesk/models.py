from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = [
    ("low", 'Низкий'),
    ("medium", 'Средний'),
    ("high", 'Высокий'),
]

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решена'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    actions = models.TextField(blank=True, null=True)

    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_tickets', null=True, blank=True)
    resolved_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='resolved_tickets', null=True, blank=True)


    def __str__(self):
        return self.name

