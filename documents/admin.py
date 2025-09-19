from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Document, DocumentQuery

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'uploaded_by', 'uploaded_at', 'file_size']
    list_filter = ['document_type', 'uploaded_at', 'uploaded_by']
    search_fields = ['title', 'summary']
    readonly_fields = ['uploaded_at', 'file_size', 'document_type', 'extracted_text']
    
    fieldsets = (
        ('Informazioni Base', {
            'fields': ('title', 'file', 'uploaded_by')
        }),
        ('Dettagli Documento', {
            'fields': ('document_type', 'file_size', 'uploaded_at')
        }),
        ('Contenuto', {
            'fields': ('summary', 'extracted_text'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DocumentQuery)
class DocumentQueryAdmin(admin.ModelAdmin):
    list_display = ['document', 'query_text_short', 'created_by', 'created_at']
    list_filter = ['created_at', 'created_by', 'document']
    search_fields = ['query_text', 'response']
    readonly_fields = ['created_at']
    
    def query_text_short(self, obj):
        return obj.query_text[:50] + "..." if len(obj.query_text) > 50 else obj.query_text
    query_text_short.short_description = 'Query'