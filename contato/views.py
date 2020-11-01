from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import EmailMessage
# Create your views here.


def contact(request):
    send = False
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # enviar e-mail
        nome = request.POST.get('nome', '')
        email = request.POST.get('email', '')
        telefone = request.POST.get('telefone', '')
        mensagem = request.POST.get('mensagem', '')
        email = EmailMessage(
            'Mensagem do Blog Django',
            f'De {nome} {telefone} <{email}> Escreveu: \n\n{mensagem}',
            'no-replay@inbox.mailtrap.io',
            ['leonardoferreiragraciano@gmail.com'],
            reply_to=[email],
        )
        try:
            email.send()
            send = True
        except:
            send = False

    context = {
        'form': form,
        'success': send,
    }
    return render(request, 'contato/contact.html', context)
