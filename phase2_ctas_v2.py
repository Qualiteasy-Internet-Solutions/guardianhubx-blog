#!/usr/bin/env python3
"""
Phase 2 CTA Optimization v2 - Handle various CTA formats.
"""

import os
import re

phase2_ctas = {
    "20241202-que-hacer-si-info-empresa-comprometida.md": {
        "emoji": "🚨",
        "title": "Responde Rápido a una Brecha de Datos",
        "description": "Protocolo paso a paso + contactos + recuperación inmediata"
    },
    "20250728-verano-proteccion-dispositivos-prey.md": {
        "emoji": "☀️",
        "title": "Asegura Dispositivos en Teletrabajo de Verano",
        "description": "Protección remota + localización + recuperación de datos"
    },
    "20251221-ciberestafas-ceo-autonomos-pymes.md": {
        "emoji": "🎯",
        "title": "Evita Estafas de CEO/Suplantación",
        "description": "Tácticas de fraude + defensa + protocolo de verificación"
    },
    "20251229-ciberseguridad-2026-fin-checklists.md": {
        "emoji": "✅",
        "title": "Cierra el Año con Seguridad",
        "description": "Checklist final + plan para 2026"
    },
    "20260101-resumen-ciberseguridad-2025.md": {
        "emoji": "📊",
        "title": "Aprende del Año en Ciberseguridad",
        "description": "Resumen 2025 + lecciones + tendencias 2026"
    },
    "20260108-guia-ciberseguridad-autonomo-desde-cero.md": {
        "emoji": "🚀",
        "title": "Protege tu Negocio como Autónomo",
        "description": "Guía paso a paso + soluciones asequibles"
    },
    "20260112-rebajas-online-proteccion-ciberseguridad.md": {
        "emoji": "🛍️",
        "title": "Compra Online de Forma Segura",
        "description": "Consejos + herramientas + protección en rebajas"
    },
    "20260209-coste-economico-ciberataques-impacto-empresas.md": {
        "emoji": "💰",
        "title": "Calcula el ROI de tu Seguridad",
        "description": "Impacto financiero + business case para inversión en ciberseguridad"
    },
    "20260212-ia-anuncios-confianza-reto-ciberseguridad.md": {
        "emoji": "⚠️",
        "title": "Evalúa Riesgos de IA en tu Negocio",
        "description": "Desafíos de confianza + marco de riesgo + mitigación"
    },
    "20260220-derechos-usuario-hackeo-empresa-datos.md": {
        "emoji": "⚖️",
        "title": "Protege Derechos de Usuarios",
        "description": "Compliance + obligaciones post-brecha + plan de comunicación"
    },
    "20260222-captchas-falsos-malware-ingenieria-social.md": {
        "emoji": "👁️",
        "title": "Identifica y Bloquea Técnicas de Fraude",
        "description": "Análisis técnico + defensas comportamentales"
    },
    "20260227-solo-49-por-ciento-empresas-invierte-ciberseguridad.md": {
        "emoji": "💡",
        "title": "Justifica Inversión en Ciberseguridad",
        "description": "Datos del mercado + ROI + plan de presupuesto"
    },
}

base_dir = "content/es"
updated_count = 0

for filename, cta_data in phase2_ctas.items():
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build new CTA
    new_cta = f"""> {cta_data['emoji']} **{cta_data['title']}** — {cta_data['description']}.
>
> **[→ Contacta con Nosotros (Gratis)](https://guardianhubx.com/es/#contact)** — Evaluación personalizada + plan de acción."""

    # Strategy: Find last `>` blockquote section and replace it
    # Find all blockquote matches (starting with >)
    matches = list(re.finditer(r'^>.*$', content, re.MULTILINE))

    if matches:
        last_match = matches[-1]
        # Expand to include multi-line blockquote
        start_idx = last_match.start()
        # Backtrack to find the start of this blockquote group
        for i in range(start_idx - 1, -1, -1):
            if content[i] == '\n' and content[i+1] != '>':
                start_idx = i + 1
                break
            if i == 0:
                start_idx = 0
                break

        end_idx = last_match.end()
        # Extend to include following continuation lines if they exist
        while end_idx < len(content) and content[end_idx] in '\n>':
            if content[end_idx] == '\n':
                if end_idx + 1 < len(content) and content[end_idx + 1] != '>':
                    break
                end_idx += 1
            else:
                end_idx += 1

        old_text = content[start_idx:end_idx]
        content = content[:start_idx] + new_cta + content[end_idx:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} — CTA updated (fallback method)")
        updated_count += 1
    else:
        print(f"❌ {filename} — no blockquote found")

print(f"\n✓ Phase 2 v2: Updated {updated_count} additional posts")
