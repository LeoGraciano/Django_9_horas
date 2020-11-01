from django import forms
from django.core.validators import RegexValidator


class ContactForm(forms.Form):
    nome = forms.CharField(label="Nome", widget=forms.TextInput(
        attrs={'placeholder': 'Digite seu nome'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(
        attrs={'placeholder': 'Digite seu e-mail'}))
    telefone = forms.CharField(label="Telefone",
                               error_messages={
                                   'Incompleto': 'Digite um código de chamada do país.'
                               },
                               validators=[
                                   RegexValidator(
                                       r'^[0-9]+$', 'Digite um código de chamada válido do país.'
                                   ),
                               ],
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Digite seu telefone'}))
    mensagem = forms.CharField(label="Mensagem", widget=forms.Textarea(
        attrs={'placeholder': 'Digite seu assunto'}))
