from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from .forms import TicketForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User


@login_required
def ticket_list(request):
    tickets = Ticket.objects.exclude(status='resolved')
    if request.user.groups.filter(name='Reception').exists():
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(assigned_user=request.user)
    return render(request, 'helpdesk/ticket_list.html', {'tickets': tickets})


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            reception_group = Group.objects.get(name='Reception')
            users_in_reception = reception_group.user_set.all()
            if users_in_reception.exists():
                ticket.assigned_user = users_in_reception.first()
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'helpdesk/create_ticket.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            if ticket.status != 'resolved':
                ticket = form.save()
                ticket.resolved_user = request.user
                ticket.status = 'resolved'
                ticket.assigned_user = User.objects.filter(groups__name='Tester').first()
                ticket.save()
            else:
                form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)

    can_edit = ticket.status != 'resolved'
    
    return render(request, 'helpdesk/ticket_detail.html', {'ticket': ticket, 'form': form,  'can_edit': can_edit})

