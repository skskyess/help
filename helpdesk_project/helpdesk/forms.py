from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'phone', 'email', 'description', 'priority', 'status', 'actions', 'assigned_user', 'resolved_user']
        widgets = {
            'status': forms.Select(choices=Ticket.STATUS_CHOICES),
            'actions': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'assigned_user': forms.Select(attrs={'class': 'form-control'}),
            'resolved_user': forms.Select(attrs={'class': 'form-control'}),
        }
