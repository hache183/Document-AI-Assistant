# Document AI Assistant API

## Base URL
http://localhost:8000/api/
## Authentication
Tutte le API richiedono autenticazione. Usa Django session authentication o token authentication.

## Endpoints

### Documents

#### GET /api/documents/
Lista tutti i documenti

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Sample Document",
      "file_url": "http://localhost:8000/media/documents/user/sample.pdf",
      "document_type": "pdf",
      "summary": "This is a sample document summary",
      "uploaded_by": "username",
      "uploaded_at": "2024-01-15T10:30:00Z",
      "file_size": 1024
    }
  ]
}