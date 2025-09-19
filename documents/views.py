from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Document, DocumentQuery
from .forms import DocumentUploadForm, DocumentQueryForm
from .serializers import DocumentSerializer, DocumentQuerySerializer, DocumentQueryCreateSerializer
from .utils import extract_text_from_file, generate_summary, query_document_with_ai
import os

User = get_user_model()

# Views Web
def home(request):
    recent_documents = Document.objects.all()[:5]
    total_documents = Document.objects.count()
    total_queries = DocumentQuery.objects.count()
    
    context = {
        'recent_documents': recent_documents,
        'total_documents': total_documents,
        'total_queries': total_queries,
    }
    return render(request, 'documents/home.html', context)

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            
            # Estrai testo in background
            file_path = document.file.path
            extracted_text = extract_text_from_file(file_path, document.document_type)
            document.extracted_text = extracted_text
            
            # Genera riassunto
            if extracted_text and len(extracted_text) > 100:
                summary = generate_summary(extracted_text)
                document.summary = summary
            
            document.save()
            messages.success(request, f'Documento "{document.title}" caricato con successo!')
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentUploadForm()
    
    return render(request, 'documents/upload.html', {'form': form})

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/list.html', {'documents': documents})

def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    queries = document.queries.all()[:10]  # Ultime 10 query
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Devi effettuare il login per fare domande.')
            return redirect('document_detail', pk=pk)
            
        form = DocumentQueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.document = document
            query.created_by = request.user
            
            # Genera risposta AI
            if document.extracted_text:
                response = query_document_with_ai(document.extracted_text, query.query_text)
                query.response = response
            else:
                query.response = "Testo del documento non disponibile per l'analisi."
            
            query.save()
            messages.success(request, 'Domanda inviata e risposta generata!')
            return redirect('document_detail', pk=pk)
    else:
        form = DocumentQueryForm()
    
    context = {
        'document': document,
        'queries': queries,
        'form': form,
    }
    return render(request, 'documents/detail.html', context)

# API Views
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.all()
    
    def perform_create(self, serializer):
        document = serializer.save(uploaded_by=self.request.user)
        
        # Estrai testo
        file_path = document.file.path
        extracted_text = extract_text_from_file(file_path, document.document_type)
        document.extracted_text = extracted_text
        
        # Genera riassunto
        if extracted_text and len(extracted_text) > 100:
            summary = generate_summary(extracted_text)
            document.summary = summary
        
        document.save()
    
    @action(detail=True, methods=['post'], serializer_class=DocumentQueryCreateSerializer)
    def query(self, request, pk=None):
        document = self.get_object()
        serializer = DocumentQueryCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            query_text = serializer.validated_data['query_text']
            
            # Crea query
            query = DocumentQuery.objects.create(
                document=document,
                query_text=query_text,
                created_by=request.user,
                response=""
            )
            
            # Genera risposta AI
            if document.extracted_text:
                response = query_document_with_ai(document.extracted_text, query_text)
                query.response = response
                query.save()
            
            return Response({
                'id': query.id,
                'query_text': query.query_text,
                'response': query.response,
                'created_at': query.created_at
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentQueryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DocumentQuerySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        document_id = self.request.query_params.get('document_id')
        if document_id:
            return DocumentQuery.objects.filter(document_id=document_id)
        return DocumentQuery.objects.all()