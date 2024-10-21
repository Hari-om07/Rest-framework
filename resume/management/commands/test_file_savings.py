from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ResumeProcessor.settings')
django.setup()

# Test file saving
file = SimpleUploadedFile("test_resume.pdf", b"file_content")
file_path = os.path.join(settings.MEDIA_ROOT, file.name)
with open(file_path, 'wb') as f:
    f.write(file.read())

# Check if file is saved
if os.path.isfile(file_path):
    print('File saved successfully')
else:
    print('Failed to save file')

# Clean up
os.remove(file_path)

