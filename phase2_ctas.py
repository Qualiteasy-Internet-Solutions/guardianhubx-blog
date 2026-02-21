#!/usr/bin/env python3
"""
Phase 2 CTA Optimization for 28 medium-value posts.
Categories: General security tips, best practices, product features, case studies.
"""

import os
import re

# Phase 2 posts: Categorized by topic for appropriate CTA type
phase2_ctas = {
    # Product/Platform Features → IT Management CTA
    "20230908-plataforma-gestion-para-cios-ctos.md": {
        "type": "product",
        "emoji": "🖥️",
        "title": "Optimiza tu Gestión de TI Hoy",
        "description": "Descubre cómo automatizar tu infraestructura y reducir costos operativos"
    },
    "20230909-principales-diferencias-RDM-RMM.md": {
        "type": "product",
        "emoji": "⚙️",
        "title": "Elige la Solución Correcta para tu Negocio",
        "description": "Comparativa experta RDM vs RMM + recomendaciones personalizadas"
    },
    "20230918-optimizando-la-gestion-de-dispositivos-con-software-uem.md": {
        "type": "product",
        "emoji": "📱",
        "title": "Gestiona Dispositivos Móviles de Forma Segura",
        "description": "Implementa UEM y reduce riesgos de seguridad en tu empresa"
    },
    "20230927-comparativa-faronics-cloud-intune-ninjaone.md": {
        "type": "comparison",
        "emoji": "⚖️",
        "title": "Compara Plataformas de Gestión Remota",
        "description": "Análisis detallado + matriz de decisión para tu contexto"
    },
    "20231004-mantengase-a-la-vanguardia-con-el-software-de-gestion-remota-de-parches-simplifique-sus-actualizaciones.md": {
        "type": "product",
        "emoji": "🔄",
        "title": "Automatiza la Gestión de Parches",
        "description": "Ahorra tiempo + mejora seguridad con actualizaciones automáticas"
    },
    "20231101-como-mejorar-la-seguridad-de-it.md": {
        "type": "best_practice",
        "emoji": "🔒",
        "title": "Fortalece tu Infraestructura de TI",
        "description": "10 mejores prácticas + plan de implementación para tu empresa"
    },
    "20231202-Sostenibilidad-Tecnología-PowerSave.md": {
        "type": "product",
        "emoji": "♻️",
        "title": "Ahorra Energía y Reduce Costos",
        "description": "Soluciones sostenibles + impacto financiero inmediato"
    },
    "20231202-como-chatgpt-te-puede-ayudar-en-el-mantenimiento-y-actualizaciones-de-tus-equipos.md": {
        "type": "trend",
        "emoji": "🤖",
        "title": "Automatiza Mantenimiento con IA",
        "description": "Implementa ChatGPT + herramientas de TI para máxima eficiencia"
    },
    "20231206-esta-su-empresa-protegida-de-los-ciberataques-estas-navidades.md": {
        "type": "seasonal",
        "emoji": "🎄",
        "title": "Protege tu Negocio en Fechas Clave",
        "description": "Checklist de seguridad para campañas y períodos de alto riesgo"
    },
    "20240701-los-datos-de-ciberataques-en-empresas.md": {
        "type": "insight",
        "emoji": "📈",
        "title": "Entiende las Tendencias de Ciberataques",
        "description": "Datos + análisis + estrategia defensiva para tu sector"
    },
    "20240710-ventajas-de-utilizar-una-consola-en-la-nube-para-la-gestion-centralizada-de-ti.md": {
        "type": "product",
        "emoji": "☁️",
        "title": "Gestiona TI desde la Nube",
        "description": "Beneficios probados + migración paso a paso"
    },
    "20240723-gestion-ti-universidades.md": {
        "type": "vertical",
        "emoji": "🎓",
        "title": "Soluciones de TI para Educación",
        "description": "Casos de uso + mejores prácticas para instituciones académicas"
    },
    "20240823-la-importancia-de-tener-las-licencias-de-software-actualizadas.md": {
        "type": "best_practice",
        "emoji": "📜",
        "title": "Asegura tu Cumplimiento de Licencias",
        "description": "Auditoría gratuita + plan de actualización y ahorro"
    },
    "20241010-como-evitar-el-ransomware-en-las-escuelas.md": {
        "type": "vertical",
        "emoji": "🏫",
        "title": "Protege tu Escuela del Ransomware",
        "description": "Guía específica para centros educativos + protocolo de respuesta"
    },
    "20241113-faronics-insight-herramienta-gestion-aula.md": {
        "type": "product",
        "emoji": "👥",
        "title": "Gestiona Aulas Digitales Seguras",
        "description": "Control total + protección para entornos educativos"
    },
    "20241202-que-hacer-si-info-empresa-comprometida.md": {
        "type": "crisis",
        "emoji": "🚨",
        "title": "Responde Rápido a una Brecha de Datos",
        "description": "Protocolo paso a paso + contactos + recuperación inmediata"
    },
    "20250127-como-la-ia-esta-revolucionando-las-tecnicas-de-evasion-en-ciberseguridad.md": {
        "type": "insight",
        "emoji": "🧠",
        "title": "Anticipa Amenazas de IA",
        "description": "Análisis de técnicas emergentes + defensas probadas"
    },
    "20250324-la-creciente-amenaza-de-los-ciberataques-en-espana-claves-para-una-ciberresiliencia-efectiva.md": {
        "type": "insight",
        "emoji": "🛡️",
        "title": "Construye Ciberresiliencia Nacional",
        "description": "Contexto español + estrategia adaptada a regulaciones locales"
    },
    "20250728-verano-proteccion-dispositivos-prey.md": {
        "type": "product",
        "emoji": "☀️",
        "title": "Asegura Dispositivos en Teletrabajo de Verano",
        "description": "Protección remota + localización + recuperación de datos"
    },
    "20250824-vector-ataque-proteccion-empresa.md": {
        "type": "best_practice",
        "emoji": "🎯",
        "title": "Bloquea Vectores de Ataque Comunes",
        "description": "Análisis por tipo + contramedidas inmediatas"
    },
    "20251021-mdm-seguridad-movil-corporativa-protege-smartphone-negocio.md": {
        "type": "product",
        "emoji": "📲",
        "title": "Protege Smartphones Corporativos",
        "description": "Implementa MDM + reduce riesgos de dispositivos móviles"
    },
    "20251221-ciberestafas-ceo-autonomos-pymes.md": {
        "type": "threat",
        "emoji": "🎯",
        "title": "Evita Estafas de CEO/Suplantación",
        "description": "Tácticas de fraude + defensa + protocolo de verificación"
    },
    "20251229-ciberseguridad-2026-fin-checklists.md": {
        "type": "best_practice",
        "emoji": "✅",
        "title": "Cierra el Año con Seguridad",
        "description": "Checklist final + plan para 2026"
    },
    "20260101-resumen-ciberseguridad-2025.md": {
        "type": "insight",
        "emoji": "📊",
        "title": "Aprende del Año en Ciberseguridad",
        "description": "Resumen 2025 + lecciones + tendencias 2026"
    },
    "20260108-guia-ciberseguridad-autonomo-desde-cero.md": {
        "type": "guide",
        "emoji": "🚀",
        "title": "Protege tu Negocio como Autónomo",
        "description": "Guía paso a paso + soluciones asequibles"
    },
    "20260112-rebajas-online-proteccion-ciberseguridad.md": {
        "type": "seasonal",
        "emoji": "🛍️",
        "title": "Compra Online de Forma Segura",
        "description": "Consejos + herramientas + protección en rebajas"
    },
    "20260209-coste-economico-ciberataques-impacto-empresas.md": {
        "type": "insight",
        "emoji": "💰",
        "title": "Calcula el ROI de tu Seguridad",
        "description": "Impacto financiero + business case para inversión en ciberseguridad"
    },
    "20260212-ia-anuncios-confianza-reto-ciberseguridad.md": {
        "type": "insight",
        "emoji": "⚠️",
        "title": "Evalúa Riesgos de IA en tu Negocio",
        "description": "Desafíos de confianza + marco de riesgo + mitigación"
    },
    "20260220-derechos-usuario-hackeo-empresa-datos.md": {
        "type": "legal",
        "emoji": "⚖️",
        "title": "Protege Derechos de Usuarios",
        "description": "Compliance + obligaciones post-brecha + plan de comunicación"
    },
    "20260222-captchas-falsos-malware-ingenieria-social.md": {
        "type": "threat",
        "emoji": "👁️",
        "title": "Identifica y Bloquea Técnicas de Fraude",
        "description": "Análisis técnico + defensas comportamentales"
    },
    "20260227-solo-49-por-ciento-empresas-invierte-ciberseguridad.md": {
        "type": "insight",
        "emoji": "💡",
        "title": "Justifica Inversión en Ciberseguridad",
        "description": "Datos del mercado + ROI + plan de presupuesto"
    },
}

base_dir = "content/es"
updated_count = 0
skipped_count = 0

for filename, cta_data in phase2_ctas.items():
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — not found")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has new CTA format (emoji + title pattern)
    if re.search(r'>\s*[🔐🛡️🏢📋⏰📊🖥️⚙️📱⚖️🔄🔒♻️🤖🎄📈☁️🎓📜🏫👥🚨🧠☀️🎯📲✅🛍️💰⚠️👁️💡]', content):
        skipped_count += 1
        continue

    # Find and replace the last contact blockquote
    # Pattern: > **¿Quieres...?** or > **¿...?**
    pattern = r'>\s*\*\*¿.*?\*\*\n*(?:>\s*.*\n)*'

    new_cta = f"""> {cta_data['emoji']} **{cta_data['title']}** — {cta_data['description']}.
>
> **[→ Contacta con Nosotros (Gratis)](https://guardianhubx.com/es/#contact)** — Evaluación personalizada + plan de acción."""

    # Try to replace
    match = re.search(pattern, content)
    if match:
        old_text = match.group(0)
        content = content.replace(old_text, new_cta, 1)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} — CTA updated ({cta_data['type']})")
        updated_count += 1
    else:
        print(f"❌ {filename} — CTA pattern not found")

print(f"\n📊 Phase 2 Summary:")
print(f"   Updated: {updated_count}")
print(f"   Skipped (already new format): {skipped_count}")
print(f"   Failed: {len(phase2_ctas) - updated_count - skipped_count}")
