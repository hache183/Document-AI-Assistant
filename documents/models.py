from django.db import models
from django.contrib.auth.models import User
import os

def document_upload_path(instance, filename):
    return f'documents/{instance.uploaded_by.username}/{filename}'

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('txt', 'Text File'),
    ]
    
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=document_upload_path)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    extracted_text = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            # Determina il tipo di documento
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext == '.pdf':
                self.document_type = 'pdf'
            elif ext == '.docx':
                self.document_type = 'docx'
            elif ext == '.txt':
                self.document_type = 'txt'
        super().save(*args, **kwargs)

class DocumentQuery(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    response = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query for {self.document.title}: {self.query_text[:50]}..."