import tempfile
import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Document, DocumentQuery
from .utils import extract_text_from_file

class DocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_document_creation(self):
        document = Document.objects.create(
            title='Test Document',
            uploaded_by=self.user,
            document_type='txt'
        )
        self.assertEqual(document.title, 'Test Document')
        self.assertEqual(document.uploaded_by, self.user)
        self.assertEqual(str(document), 'Test Document')

class DocumentViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Document AI Assistant')
    
    def test_document_list_view(self):
        response = self.client.get(reverse('document_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_upload_view_get(self):
        response = self.client.get(reverse('upload_document'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carica Nuovo Documento')

class UtilsTest(TestCase):
    def test_extract_text_from_txt(self):
        # Test con file temporaneo (funziona su tutti i sistemi)
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tmp_file:
            tmp_file.write("Questo è un test")
            tmp_file_path = tmp_file.name
        
        try:
            result = extract_text_from_file(tmp_file_path, 'txt')
            self.assertIn('test', result)
        finally:
            # Pulizia
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)