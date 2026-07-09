#!/usr/bin/env python3
"""TNR — atman-hub : validation avant push"""
import subprocess, sys, json, os, re

html_path = "/Users/jahangir/Desktop/atman-hub/index.html"
errors = []

with open(html_path) as f:
    html = f.read()

# 1. Structure HTML
print("🔍 1/6 Structure HTML…")
if '<!DOCTYPE html>' not in html: errors.append("Doctype manquant")
if '</html>' not in html: errors.append("Fermeture html manquante")
if '<style>' not in html or '</style>' not in html: errors.append("Style manquant")
if '<script>' not in html or '</script>' not in html: errors.append("Script manquant")
if '<meta charset="UTF-8">' not in html: errors.append("Charset manquant")
if '<meta name="viewport"' not in html: errors.append("Viewport manquant")
print("  ✅" if not errors else "  ❌ " + str(errors))

# 2. Liens externes
print("\n🔍 2/6 Liens externes…")
urls = re.findall(r'https?://[^\s"\'<>]+', html)
for u in urls:
    if 'fonts.googleapis.com' in u: continue
    if 'fonts.gstatic.com' in u: continue
    try:
        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '-m', '10', u],
                         capture_output=True, text=True, timeout=15)
        code = int(r.stdout)
        if code >= 400:
            errors.append(f"Lien mort: {u} ({code})")
            print(f"  ❌ {u} → {code}")
        else:
            print(f"  ✅ {u} → {code}")
    except:
        errors.append(f"Timeout: {u}")
        print(f"  ⚠️  {u} → timeout")

# 3. Design system
print("\n🔍 3/6 Design system…")
checks = {
    'Fond #0a0a0f': '#0a0a0f' in html,
    'Accent violet #7c3aed': '#7c3aed' in html,
    'Accent indigo #6366f1': '#6366f1' in html,
    'Blanc cassé #f1f5f9': '#f1f5f9' in html,
    'Glassmorphism backdrop-filter': 'backdrop-filter:blur' in html,
    'Border radius 16px': '16px' in html and 'border-radius' in html,
    'Inter font': "'Inter'" in html or '"Inter"' in html,
    'Grid responsive 3 cols': 'repeat(3,1fr)' in html,
    'Responsive 2 cols': '@media(max-width:1024px)' in html and 'repeat(2,1fr)' in html,
    'Responsive 1 col': '@media(max-width:640px)' in html and ('1fr' in html.split('@media')[2] if len(html.split('@media')) > 2 else '1fr' in html),
    'Animation fade-in': 'card-fade-in' in html,
    'Animation staggered': 'animationDelay' in html,
    'Hover scale': 'scale(1.01)' in html or 'scale(1.02)' in html or 'scale(1.03)' in html,
    'Pulse dot en ligne': 'pulse-dot' in html,
    'Max-width 1200px': '1200px' in html and 'max-width' in html,
}
for label, ok in checks.items():
    print(f"  {'✅' if ok else '❌'} {label}")
    if not ok: errors.append(f"Design: {label}")

# 4. Contenu — 5 projets
print("\n🔍 4/6 Contenu — 5 projets…")
projects = ['LLM Man', 'TDAH Profile', 'JobHunt', 'Nous AI News', 'QA Universe']
for p in projects:
    if p in html:
        print(f"  ✅ {p}")
    else:
        errors.append(f"Projet manquant: {p}")
        print(f"  ❌ {p}")

# 5. Fonctionnalités JS
print("\n🔍 5/6 Fonctionnalités JS…")
js_checks = {
    'Filtre dynamique': 'filterCards' in html and 'data-filter' in html,
    'Date dynamique': 'getFullYear()' in html,
    'Staggered delay': '50 * i' in html or '50*i' in html,
    'Onglet target _blank': 'target=\"_blank\"' in html,
    'Noopener rel': 'rel=\"noopener\"' in html,
}
for label, ok in js_checks.items():
    print(f"  {'✅' if ok else '❌'} {label}")
    if not ok: errors.append(f"JS: {label}")

# 6. Zéro dépendance
print("\n🔍 6/6 Zéro dépendance externe…")
for dep in ['node_modules', 'import React', 'from "', "from '", 'npm', 'cdn.jsdelivr', 'unpkg.com']:
    if dep in html:
        errors.append(f"Dépendance trouvée: {dep}")
        print(f"  ❌ {dep}")
if errors:
    print(f"  ✅ Google Fonts seulement (intentionnel)")
else:
    print(f"  ✅ Google Fonts seulement (intentionnel)")

# Résultat
print("\n" + "="*50)
if errors:
    print(f"\n❌ TNR ÉCHOUÉ — {len(errors)} erreur(s)")
    for e in errors: print(f"  • {e}")
    sys.exit(1)
else:
    print("\n✅ TNR PASSÉ — 0 erreur, prêt à push")
