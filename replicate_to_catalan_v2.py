#!/usr/bin/env python3
"""Replicate CTAs to Catalan by matching dates, not filenames."""

import os
import re
from collections import defaultdict

ca_translations = {
    # CTA Titles (comprehensive list from previous script)
    "Domina la Terminología de Ciberseguridad": "Domina la Terminologia de Ciberseguretat",
    "Domina Detección de Amenazas con IA": "Domina la Detecció de Amenaces amb IA",
    "Programa tu Auditoría de Cumplimiento NIS2 (Gratis)": "Programa la teva Auditoria de Compliment NIS2 (Gratis)",
    "Obtén Checklist de Seguridad en Fechas Clave (Gratis)": "Obté Checklist de Seguretat en Dates Clau (Gratis)",
    "Solicita tu Evaluación de Seguridad Gratuita": "Solicita la teva Evaluació de Seguretat Gratuïta",
    "Descarga el Glosario Completo de Ciberseguridad": "Descarrega el Glossari Complet de Ciberseguretat",
    "Obtén Plan de Seguridad para Educación (Gratis)": "Obté Plan de Seguretat per a Educació (Gratis)",
    "Obtén Estrategia contra Amenazas de IA (Gratis)": "Obté Estrategia contra Amenaces de IA (Gratis)",
    "Solicita Evaluación de Ciberresiliencia (Gratis)": "Solicita Evaluació de Ciberresiliència (Gratis)",
    "Obtén Plan de Seguridad para Pymes (Gratis)": "Obté Plan de Seguretat per a Pimes (Gratis)",
    "Identifica tus Vectores de Ataque (Gratis)": "Identifica els teus Vectors d'Atac (Gratis)",
    "Descarga Plan de Respuesta a Ransomware (Gratis)": "Descarrega Plan de Resposta a Ransomware (Gratis)",
    "Obtén Evaluación de Seguridad Móvil (Gratis)": "Obté Evaluació de Seguretat Mòbil (Gratis)",
    "Obtén Resumen de Seguridad en Fechas Clave (Gratis)": "Obté Resum de Seguretat en Dates Clau (Gratis)",
    "Obtén Auditoría de Seguridad de Fin de Año (Gratis)": "Obté Auditoria de Seguretat de Final d'Any (Gratis)",
    "Descarga Pronóstico de Amenazas 2026 (Gratis)": "Descarrega Pronòstic d'Amenaces 2026 (Gratis)",
    "Obtén Evaluación de Seguridad en Nube (Gratis)": "Obté Evaluació de Seguretat en Núvol (Gratis)",

    "Optimiza tu Gestión de TI Hoy": "Optimitza la teva Gestió de TI Avui",
    "Elige la Solución Correcta para tu Negocio": "Tria la Solució Correcta per al teu Negoci",
    "Gestiona Dispositivos Móviles de Forma Segura": "Gestiona Dispositius Mòbils de Forma Segura",
    "Compara Plataformas de Gestión Remota": "Compara Plataformes de Gestió Remota",
    "Automatiza la Gestión de Parches": "Automatitza la Gestió de Pegats",
    "Fortalece tu Infraestructura de TI": "Enforteix la teva Infraestructura de TI",
    "Ahorra Energía y Reduce Costos": "Estalvia Energia i Redueix Costos",
    "Automatiza Mantenimiento con IA": "Automatitza Manteniment amb IA",
    "Protege tu Negocio en Fechas Clave": "Protegeix el teu Negoci en Dates Clau",
    "Entiende las Tendencias de Ciberataques": "Comprèn les Tendències de Ciberatacs",
    "Gestiona TI desde la Nube": "Gestiona TI des del Núvol",
    "Soluciones de TI para Educación": "Solucions de TI per a Educació",
    "Asegura tu Cumplimiento de Licencias": "Assegura el teu Compliment de Llicencies",
    "Protege tu Escuela del Ransomware": "Protegeix la teva Escola del Ransomware",
    "Gestiona Aulas Digitales Seguras": "Gestiona Aules Digitals Segures",
    "Responde Rápido a una Brecha de Datos": "Respon Ràpid a una Violació de Dades",
    "Anticipa Amenazas de IA": "Anticipa Amenaces de IA",
    "Construye Ciberresiliencia Nacional": "Construeix Ciberresiliència Nacional",
    "Asegura Dispositivos en Teletrabajo de Verano": "Assegura Dispositius en Teletreball d'Estiu",
    "Bloquea Vectores de Ataque Comunes": "Bloqueja Vectors d'Atac Comuns",
    "Protege Smartphones Corporativos": "Protegeix Smartphones Corporatius",
    "Evita Estafas de CEO/Suplantación": "Evita Estafes de CEO/Suplantació",
    "Cierra el Año con Seguridad": "Tanca l'Any amb Seguretat",
    "Aprende del Año en Ciberseguridad": "Aprèn de l'Any en Ciberseguretat",
    "Protege tu Negocio como Autónomo": "Protegeix el teu Negoci com Autònom",
    "Compra Online de Forma Segura": "Compra En Línia de Forma Segura",
    "Calcula el ROI de tu Seguridad": "Calcula el ROI de la teva Seguretat",
    "Evalúa Riesgos de IA en tu Negocio": "Avalua Riscos de IA en el teu Negoci",
    "Protege Derechos de Usuarios": "Protegeix Drets d'Usuaris",
    "Identifica y Bloquea Técnicas de Fraude": "Identifica i Bloqueja Tècniques de Frau",
    "Justifica Inversión en Ciberseguridad": "Justifica Inversió en Ciberseguretat",

    "Automatiza Soporte de TI y Reduce Costos": "Automatitza Suport de TI i Redueix Costos",
    "Prevén Problemas Antes de que Ocurran": "Prevé Problemes Abans que Ocorrin",
    "Transforma la TI de tu Universidad": "Transforma la TI de la teva Universitat",
    "Cumple NIS2 sin Complicaciones": "Compleix NIS2 sense Complicacions",
    "Detecta y Elimina Malware de Red": "Detecta i Elimina Malware de Xarxa",
    "Evita los 5 Errores Más Costosos": "Evita els 5 Errors Més Costosos",
    "Asegura tu Red IoT Completamente": "Assegura la teva Xarxa IoT Completament",
    "Protege tus Operaciones en Temporada Alta": "Protegeix les teves Operacions en Temporada Alta",

    # Descriptions
    "Comprende amenazas + protégete efectivamente": "Comprèn amenaces + protegeix-te efectivament",
    "Adelántate a técnicas de evasión en evolución": "Anticipa-t a tècniques d'evasió en evolució",
    "Identifica brechas regulatorias y de protección en 20 minutos": "Identifica bretxes regulatòries i de protecció en 20 minuts",
    "Orientación experta para protección de fin de año": "Orientació experta per a protecció de final d'any",
    "Consulta de 20 minutos sin compromiso": "Consulta de 20 minuts sense compromís",
    "Guía gratuita con 50+ términos esenciales": "Guia gratuïta amb 50+ termes essencials",
    "Protección contra ransomware adaptada para escuelas": "Protecció contra ransomware adaptada per a escoles",
    "Aprende a defenderte contra ataques de nueva generación": "Aprèn a defensar-te contra atacs de nova generació",
    "Análisis experto + plan de protección accionable": "Anàlisi expert + plan de protecció accionable",
    "Estrategia de protección personalizada + guía de implementación": "Estrategia de protecció personalitzada + guia d'implementació",
    "Evaluación de seguridad + plan de mitigación": "Evaluació de seguretat + plan de mitigació",
    "Guía paso a paso + consulta experta": "Guia pas a pas + consulta experta",
    "Revisión experta de tu seguridad de endpoints": "Revisió experta de la teva seguretat d'endpoints",
    "Tendencias de amenazas + checklist de protección": "Tendències d'amenaces + checklist de protecció",
    "Evaluación experta + plan de remediación": "Evaluació experta + plan de remediació",
    "Predicciones expertas + estrategia defensiva": "Prediccions expertes + estrategia defensiva",
    "Revisión de configuración + análisis de vulnerabilidades": "Revisió de configuració + anàlisi de vulnerabilitats",

    "Elimina dependencia de personal manual + mejora eficiencia operativa": "Elimina dependència de personal manual + millora eficiència operativa",
    "Mantenimiento proactivo + monitoreo continuo + respuesta automática": "Manteniment proactiu + monitoreo continu + resposta automàtica",
    "Gestión centralizada + seguridad + aprendizaje sin interrupciones": "Gestió centralitzada + seguretat + aprenentatge sense interrupcions",
    "Auditoría + plan de cumplimiento + certificación experta": "Auditoria + plan de compliment + certificació experta",
    "Análisis en tiempo real + respuesta automática + prevención continua": "Anàlisi en temps real + resposta automàtica + prevenció contínua",
    "Análisis + checklist + plan de corrección inmediata": "Anàlisi + checklist + plan de correcció immediata",
    "Auditoría + segmentación + cifrado + monitoreo 24/7": "Auditoria + segmentació + xifrat + monitoreo 24/7",

    "Evaluación personalizada + plan de acción": "Avaluació personalitzada + plan d'acció",
    "Contacta con Nosotros (Gratis)": "Contacta amb Nosaltres (Gratis)",
}

es_dir = "content/es"
ca_dir = "content/ca"

# Group files by date
es_by_date = {}
ca_by_date = {}

for f in os.listdir(es_dir):
    if f.endswith('.md'):
        date = f[:8]  # YYYYMMDD
        es_by_date[date] = f

for f in os.listdir(ca_dir):
    if f.endswith('.md'):
        date = f[:8]
        ca_by_date[date] = f

# Match and process
updated = 0
for date, es_filename in sorted(es_by_date.items()):
    if date not in ca_by_date:
        continue

    ca_filename = ca_by_date[date]
    es_path = os.path.join(es_dir, es_filename)
    ca_path = os.path.join(ca_dir, ca_filename)

    with open(es_path, 'r', encoding='utf-8') as f:
        es_content = f.read()

    with open(ca_path, 'r', encoding='utf-8') as f:
        ca_content = f.read()

    # Extract Spanish CTA (find last blockquote with emoji)
    es_cta_match = re.search(r'(>\s*[🔐🛡️🏢📋⏰📊🖥️⚙️📱⚖️🔄🔒♻️🤖🎄📈☁️🎓📜🏫👥🚨🧠☀️🎯📲✅🛍️💰⚠️👁️💡🎁👨‍💼🔧🦠🔌].*?)$', es_content, re.MULTILINE | re.DOTALL)

    if not es_cta_match:
        print(f"⚠️  {es_filename} — No CTA found")
        continue

    es_cta = es_cta_match.group(1).strip()

    # Translate to Catalan
    ca_cta = es_cta
    for es_text, ca_text in ca_translations.items():
        ca_cta = ca_cta.replace(es_text, ca_text)

    # Remove old CTA from Catalan and add new
    ca_content_new = re.sub(
        r'(>\s*[🔐🛡️🏢📋⏰📊🖥️⚙️📱⚖️🔄🔒♻️🤖🎄📈☁️🎓📜🏫👥🚨🧠☀️🎯📲✅🛍️💰⚠️👁️💡🎁👨‍💼🔧🦠🔌].*?)$',
        '',
        ca_content,
        count=1,
        flags=re.MULTILINE | re.DOTALL
    )

    ca_content_new = ca_content_new.rstrip() + '\n\n' + ca_cta + '\n'

    with open(ca_path, 'w', encoding='utf-8') as f:
        f.write(ca_content_new)

    print(f"✅ {date} — {es_filename} → {ca_filename}")
    updated += 1

print(f"\n✓ Updated {updated} Catalan posts with translated CTAs")
