#!/usr/bin/env python3
"""Fix ALL remaining English CTAs to Spanish across all posts."""

import os
import re

# English → Spanish translations for CTAs
translations = {
    # CTA titles
    "Master Cybersecurity Terminology": "Domina la Terminología de Ciberseguridad",
    "Master AI-Powered Threat Detection": "Domina Detección de Amenazas con IA",
    "Schedule Your NIS2 Compliance Audit (Free)": "Programa tu Auditoría de Cumplimiento NIS2 (Gratis)",
    "Get Holiday Security Checklist (Free)": "Obtén Checklist de Seguridad en Fechas Clave (Gratis)",
    "Request Your Free Security Assessment": "Solicita tu Evaluación de Seguridad Gratuita",
    "Download the Complete Cybersecurity Glossary": "Descarga el Glosario Completo de Ciberseguridad",
    "Get Education Security Plan (Free)": "Obtén Plan de Seguridad para Educación (Gratis)",
    "Get AI Threat Strategy (Free)": "Obtén Estrategia contra Amenazas de IA (Gratis)",
    "Request Resilience Assessment (Free)": "Solicita Evaluación de Ciberresiliencia (Gratis)",
    "Get SMB Security Blueprint (Free)": "Obtén Plan de Seguridad para Pymes (Gratis)",
    "Identify Your Attack Vectors (Free)": "Identifica tus Vectores de Ataque (Gratis)",
    "Download Ransomware Response Plan (Free)": "Descarga Plan de Respuesta a Ransomware (Gratis)",
    "Get Mobile Security Assessment (Free)": "Obtén Evaluación de Seguridad Móvil (Gratis)",
    "Get Holiday Security Brief (Free)": "Obtén Resumen de Seguridad en Fechas Clave (Gratis)",
    "Get Year-End Security Audit (Free)": "Obtén Auditoría de Seguridad de Fin de Año (Gratis)",
    "Download 2026 Threat Forecast (Free)": "Descarga Pronóstico de Amenazas 2026 (Gratis)",
    "Get Cloud Security Assessment (Free)": "Obtén Evaluación de Seguridad en Nube (Gratis)",

    # Descriptions/Benefits
    "Understand threats + protect effectively": "Comprende amenazas + protégete efectivamente",
    "Stay ahead of evolving evasion techniques": "Adelántate a técnicas de evasión en evolución",
    "Identify regulatory gaps and protection gaps in just 20 minutes": "Identifica brechas regulatorias y de protección en 20 minutos",
    "Expert guidance for year-end protection": "Orientación experta para protección de fin de año",
    "20-minute consultation with zero obligation": "Consulta de 20 minutos sin compromiso",
    "Free guide with 50+ essential terms": "Guía gratuita con 50+ términos esenciales",
    "Tailored ransomware protection for schools": "Protección contra ransomware adaptada para escuelas",
    "Learn how to defend against next-gen attacks": "Aprende a defenderte contra ataques de nueva generación",
    "Análisis experto + actionable protection plan": "Análisis experto + plan de protección accionable",
    "Tailored protection strategy + implementation guide": "Estrategia de protección personalizada + guía de implementación",
    "Security assessment + mitigation roadmap": "Evaluación de seguridad + plan de mitigación",
    "Step-by-step guide + expert consultation": "Guía paso a paso + consulta experta",
    "Revisión experta of your endpoint security": "Revisión experta de tu seguridad de endpoints",
    "Threat trends + protection checklist": "Tendencias de amenazas + checklist de protección",
    "Evaluación experta + remediation plan": "Evaluación experta + plan de remediación",
    "Predicciones expertas + defense strategy": "Predicciones expertas + estrategia defensiva",
    "Configuration review + vulnerability analysis": "Revisión de configuración + análisis de vulnerabilidades",
}

base_dir = "content/es"
fixed_count = 0
file_count = 0

for filename in os.listdir(base_dir):
    if not filename.endswith(".md"):
        continue

    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Apply all translations
    for english, spanish in translations.items():
        if english in content:
            content = content.replace(english, spanish)
            fixed_count += 1

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        file_count += 1
        print(f"✅ {filename}")

print(f"\n✓ Fixed {fixed_count} English CTA phrases in {file_count} posts")
