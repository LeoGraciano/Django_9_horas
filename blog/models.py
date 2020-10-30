from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='publicado')


class Category(models.Model):
    nome = models.CharField(max_length=50, verbose_name='Nome')
    publicado = models.DateTimeField(
        default=timezone.now, verbose_name='Publicado')
    criado = models.DateTimeField(auto_now_add=True, verbose_name='Criado')

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS = {
        ('rascunho', 'Rascunho'),
        ('publicado', 'Pulbicado')
    }
    titulo = models.CharField(verbose_name='Título',  max_length=250)
    slug = models.SlugField(verbose_name='Link', max_length=250)
    autor = models.ForeignKey(User,
                              on_delete=CASCADE, verbose_name='Autor')
    categoria = models.ManyToManyField(
        Category, related_name='get_pots', verbose_name='Categoria')
    conteudo = models.TextField(verbose_name='Conteúdo')
    publicado = models.DateTimeField(
        default=timezone.now, verbose_name='Publicado')
    criado = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    alterado = models.DateTimeField(auto_now=True, verbose_name='Alterado')
    status = models.CharField(max_length=10,
                              choices=STATUS,
                              default='rascunho', verbose_name='Status')

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    def get_absolute_url_update(self):
        return reverse('post_edit', args=[self.slug])

    def get_absolute_url_delete(self):
        return reverse('post_delete', args=[self.pk])

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


@receiver(post_save, sender=Post)
def insert_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.titulo)
        return instance.save()
