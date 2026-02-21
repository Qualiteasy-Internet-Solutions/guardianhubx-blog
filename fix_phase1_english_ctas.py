#!/usr/bin/env python3
"""Fix remaining English CTAs in Phase 1 posts to Spanish."""

import os
import re

# Phase 1 post files
phase1_posts = {
    "20250211-nueva-ley-de-ciberseguridad-lo-que-las-empresas-deben-saber-en-2025.md": {},
    "20240816-como-proteger-red-ataques-ransomware.md": {
        "Protect Your Network from Ransomware Today": "Protege tu Red contra Ransomware Hoy",
        "Get expert guidance + protection strategy": "Obtén orientación experta + estrategia de protección"
    },
    "20240912-guia-rapida-para-entender-los-terminos-clave-en-ataques-de-ciberseguridad.md": {},
    "20250721-ataques-ato-proteger-cuentas.md": {
        "Stop Account Takeover Attacks": "Evita Ataques de Toma de Control de Cuenta",
        "Detect + defend against credential threats": "Detecta + defiéndete contra amenazas de credenciales"
    },
    "20250623-concienciacion-ciberseguridad-empleados.md": {},
    "20250808-ciberseguridad-pymes-riesgos-soluciones.md": {
        "Protect Your SMB Without a Dedicated IT Team": "Protege tu Pyme sin Equipo de TI Dedicado",
        "Practical, affordable security": "Seguridad práctica y asequible"
    },
    "20250908-errores-comunes-ciberseguridad-pymes.md": {},
    "20250515-guia-practica-seguridad-dispositivos-moviles.md": {},
    "20251023-vulnerabilidades-seguridad-ai-llms.md": {},
    "20251020-seguridad-dispositivos-IoT-PYMES-riesgos-y-como-mitigarlos.md": {},
    "20250319-acceso-zero-trust-arquitectura-seguridad.md": {},
    "20250430-malware-red-dispara-94-analisis-informe-watchguard.md": {
        "Assess Your Infostealer Risk": "Evalúa tu Riesgo de Infostealers",
        "Credential exposure analysis + protection plan": "Análisis de exposición de credenciales + plan de protección"
    },
    "20251202-checklist-ciberseguridad-fin-ano-pymes.md": {},
    "20251210-tendencias-ciberamenazas-2026.md": {},
    "20251121-ciberamenazas-black-friday-2025-tendencias-2026.md": {},
    "20250611-infostealers-amenaza-robo-datos.md": {
        "Assess Your Infostealer Risk": "Evalúa tu Riesgo de Infostealers",
        "Credential exposure analysis + protection plan": "Análisis de exposición de credenciales + plan de protección"
    },
    "20250910-guia-60-minutos-ataque-ransomware.md": {},
}

base_dir = "content/es"

for filename, replacements in phase1_posts.items():
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — not found")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Apply replacements
    for english, spanish in replacements.items():
        content = content.replace(english, spanish)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} — updated")
    else:
        if replacements:
            print(f"ℹ️  {filename} — no matches found (already fixed?)")
        else:
            print(f"ℹ️  {filename} — no English CTAs to fix")

print("\n✓ Phase 1 CTA fixes complete")
