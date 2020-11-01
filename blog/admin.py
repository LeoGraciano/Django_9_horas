from django.contrib import admin
from .models import Post, Category
# Register your models here.


@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado', 'publicado',)
    list_filter = ('nome', 'criado', 'publicado',)
    data_hierarchy = 'publicado'
    search_fields = ('nome', 'criado', 'publicado',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'autor', 'publicado', 'status',)
    list_filter = ('status', 'criado', 'publicado', 'autor',)
    readonly_fields = ('visualizar_imagem',)
    raw_id_fields = ('autor',)
    data_hierarchy = 'nome'
    search_fields = ('titulo', 'conteudo', 'autor',)
    raw_id_fields = ('autor',)
    # Prepopulaterd_fields = alto cria já o url para link.
    prepopulated_fields = {'slug':  ('titulo',)}

    def visualizar_imagem(self, obj):
        return obj.view_image
    visualizar_imagem.short_description = "Imagem Cadastrada"
