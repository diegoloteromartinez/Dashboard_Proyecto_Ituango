#!/usr/bin/env python3
"""Procesa un inventario local. NO copia identificadores, coordenadas ni observaciones."""
from pathlib import Path
from collections import Counter,defaultdict
import openpyxl,json,sys,re,datetime
ROOT=Path(__file__).resolve().parents[1]
SRC=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'privado'/'LIST-INSTRUMENTOS_REV_25_EPM(1).xlsx'
OUT=ROOT/'public'/'data'/'resumen_publico.json'
if not SRC.is_file(): raise SystemExit(f'No existe el archivo privado: {SRC}')
wb=openpyxl.load_workbook(SRC,read_only=True,data_only=True)
g=wb['Glosario']; glossary=list(g.iter_rows(min_row=2,max_col=9,values_only=True))
frentes={str(r[1]).strip():str(r[2]).strip() for r in glossary if r[1] and r[2]}
tipos={str(r[7]).strip():str(r[8]).strip() for r in glossary if r[7] and r[8]}
subfrentes={str(r[3]).strip():str(r[4]).strip() for r in glossary if r[3] and r[4]}
s=wb['Listado']
fields=list(next(s.iter_rows(min_row=1,max_row=1,max_col=35,values_only=True)))
indices={v:i for i,v in enumerate(fields) if v}
rows=[]; ids=Counter(); missing_coords=0; dates=Counter(); mismatch=Counter()
for r in s.iter_rows(min_row=2,max_col=35,values_only=True):
 if not r[0] or not r[1]:continue
 obra,frente,tipo,inst,op=[str(r[i]).strip() if r[i] is not None else 'Sin dato' for i in (0,1,4,16,17)]
 sub=str(r[2]).strip() if r[2] else 'Sin dato'
 rows.append((obra,frente,tipo,inst,op,sub))
 if not r[25] or not r[26]:missing_coords+=1
 id_=str(r[7]).strip() if r[7] else ''
 if id_: ids[(obra,frente,id_)]+=1
 if isinstance(r[18],(datetime.datetime,datetime.date)):dates[str(r[18].year)]+=1
 if frente not in frentes:mismatch['frentes_sin_glosario']+=1
 if tipo not in tipos:mismatch['tipos_sin_glosario']+=1
all_count=len(rows)
# Publicación estadística. Pequeñas celdas se agrupan por tipo dentro del frente,
# preservando total por frente y por estado, pero evitando microceldas específicas.
groups=Counter((o,f,t,i) for o,f,t,i,op,su in rows)
public=Counter()
for (o,f,t,i),n in groups.items():
 public[(o,f,t if n>=10 else 'OTROS / AGRUPADOS',i)]+=n
# NO se publica el estado operativo individual combinado con frente, tipo ni subfrente.
operation=Counter((o,op) for o,f,t,i,op,su in rows)
front=Counter((o,f) for o,f,t,i,op,su in rows)
sub_counts=Counter((o,f,su) for o,f,t,i,op,su in rows)
# Exportar solo subtotales de subfrentes con grupos suficientes (>= 20 registros).
subs=[{'obra':o,'frente':f,'subfrente':su,'nombre':subfrentes.get(su,su),'cantidad':n} for (o,f,su),n in sub_counts.items() if n>=20]
public_data={
 'metadata':{'titulo':'Instrumentación geotécnica — Proyecto Ituango','dashboard_actualizado':'noviembre de 2026','fecha_corte_inventario':'No verificada','unidad':'Registros del listado, no instrumentos únicos','registros_originales':all_count,'politica':'Agregaciones estadísticas; sin geolocalización exacta ni identificadores','revision_publicacion':'REQUIERE APROBACIÓN EXPRESA ANTES DE PUBLICAR'},
 'categorias':{'frentes':frentes,'instrumentos':tipos,'subfrentes':subfrentes},
 'registros':[{'obra':o,'frente':f,'tipo':t,'instalacion':i,'cantidad':n} for (o,f,t,i),n in sorted(public.items())],
 'operacion_por_obra':[{'obra':o,'estado':op,'cantidad':n} for (o,op),n in sorted(operation.items())],
 'subfrentes':[x for x in sorted(subs,key=lambda x:(x['obra'],x['frente'],x['subfrente']))],
 'calidad':{'filas_validas':all_count,'sin_coordenadas':missing_coords,'identificadores_distintos_no_verificados':len(ids),'identificadores_repetidos':sum(1 for v in ids.values() if v>1),'identificadores_faltantes':all_count-sum(ids.values()),'advertencias':dict(mismatch),'fechas_instalacion_por_anio':dict(sorted(dates.items()))},
 'capas':{'presa':'Pendiente cartografía validada y autorización','vertedero':'Pendiente cartografía validada y autorización','subestacion':'Pendiente cartografía validada y autorización','obras_principales':'Pendiente cartografía validada y autorización'}
}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(public_data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'scripts'/'reporte_validacion.json').write_text(json.dumps({'filas':all_count,'frentes':len(set(r[1] for r in rows)),'tipos':len(set(r[2] for r in rows)),'estados_instalacion':dict(Counter(r[3] for r in rows)),'estados_operacion':dict(Counter(r[4] for r in rows)),'calidad':public_data['calidad']},ensure_ascii=False,indent=2),encoding='utf-8')
print('Procesados',all_count,'registros; archivo público',OUT,'bytes',OUT.stat().st_size)
