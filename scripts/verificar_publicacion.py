#!/usr/bin/env python3
"""Bloquea subida accidental de material privado y valida totales agregados."""
from pathlib import Path
import json,sys
r=Path(__file__).resolve().parents[1];violations=[]
for file in r.rglob('*'):
 if not file.is_file() or '.git' in file.parts:continue
 if file.suffix.lower() in {'.xlsx','.xls','.xlsm','.csv','.gpkg','.shp','.kml','.kmz'}:violations.append(str(file.relative_to(r)))
 if 'privado' in file.parts:violations.append(str(file.relative_to(r)))
path=r/'public'/'data'/'resumen_publico.json';d=json.loads(path.read_text(encoding='utf8'))
for row in d['registros']:
 assert set(row)=={'obra','frente','tipo','instalacion','cantidad'}
 assert row['cantidad']>0
assert sum(row['cantidad'] for row in d['registros'])==d['metadata']['registros_originales']
assert sum(x['cantidad'] for x in d['operacion_por_obra'])==d['metadata']['registros_originales']
if violations:raise SystemExit('ERROR: Archivos privados incluidos: '+repr(violations))
print('Validación OK: agregaciones coherentes; no se detectaron archivos privados. PUBLICACIÓN SUJETA A AUTORIZACIÓN INSTITUCIONAL.')
