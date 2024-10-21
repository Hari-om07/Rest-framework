from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import os
import logging
import re
from django.conf import settings
from .models import Candidate
from .serializers import CandidateSerializer
import spacy
import pdfplumber
from django.shortcuts import render
from docx import Document

logger = logging.getLogger(__name__)

def homepage(request):
    return render(request, 'homepage.html')

class ResumeExtractView(APIView):
    def post(self, request):
        file = request.FILES.get('resume')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure MEDIA_ROOT directory exists
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        
        try:
            # Save the file temporarily
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            
            # Load spaCy model
            nlp = spacy.load('en_core_web_sm')
            
            # Process the resume based on file type
            text = ''
            first_name = ''
            if file.name.lower().endswith('.pdf'):
                # Handle PDF files
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        # Extract text, font size, and other text properties
                        for char in page.chars:
                            if char['size'] > 14:
                                first_name += char['text']
                        text += page.extract_text()
            elif file.name.lower().endswith('.docx'):
                # Handle DOCX files
                doc = Document(file_path)
                for para in doc.paragraphs:
                    for run in para.runs:
                        if run.font.size and run.font.size.pt > 14:
                            first_name += run.text
                    text += para.text
            else:
                # Unsupported file type
                return Response({'error': 'Unsupported file type. Please upload a PDF or DOCX file.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Apply spaCy NLP processing
            doc = nlp(text)
            
            # Extract other details like email and mobile number
            email = ''
            mobile_number = ''
            
            # Regex patterns
            email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@gmail\.com')
            phone_pattern = re.compile(r'\b\d{10}\b')
            
            # Extract email and phone number using regex
            email_matches = email_pattern.findall(text)
            if email_matches:
                email = email_matches[0]
            
            phone_matches = phone_pattern.findall(text)
            if phone_matches:
                mobile_number = phone_matches[0]
            
            # Create a Candidate object
            candidate = Candidate.objects.create(
                first_name=first_name.strip()[:100],
                email=email,
                mobile_number=mobile_number
            )
            
            # Serialize the Candidate object
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Internal server error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
