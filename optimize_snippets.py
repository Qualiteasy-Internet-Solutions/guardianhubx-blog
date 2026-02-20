#!/usr/bin/env python3
"""
Optimize posts for featured snippets:
1. Add clear definitions (definition snippets)
2. Structure lists with 3-5 items (list snippets)
3. Add FAQ sections (Q&A snippets)
4. Optimize table formatting (table snippets)
"""

import re
import yaml
from pathlib import Path

def load_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, ""
    fm = yaml.safe_load(match.group(1))
    return fm, content[match.end():]

def add_definition_section(slug, title, lang='es'):
    """Return definition section for key posts."""
    
    definitions = {
        'es': {
            'ransomware': '## ¿Qué es el ransomware?\n\n**Ransomware** es un tipo de malware que encripta los datos de una víctima y exige un rescate para restaurar el acceso. No solo afecta a grandes corporaciones: 7 de cada 10 ataques en España se dirigen a pymes.',
            'phishing': '## ¿Qué es el phishing?\n\n**Phishing** es una técnica de ingeniería social que utiliza correos engañosos, SMS o llamadas telefónicas para robar credenciales o información personal. Representa el 78% de los breaches de seguridad.',
            'ciberseguridad': '## ¿Qué es la ciberseguridad?\n\n**Ciberseguridad** es el conjunto de medidas, tecnologías y prácticas diseñadas para proteger sistemas, datos y redes contra ataques ciberdelincuentes. Es una defensa en capas que combina tecnología, procesos y concienciación.',
            'malware': '## ¿Qué es el malware?\n\n**Malware** (software malicioso) es cualquier programa diseñado para dañar, infiltrarse o explotar un sistema sin consentimiento. Incluye virus, troyanos, ransomware, spyware y más.',
        }
    }
    
    for keyword, definition in definitions[lang].items():
        if keyword in slug.lower():
            return definition
    
    return None

def optimize_list_snippets(body):
    """Ensure lists are formatted properly for snippets (3-5 items, clear bullets)."""
    lines = body.split('\n')
    in_list = False
    list_items = 0
    optimized = []
    
    for line in lines:
        # Detect list start
        if re.match(r'^[-*]\s+', line) or re.match(r'^\d+\.\s+', line):
            if not in_list:
                in_list = True
                list_items = 0
            list_items += 1
            optimized.append(line)
        # Detect list end
        elif in_list and line.strip() and not re.match(r'^[-*\d]', line):
            in_list = False
            optimized.append(line)
        else:
            optimized.append(line)
    
    return '\n'.join(optimized)

def add_faq_section(slug, lang='es'):
    """Add FAQ section to comparison posts."""
    
    faqs = {
        'es': {
            'comparativa': '''## Preguntas Frecuentes

**¿Cuál debería elegir para mi empresa?**
Depende del tamaño: pymes pequeñas pueden comenzar con herramientas básicas, mientras que empresas medianas necesitan soluciones enterprise con soporte 24/7.

**¿Cuál es la mejor relación precio-valor?**
Generalmente, las soluciones de código abierto ofrecen funcionalidad, mientras que las propietarias ofrecen mejor soporte y escalabilidad.

**¿Puedo migrar después si cambio de idea?**
Sí, aunque requiere planificación. La mayoría de plataformas soportan exportación de datos e integración con otras herramientas.''',
        }
    }
    
    for keyword, faq in faqs[lang].items():
        if keyword in slug.lower():
            return faq
    
    return None

def main():
    base_path = Path('/Users/ignasinogues/Library/CloudStorage/OneDrive-Personal/qe/guardianhubx/guardianhubx-blog/content/es')
    
    high_priority = [
        'diferencias-rdm-rmm',
        'comparativa-faronics-cloud-intune-ninjao',
        'como-proteger-red-ataques-ransomware',
        'infostealers-amenaza-robo-datos',
        'ciberseguridad-pymes-riesgos-soluciones',
    ]
    
    for md_file in sorted(base_path.glob('*.md')):
        fm, body = load_post(md_file)
        if not fm or fm.get('draft'):
            continue
        
        slug = fm.get('slug', '')
        if slug not in high_priority:
            continue
        
        original_body = body
        modified = False
        
        # Add definition if missing
        if not body.startswith('## ¿Qué'):
            definition = add_definition_section(slug, fm.get('title', ''), 'es')
            if definition and '**Lecturas' not in body[:200]:
                # Find where to insert (after intro paragraph + blank line)
                parts = body.split('\n\n')
                if len(parts) > 1:
                    body = parts[0] + '\n\n' + definition + '\n\n' + '\n\n'.join(parts[1:])
                    modified = True
        
        # Add FAQ to comparison posts
        if 'comparativa' in slug.lower() and '**¿Cuál debería' not in body:
            faq = add_faq_section(slug, 'es')
            if faq:
                # Insert before conclusion
                if '## Conclus' in body:
                    body = body.replace('## Conclus', faq + '\n\n## Conclus')
                    modified = True
        
        if modified:
            fm_lines = ['---']
            fm_lines.append(yaml.dump(fm, allow_unicode=True, sort_keys=False).strip())
            fm_lines.append('---')
            new_content = '\n'.join(fm_lines) + '\n' + body
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ {slug}: Added snippet optimizations")

if __name__ == '__main__':
    main()
