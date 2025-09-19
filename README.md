# Document AI Assistant 🤖📄

Un'applicazione Django avanzata per l'analisi intelligente di documenti usando OpenAI GPT.

## 🚀 Caratteristiche

- **Upload Multi-formato**: Supporta PDF, DOCX, TXT
- **Estrazione Automatica**: Estrazione testo automatica da tutti i formati
- **Analisi AI**: Riassunti automatici e Q&A intelligente
- **API REST**: Endpoints completi per integrazione
- **Docker Ready**: Containerizzazione completa
- **UI Responsive**: Interfaccia Bootstrap moderna
- **Admin Panel**: Gestione completa dei documenti

## 🛠 Stack Tecnologico

- **Backend**: Django 4.2, Django REST Framework
- **AI**: OpenAI GPT-3.5-turbo
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite (sviluppo), PostgreSQL ready
- **Deployment**: Docker, Docker Compose

## 📋 Quick Start

### 1. Clone del Progetto
```bash
git clone https://github.com/your-username/document-ai-assistant.git
cd document-ai-assistant
```

### 2. Configurazione Ambiente
```bash
# Crea file .env
echo "DEBUG=True" > .env
echo "SECRET_KEY=django-insecure-your-secret-key" >> .env
echo "OPENAI_API_KEY=sk-your-openai-key" >> .env
```

### 3. Lancio con Docker (Consigliato)
```bash
docker-compose up --build
```

### 4. Setup Database
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

L'applicazione sarà disponibile su `http://localhost:8000`

## 🔧 Sviluppo Locale

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Database
python manage.py makemigrations
python manage.py migrate

# Avvia server
python manage.py runserver
```

## 📊 API Endpoints

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|
| `/api/documents/` | GET, POST | Lista/Crea documenti |
| `/api/documents/{id}/` | GET | Dettagli documento |
| `/api/documents/{id}/query/` | POST | Query AI documento |
| `/api/queries/` | GET | Lista query |

### Esempio API Usage:

```bash
# Upload documento
curl -X POST http://localhost:8000/api/documents/ \
  -F "title=My Document" \
  -F "file=@document.pdf"

# Query documento
curl -X POST http://localhost:8000/api/documents/1/query/ \
  -H "Content-Type: application/json" \
  -d '{"query_text": "What is this document about?"}'
```

## 🏗 Architettura

### Modelli Principali
- **Document**: Gestisce upload, estrazione testo e metadati
- **DocumentQuery**: Salva domande e risposte AI

### Componenti Chiave
- **utils.py**: Funzioni per estrazione testo e integrazione OpenAI
- **views.py**: Views web e API ViewSets
- **serializers.py**: Serializzatori per API REST
- **forms.py**: Forms Django con validazione

### Struttura Directory
```
document-ai-assistant/
├── document_ai/           # Progetto Django
│   ├── settings.py        # Configurazioni
│   └── urls.py           # URL routing
├── documents/             # App principale
│   ├── models.py         # Modelli database
│   ├── views.py          # Views e API
│   ├── utils.py          # Logica business
│   ├── forms.py          # Forms validazione
│   └── serializers.py    # API serializers
├── templates/             # Templates HTML
├── media/                # File caricati
├── requirements.txt      # Dipendenze Python
├── Dockerfile           # Container config
└── docker-compose.yml   # Orchestrazione
```

## 🔐 Configurazione OpenAI

Per abilitare le funzionalità AI:

1. Ottieni API key da OpenAI
2. Aggiungi al file `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key
   ```
3. Riavvia l'applicazione

Senza API key, l'app funziona comunque per upload e gestione documenti.

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚢 Deployment

### Docker Production
```bash
# Build produzione
docker-compose -f docker-compose.prod.yml up --build -d
```

### Heroku
```bash
heroku create document-ai-assistant
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

### AWS/GCP
L'app è containerizzata e pronta per deployment su qualsiasi cloud provider.

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Upload Documento
![Upload](screenshots/upload.png)

### Analisi AI
![Analysis](screenshots/analysis.png)

## 🔧 Personalizzazione

### Aggiungere Nuovi Formati Documento
```python
# In utils.py
def extract_text_from_newformat(file_path):
    # Logica estrazione
    return extracted_text

# In models.py DOCUMENT_TYPES
('newformat', 'New Format'),
```

### Configurare Database Produzione
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## 🤝 Contribuzioni

1. Fork il repository
2. Crea feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Apri Pull Request

## 📝 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 👨‍💻 Autore

**Marco Rossi** - Sviluppatore Python/Django
- GitHub: [@marcorossi](https://github.com/marcorossi)
- LinkedIn: [Marco Rossi](https://linkedin.com/in/marcorossi)
- Email: marco@example.com

## 🙏 Ringraziamenti

- OpenAI per le API di intelligenza artificiale
- Django community per il framework
- Bootstrap per l'UI framework
- Docker per la containerizzazione

## 📞 Supporto

Per domande, bug reports o richieste di funzionalità:

1. Apri un issue su GitHub
2. Consulta la documentazione API
3. Contatta il maintainer

## 🔄 Changelog

### v1.0.0 (2025-09-19)
- ✅ Upload documenti multi-formato
- ✅ Estrazione testo automatica
- ✅ Integrazione OpenAI per riassunti e Q&A
- ✅ API REST complete
- ✅ Containerizzazione Docker
- ✅ Admin panel per gestione
- ✅ UI responsive con Bootstrap

### Prossime Features
- 🔄 OCR per documenti scansionati
- 🔄 Supporto file Excel/CSV
- 🔄 Chat multi-documento
- 🔄 Export risultati
- 🔄 Autenticazione OAuth
- 🔄 Dashboard analytics