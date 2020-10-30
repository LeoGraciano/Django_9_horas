from django.contrib import admin
from .models import Post
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'publicado', 'status',)
    list_filter = ('status', 'criado', 'publicado', 'autor',)
    search_fields = ('titulo', 'conteudo', 'autor',)
    raw_id_fields = ('autor',)
    # Prepopulaterd_fields = alto cria já o url para link.
    prepopulated_fields = {'slug':  ('titulo',)}
