"""Réplica de la Gráfica 1 (Comunicado de prensa 88/26) / Gráfica 2 (Reporte de resultados 39/26)
del INEGI, ICMM 2024, con intervalos de confianza al 95 % calculados con los errores estándar publicados.
Datos: datos.csv (generado por extract.py a partir de icmm_2024_tabulados.xlsx)."""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

d = pd.read_csv('datos.csv', dtype={'cvegeo': str})

# Valores publicados en la gráfica del INEGI (redondeados), para verificar orden y cifras
publicados = [176661,155273,149095,147423,140948,130959,130014,125350,120651,120614,119350,116197,115063,
              114573,114438,111364,110463,109898,108897,108530,108405,108376,107482,107473,107189,107030,
              106710,106637,106272,105767,104461,104228,104158,103902,103122,102401,101501,101184,99944,99780]
assert list(d.estimacion.round().astype(int)) == publicados, 'No coincide con la gráfica publicada'

abrev = {'Ciudad de México':'CDMX','Nuevo León':'NL','Querétaro':'Qro.','Baja California Sur':'BCS',
         'Quintana Roo':'Q. Roo','Sonora':'Son.','Coahuila de Zaragoza':'Coah.','Jalisco':'Jal.',
         'Chihuahua':'Chih.','Baja California':'BC','Yucatán':'Yuc.','San Luis Potosí':'SLP'}
d['etiqueta'] = d.municipio + ', ' + d.entidad.map(abrev)
col = {'Ciudad de México':'#7B1E3A', 'Nuevo León':'#1F5FA8'}
otros = '#8C8C8C'
d['color'] = d.entidad.map(col).fillna(otros)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig, ax = plt.subplots(figsize=(10.8, 13.5), dpi=200)   # 2160 x 2700 px (proporción 4:5, 1080x1350 x2)
fig.subplots_adjust(left=0.30, right=0.96, top=0.875, bottom=0.10)

y = np.arange(len(d))[::-1]
# Banda: IC 95 % del municipio #1
ax.axvspan(d.li95[0], d.ls95[0], color=col['Ciudad de México'], alpha=0.08, zorder=0, lw=0)
ax.axvline(d.li95[0], color=col['Ciudad de México'], alpha=0.35, lw=0.8, ls='--', zorder=0)
for yi, (_, r) in zip(y, d.iterrows()):
    ax.plot([r.li95, r.ls95], [yi, yi], color=r.color, lw=2.2, alpha=0.55, solid_capstyle='round', zorder=2)
    ax.plot(r.estimacion, yi, 'o', color=r.color, ms=6.5, zorder=3, mec='white', mew=0.8)
    ax.text(r.ls95 + 1500, yi, f"{r.estimacion:,.0f}".replace(',', ' '), va='center', fontsize=8.5, color='#333333')

ax.set_yticks(y)
ax.set_yticklabels([f"{int(r)}. {e}" for r, e in zip(d['rank'], d.etiqueta)], fontsize=10)
for lab, c in zip(ax.get_yticklabels(), d.color):
    lab.set_color(c if c != otros else '#444444')
ax.set_ylim(-0.8, len(d) - 0.2)
ax.set_xlim(80000, 222000)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"${v/1000:,.0f} mil"))
ax.set_xlabel('Ingreso corriente promedio trimestral por hogar (pesos de 2024)', fontsize=11)
ax.grid(axis='x', color='#DDDDDD', lw=0.7); ax.set_axisbelow(True)
for s in ['top', 'right', 'left']:
    ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)

fig.text(0.03, 0.965, 'Los 40 municipios con mayor ingreso por hogar, 2024', fontsize=19, weight='bold', ha='left')
fig.text(0.03, 0.940, 'Ingreso corriente promedio trimestral por hogar (ICPTH): estimación puntual e intervalo de confianza al 95 %',
         fontsize=11.2, ha='left', color='#333333')
fig.text(0.03, 0.920, 'Banda sombreada: IC 95 % de Benito Juárez (#1). Los intervalos que la alcanzan se traslapan con el del primer lugar.',
         fontsize=9.3, ha='left', color='#555555')
handles = [Line2D([0],[0], color=col['Ciudad de México'], marker='o', lw=2.2, label='Ciudad de México'),
           Line2D([0],[0], color=col['Nuevo León'], marker='o', lw=2.2, label='Nuevo León'),
           Line2D([0],[0], color=otros, marker='o', lw=2.2, label='Otras entidades'),
           Patch(color=col['Ciudad de México'], alpha=0.12, label='IC 95 % de Benito Juárez')]
ax.legend(handles=handles, loc='lower right', frameon=True, framealpha=0.95, edgecolor='#DDDDDD', fontsize=9.5)

fig.text(0.03, 0.045, 'Fuente: INEGI, Ingreso Corriente para los Municipios de México (ICMM) 2024. Estimación en áreas pequeñas, 2026.', fontsize=8.8, ha='left', color='#444444')
fig.text(0.03, 0.030, 'IC al 95 % calculados con los errores estándar publicados (estimación ± 1.96 × EE); INEGI publica límites al 90 %.', fontsize=8.8, ha='left', color='#444444')
fig.text(0.03, 0.015, 'Estimaciones de áreas pequeñas (basadas en un modelo) a partir de la ENIGH 2024. Pesos constantes de 2024.', fontsize=8.8, ha='left', color='#444444')
fig.savefig('ingreso_municipal_ic95.png', dpi=200, facecolor='white')
print('ok')
