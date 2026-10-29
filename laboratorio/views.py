from django.shortcuts import render, redirect
from .models import PuestoSalud, Usuario, PruebaLaboratorio
from .forms import UsuarioForm, PruebaForm
from django.db.models import Sum

def registrar_equipo(request):
    if request.method == 'POST':
        u_form = UsuarioForm(request.POST)
        p_form = PruebaForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            usuario = u_form.save()
            prueba = p_form.save(commit=False)
            prueba.usuario = usuario
            prueba.save()
            return redirect('lista_equipos')
    else:
        u_form = UsuarioForm()
        p_form = PruebaForm()
    return render(request, 'laboratorio/registrar_equipo.html', {'u_form': u_form, 'p_form': p_form})

def lista_equipos(request):
    puestos = PuestoSalud.objects.all()
    resumen_puestos = []

    for puesto in puestos:
        usuarios_count = puesto.usuarios.count()
        pruebas = PruebaLaboratorio.objects.filter(usuario__puesto=puesto)
        
        total_pruebas_count = pruebas.aggregate(total=Sum('cantidad'))['total'] or 0
        
        conteo_micro = pruebas.filter(tipo_prueba='Microbiologia').aggregate(s=Sum('cantidad'))['s'] or 0
        conteo_bact = pruebas.filter(tipo_prueba='Bacteriologia').aggregate(s=Sum('cantidad'))['s'] or 0
        conteo_quim = pruebas.filter(tipo_prueba='Quimica').aggregate(s=Sum('cantidad'))['s'] or 0

        porc_micro = (conteo_micro / total_pruebas_count * 100) if total_pruebas_count > 0 else 0
        porc_bact = (conteo_bact / total_pruebas_count * 100) if total_pruebas_count > 0 else 0
        porc_quim = (conteo_quim / total_pruebas_count * 100) if total_pruebas_count > 0 else 0

        resumen_puestos.append({
            'puesto': puesto,
            'usuarios_count': usuarios_count,
            'conteo_micro': conteo_micro,
            'conteo_bact': conteo_bact,
            'conteo_quim': conteo_quim,
            'porc_micro': round(porc_micro, 2),
            'porc_bact': round(porc_bact, 2),
            'porc_quim': round(porc_quim, 2),
            'total_pruebas': total_pruebas_count,
        })

    return render(request, 'laboratorio/lista_equipos.html', {'resumen_puestos': resumen_puestos})