from rest_framework import serializers
from .models import Document, DocumentQuery

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_url', 'document_type', 'summary', 
                 'uploaded_by', 'uploaded_at', 'file_size']
        read_only_fields = ['document_type', 'summary', 'uploaded_by', 
                           'uploaded_at', 'file_size']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

class DocumentQuerySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = DocumentQuery
        fields = ['id', 'query_text', 'response', 'created_by', 'created_at']
        read_only_fields = ['response', 'created_by', 'created_at']

class DocumentQueryCreateSerializer(serializers.Serializer):
    query_text = serializers.CharField(max_length=1000)
    
    def validate_query_text(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("La domanda deve essere di almeno 3 caratteri")
        return value