from django.shortcuts import render
from django.contrib import messages
from bs4 import BeautifulSoup
import requests
import re
from decouple import config
import segno
import uuid

from report.views import convert_to_pdf


def generate_qr(id):
    qrcode = segno.make(f'http://192.168.0.100:8080/?id_expe={id}')
    qrcode.save(f'expediente_{id}_{uuid.uuid1()}.png')


def get_expediente_id(request):

    numero_juicio_a = request.POST.get('num_juicio1')
    numero_juicio_b = request.POST.get('num_juicio2')

    if numero_juicio_a and numero_juicio_b:
        response = requests.get(
                config('URL_BUSCAR_EXPEDIENTE'), 
                data = { 'FIELD_BUS_JUICIO': numero_juicio_a, 'FIELD_BUS_JUICIO1': numero_juicio_b },
                cookies = { 
                    'TCONTROL': config("TCONTROL"), 
                    'PASW': config("PASW"), 
                    'NOMBRE_USER': config("NOMBRE_USER"), 
                    'USER': config("USER"), 
                    'NOM_REPO': config("NOM_REPO"), 
                    'BUS_MUNI': 'Todos', 
                    'FIELD_BUS_POB': '', 
                    'BUS_ORIGEN': 'Todos', 
                    'BUS_SENTE': 'Todos', 
                    'BUS_EDO_PROC': 'Todos', 
                    'FIELD_BUS_DEMANDADO': '', 
                    'FIELD_BUS_ACTOR': '', 
                    'LLAVE_INI': '', 
                    'FIELD_BUS_JUICIO': numero_juicio_a,
                    'FIELD_BUS_JUICIO1': numero_juicio_b
                    }, 
                verify = False
                )
        
        if response.status_code == 200:
            
            soup_session1 = BeautifulSoup(response.text, 'html.parser')

            tablas = soup_session1.find('form').find_all('table')

            link_expediente = tablas[4].find('a', class_= 'link', href=re.compile('id_expe='))

            if link_expediente:
                id_expediente = re.findall('id_expe=(.*)', link_expediente['href'])[0]
                return id_expediente
            else:
                messages.add_message(request, messages.INFO, f'No se encontró el expediente "{numero_juicio_a} / {numero_juicio_b}"')    
    
    return None


def get_expediente_detail(request):

    expediente_id = get_expediente_id(request)

    if expediente_id:

        url = f'{config("URL_DETALLE_EXPEDIENTE")}id_expe={expediente_id}'

        response = requests.get(url, cookies={'TCONTROL': config("TCONTROL"), 'PASW': config("PASW"),
                                'NOMBRE_USER': config("NOMBRE_USER"), 'USER': config("USER")}, verify=False)
            
        if response.status_code == 200:
            soup_session2 = BeautifulSoup(response.text, 'html.parser')

            # Tablas
            tablas = soup_session2.find('form').find_all('table')

            # Table - Entrada de Expediente
            tabla_entrada_expediente = tablas[1].tbody.tr.table
            # Rows - Entrada de Expediente
            rows = tabla_entrada_expediente.tbody.find_all('tr')
            # Valores - Entrada De Expediente
            num_juicio = rows[0].find_all('td')[1].get_text(strip=True)
            fecha_entrada = rows[0].find_all('td')[3].input['value']
            estado = rows[1].find_all('td')[1].get_text(strip=True)
            rezago_agrario = rows[1].find_all('td')[3].find(attrs={"selected": True}).get_text()
            municipio = rows[2].find_all('td')[1].get_text(strip=True)
            origen_expediente = rows[2].find_all('td')[3].find(attrs={"selected": True}).get_text()
            poblado = rows[3].find_all('td')[1].input['value']
            tipo_juicio = rows[3].find_all('td')[3].find(attrs={"selected": True}).get_text()

            # Table - Datos de Admision
            tabla_datos_admision = tablas[4].tbody.tr.td.table
            # Rows - Datos de Admision
            rows = tabla_datos_admision.find_all('tr')
            # Valores - Datos de Admision
            tramite_realizado = rows[0].find_all('td')[1].find(attrs={"selected": True}).get_text()
            fecha_tramite = rows[0].find_all('td')[3].input['value']
            accion_ejercida = rows[1].find_all('td')[1].get_text(strip=True)
            fundamento_legal = rows[1].find_all('td')[3].get_text(strip=True)

            # Table - Promovente / Actor
            tabla_promovente_actor = tablas[7].tbody.tr.td.table
            # Rows - Promovente / Actor
            rows = tabla_promovente_actor.find_all('tr')
            # Valores - Promovente / Actor
            nombre_promovente = rows[0].find_all('td')[1].input['value']
            otros_promovente = rows[0].find_all('td')[3].textarea.get_text(strip=True)

            # Table - Datos del Demandado
            tabla_datos_demandado = tablas[10].tbody.tr.td.table
            # Rows - Datos del Demandado
            rows = tabla_datos_demandado.find_all('tr')
            # Valores - Datos del Demandado
            nombre_demandado = rows[0].find_all('td')[1].input['value']
            otros_demandado = rows[0].find_all('td')[3].textarea.get_text(strip=True)

            # Table - Resoluciones
            tabla_resoluciones = tablas[30].tbody.tr.td.table
            # Rows - Resoluciones
            rows = tabla_resoluciones.find_all('tr')
            # TD's - Resoluciones
            tds_resoluciones = tabla_resoluciones.find_all('td')
            # Valores - Resoluciones
            fecha_sentencia = rows[0].find_all('td')[1].input['value']
            fecha_ejecucion = rows[0].find_all('td')[3].input['value']
            tipo_sentencia = rows[1].find_all('td')[1].find(attrs={"selected": True}).get_text()
            observaciones_resoluciones = rows[1].find_all('td')[3].textarea.get_text(strip=True)
            magistrado_resolucion = tds_resoluciones[9].span.find(attrs={"selected": True}).get_text()

            # Table - Otros Datos
            tabla_otros_datos = soup_session2.find('td', string=re.compile('Estado Procesal')).parent.parent
            # Rows - Otros Datos
            rows = tabla_otros_datos.find_all('tr')
            # Valores - Otros Datos
            estado_procesal = rows[0].find_all('td')[1].span.find(attrs={"selected": True}).get_text()
            observaciones_otros_datos = rows[0].find_all('td')[3].textarea.get_text(strip=True)
            fecha_conclusion = rows[1].find_all('td')[1].input['value']

            generate_qr(expediente_id)

            return { 
                'context_detail': {
                    'num_juicio': num_juicio,
                    'fecha_entrada': fecha_entrada,
                    'estado': estado,
                    'rezago_agrario': rezago_agrario,
                    'municipio': municipio,
                    'origen_expediente': origen_expediente,
                    'poblado': poblado,
                    'tipo_juicio': tipo_juicio,
                    'tramite_realizado': tramite_realizado,
                    'fecha_tramite': fecha_tramite,
                    'accion_ejercida': accion_ejercida,
                    'fundamento_legal': fundamento_legal,
                    'nombre_promovente': nombre_promovente,
                    'otros_promovente': otros_promovente,
                    'nombre_demandado': nombre_demandado,
                    'otros_demandado': otros_demandado,
                    'fecha_sentencia': fecha_sentencia,
                    'fecha_ejecucion': fecha_ejecucion,
                    'tipo_sentencia': tipo_sentencia,
                    'observaciones_resoluciones': observaciones_resoluciones,
                    'magistrado_resolucion': magistrado_resolucion,
                    'estado_procesal': estado_procesal,
                    'observaciones_otros_datos': observaciones_otros_datos,
                    'fecha_conclusion': fecha_conclusion
                },
                'context_caratula': {
                    'num_juicio': num_juicio,
                    'tomo': '',
                    'fecha': '',
                    'promovente': '',
                    'demandado': '',
                    'poblado': '',
                    'municipio': '',
                    'estado': '',
                    'asunto': '',
                    'juicio_de_amparo': '',
                    'recurso_de_revision': '',
                }
                
            }

    return None      


def expediente_detail(request):
    if request.method == 'POST':

        context = get_expediente_detail(request)

        convert_to_pdf(context['context_detail'])

        return render(request, 'webpage/expediente_detail.html', context['context_detail'])
            
    return render(request, 'webpage/expediente_detail.html')


