from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe

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

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-criado']

    def __str__(self):
        return self.nome


class Post(models.Model):
    STATUS = {
        ('rascunho', 'Rascunho'),
        ('publicado', 'Pulbicado')
    }
    titulo = models.CharField(verbose_name='Título',  max_length=250)
    subtitulo = models.CharField(verbose_name='Sub-Título',  max_length=100)
    slug = models.SlugField(verbose_name='Link', max_length=250, unique=True)
    autor = models.ForeignKey(User,
                              on_delete=CASCADE, verbose_name='Autor')
    categoria = models.ManyToManyField(
        Category, related_name='get_pots', verbose_name='Categoria')
    conteudo = RichTextField(verbose_name='Conteúdo')
    publicado = models.DateTimeField(
        default=timezone.now, verbose_name='Publicado')
    criado = models.DateTimeField(auto_now_add=True, verbose_name='Criado')
    alterado = models.DateTimeField(auto_now=True, verbose_name='Alterado')
    status = models.CharField(max_length=10,
                              choices=STATUS,
                              default='rascunho', verbose_name='Status')
    imagem = models.ImageField(upload_to='blog', blank=True, null=True)

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    def get_absolute_url_update(self):
        return reverse('post_edit', args=[self.slug])

    def get_absolute_url_delete(self):
        return reverse('post_delete', args=[self.pk])

    @property
    def view_image(self):
        return mark_safe('<img src="%s" width="150px" />' % self.imagem.url)
        view_image.short_description = "Imagem Cadastrada"
        view_image.allow_tags = True

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


@receiver(post_save, sender=Post)
def insert_slug(sender, instance, **kwargs):
    if kwargs.get('created', False):
        print('Criado Slug')
    if not instance.slug:
        instance.slug = slugify(instance.titulo)
        return instance.save()
