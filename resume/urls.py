from django.urls import path
from .views import ResumeExtractView, homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('api/extract_resume/', ResumeExtractView.as_view(), name='extract_resume'),
]