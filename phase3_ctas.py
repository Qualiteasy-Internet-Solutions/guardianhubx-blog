#!/usr/bin/env python3
"""Phase 3 CTA Optimization for remaining Spanish posts."""

import os
import re

# Phase 3: Remaining posts with optimized CTAs
phase3_ctas = {
    "20230908-la-escasez-de-perfiles-tecnicos-de-soporte-un-desafio-para-cios-ctos-y-directores-de-informatica.md": {
        "emoji": "👨‍💼",
        "title": "Automatiza Soporte de TI y Reduce Costos",
        "description": "Elimina dependencia de personal manual + mejora eficiencia operativa"
    },
    "20230921-problemas-generados-por-la-falta-de-mantenimiento-informatico.md": {
        "emoji": "🔧",
        "title": "Prevén Problemas Antes de que Ocurran",
        "description": "Mantenimiento proactivo + monitoreo continuo + respuesta automática"
    },
    "20240724-gestion-ti-universidades.md": {
        "emoji": "🎓",
        "title": "Transforma la TI de tu Universidad",
        "description": "Gestión centralizada + seguridad + aprendizaje sin interrupciones"
    },
    "20250211-nueva-ley-de-ciberseguridad-lo-que-las-empresas-deben-saber-en-2025.md": {
        "emoji": "⚖️",
        "title": "Cumple NIS2 sin Complicaciones",
        "description": "Auditoría + plan de cumplimiento + certificación experta"
    },
    "20250430-malware-red-dispara-94-analisis-informe-watchguard.md": {
        "emoji": "🦠",
        "title": "Detecta y Elimina Malware de Red",
        "description": "Análisis en tiempo real + respuesta automática + prevención continua"
    },
    "20250908-errores-comunes-ciberseguridad-pymes.md": {
        "emoji": "⚠️",
        "title": "Evita los 5 Errores Más Costosos",
        "description": "Análisis + checklist + plan de corrección inmediata"
    },
    "20251020-seguridad-dispositivos-IoT-PYMES-riesgos-y-como-mitigarlos.md": {
        "emoji": "🔌",
        "title": "Asegura tu Red IoT Completamente",
        "description": "Auditoría + segmentación + cifrado + monitoreo 24/7"
    },
}

base_dir = "content/es"
updated = 0

for filename, cta_data in phase3_ctas.items():
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — not found")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build new CTA format
    new_cta = f"""> {cta_data['emoji']} **{cta_data['title']}** — {cta_data['description']}.
>
> **[→ Contacta con Nosotros (Gratis)](https://guardianhubx.com/es/#contact)** — Evaluación personalizada + plan de acción."""

    # Find and replace the last blockquote section (the old CTA)
    # Strategy: Find all > lines and replace the last group
    matches = list(re.finditer(r'^>.*$', content, re.MULTILINE))

    if matches:
        # Get the last match
        last_idx = len(matches) - 1
        start_pos = matches[last_idx].start()

        # Backtrack to find the start of this blockquote group
        for i in range(start_pos - 1, -1, -1):
            if i < len(content) and content[i] == '\n':
                if i + 1 < len(content) and content[i + 1] != '>':
                    start_pos = i + 1
                    break
            if i == 0:
                start_pos = 0
                break

        # Find end (after all consecutive > lines)
        end_pos = matches[last_idx].end()
        while end_pos < len(content) and content[end_pos] in '\n>':
            if content[end_pos] == '\n':
                if end_pos + 1 < len(content) and content[end_pos + 1] != '>':
                    break
            end_pos += 1

        old_cta = content[start_pos:end_pos]
        content = content[:start_pos] + new_cta + content[end_pos:]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
        updated += 1
    else:
        print(f"❌ {filename} — no CTA found")

print(f"\n✓ Phase 3: Updated {updated} posts with new CTA format")
