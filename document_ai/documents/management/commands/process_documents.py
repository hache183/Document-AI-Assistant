from django.core.management.base import BaseCommand
from documents.models import Document
from documents.utils import extract_text_from_file, generate_summary

class Command(BaseCommand):
    help = 'Processes documents that need text extraction and summary generation'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reprocess',
            action='store_true',
            help='Reprocess all documents, even those already processed',
        )
    
    def handle(self, *args, **options):
        if options['reprocess']:
            documents = Document.objects.all()
            self.stdout.write('Reprocessing all documents...')
        else:
            documents = Document.objects.filter(extracted_text='')
            self.stdout.write('Processing documents without extracted text...')
        
        processed = 0
        for document in documents:
            self.stdout.write(f'Processing: {document.title}')
            
            try:
                # Estrai testo
                file_path = document.file.path
                extracted_text = extract_text_from_file(file_path, document.document_type)
                document.extracted_text = extracted_text
                
                # Genera riassunto
                if extracted_text and len(extracted_text) > 100:
                    summary = generate_summary(extracted_text)
                    document.summary = summary
                
                document.save()
                processed += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully processed: {document.title}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {document.title}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Processed {processed} documents')
        )