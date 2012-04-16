# -*- coding: UTF-8 -*-

from django.db import models
#from django.forms import ModelForm
from tagging.forms import TagField
from tagging_autocomplete.widgets import TagAutocomplete
from models import *
from django import forms

class ForosForm(forms.ModelForm):
    class Meta:
    	model = Foros
    	exclude = ('contraparte','creacion',)

class AporteForm(forms.ModelForm):
    class Meta:
    	model = Aportes
    	exclude = ('foro','fecha','user',)

class ComentarioForm(forms.ModelForm):
    class Meta:
    	model = Comentarios
    	exclude = ('fecha','aporte','usuario')

class ImagenForm(forms.ModelForm):
    tags = TagField(widget=TagAutocomplete())

    class Meta:
    	model = Imagen
    	exclude = ('content_type', 'object_id', 'content_object',)

class DocumentoForm(forms.ModelForm):
    tags = TagField(widget=TagAutocomplete())

    class Meta:
    	model = Documentos
    	exclude = ('content_type', 'object_id', 'content_object',)

class VideoForm(forms.ModelForm):
    tags = TagField(widget=TagAutocomplete())

    class Meta:
    	model = Videos
    	exclude = ('content_type', 'object_id', 'content_object',)

class AudioForm(forms.ModelForm):
    tags = TagField(widget=TagAutocomplete())

    class Meta:
    	model = Audios
    	exclude = ('content_type', 'object_id', 'content_object',)
