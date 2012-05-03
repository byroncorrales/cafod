# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from models import *
from forms import *
from notas.models import *
from django.contrib.sites.models import Site
from django.core.mail import send_mail
import operator
import thread
import datetime
from django.template.loader import render_to_string

# Create your views here.
#def contrapartes_index(request):
#    contra = Contraparte.objects.all()
#    return render_to_response('contrapartes/contraparte_index.html', locals(),
#                                 context_instance=RequestContext(request))


def detalle_contraparte(request,id):
    contra = get_object_or_404(Contraparte, id=id)
    notas = Notas.objects.filter(user__userprofile__contraparte__id=id).order_by('-fecha')
    return render_to_response('contrapartes/contraparte_detail.html', locals(),
                                 context_instance=RequestContext(request))

@login_required
def crear_contraparte(request):
    form = ContraparteForms(request.POST, request.FILES)
    if request.method == 'POST':
    	if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.save()
            return HttpResponseRedirect('/')
    else:
    	form = ContraparteForms()
    return render_to_response('contrapartes/crear_contraparte.html', locals(),
    	                         context_instance=RequestContext(request))

@login_required
def editar_contraparte(request, id):
    contra = get_object_or_404(Contraparte, id=id)
    user_ids = UserProfile.objects.filter(contraparte__id=contra.id).values_list('user__id', flat=True)

    if not request.user.id in user_ids:
        if not request.user.is_superuser:
            return HttpResponse("Usted no puede editar esta Contraparte")

    if request.method == 'POST':
        form = ContraparteForms(data=request.POST, 
                                instance=contra, 
                                files=request.FILES)
        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.save()
            return HttpResponseRedirect('%s?shva=ok' % contra.get_absolute_url())
    else:
        form = ContraparteForms(instance=contra)
    return render_to_response('contrapartes/crear_contraparte.html', locals(),
                                 context_instance=RequestContext(request))

# @login_required
# def borrar_contraparte(request, id):
#     contra = get_object_or_404(Contraparte, pk=id)
#     usuarios = UserProfile.objects.filter(contraparte_id=contra.id)

#     nombres = []
#     for obj in usuarios:
#         nombres.append(obj.user.username)

#     if request.user.username in [i for i in nombres] or request.user.is_superuser:
#         contra.delete()
#         return redirect('contraparte-list')
#     else:
#         return redirect('/')

@login_required
def editar_usuario_perfil(request):
    #usuario = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=request.user)
        form1 = UserProfileForm(data=request.POST, instance=request.user.userprofile, files=request.FILES)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            #form_uncommited = form.save(commit=False)
            #form_uncommited.user = request.user
            #form_uncommited.save()

            return HttpResponseRedirect('/foros/perfil')
    else:
        form = UserForm(instance=request.user)
        form1 = UserProfileForm(instance=request.user.userprofile)
    return render_to_response('contrapartes/editar_usuario.html', locals(),
                                 context_instance=RequestContext(request))

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        form = MensajeForm(data=request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/contrapartes/mensajes/')

    else:
        form = MensajeForm()
    return render_to_response('contrapartes/mensajes.html', locals(),
                                context_instance=RequestContext(request))

def notify_all_mensaje(mensaje):
    pass