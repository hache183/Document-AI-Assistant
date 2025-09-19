from django import forms
from .models import Document, DocumentQuery

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inserisci titolo del documento'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.docx,.txt'
            })
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Controllo dimensione (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Il file non può superare i 10MB")
            
            # Controllo estensione
            allowed_extensions = ['.pdf', '.docx', '.txt']
            import os
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("Sono supportati solo file PDF, DOCX e TXT")
        
        return file

class DocumentQueryForm(forms.ModelForm):
    class Meta:
        model = DocumentQuery
        fields = ['query_text']
        widgets = {
            'query_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Fai una domanda sul documento...'
            })
        }