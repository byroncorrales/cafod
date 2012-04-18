# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from models import *
from forms import *

# Create your views here.

#def contrapartes_index(request):

#    contra = Contraparte.objects.all()

#    return render_to_response('contrapartes/contraparte_index.html', locals(),
#                                 context_instance=RequestContext(request))

@login_required
def crear_contraparte(request):
    form = ContraparteForms(request.POST, request.FILES)
    if request.method == 'POST':
    	if form.is_valid():
	    form_uncommited = form.save(commit=False)
	    form_uncommited.user = request.user
	    form_uncommited.save()
    	    
    	    #obj.save()
    	    return HttpResponseRedirect('/')
    else:
    	form = ContraparteForms()
    return render_to_response('contrapartes/crear_contraparte.html', locals(),
    	                         context_instance=RequestContext(request))

@login_required
def editar_contraparte(request, id):
    contra = get_object_or_404(Contraparte, id=id)
    usuarios = UserProfile.objects.filter(contraparte_id=contra.id)

    user_profile = request.user.get_profile().user.id
    print user_profile

    nombres = []
    for obj in usuarios:
        nombres.append(obj.user.username)

    if not request.user.username in [i for i in nombres]:
        return HttpResponse("Usted no puede editar esta Contraparte")

    if request.method == 'POST':
        form = ContraparteForms(request.POST, instance = contra)
        if form.is_valid():
            form_uncommited = form.save(commit=False)
            form_uncommited.user = request.user
            form_uncommited.save()
            
            return HttpResponseRedirect('/contrapartes')
    else:
        form = ContraparteForms(instance=contra)
    return render_to_response('contrapartes/crear_contraparte.html', locals(),
                                 context_instance=RequestContext(request))

@login_required
def borrar_contraparte(request, id):
    contra = get_object_or_404(Contraparte, pk=id)
    usuarios = UserProfile.objects.filter(Contraparte_id=contra.id)

    nombres = []
    for obj in usuarios:
        nombres.append(obj.user.username)

    if request.user.username in [i for i in nombres] or request.user.is_superuser:
        contra.delete()
        return redirect('contraparte-list')
    else:
        return redirect('/')