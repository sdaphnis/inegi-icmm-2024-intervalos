import pandas as pd, numpy as np
import zipfile, os
if not os.path.exists("datos_inegi/opendata"):
    zipfile.ZipFile("datos_inegi/conjunto_de_datos_icmm_2024_csv.zip").extractall("datos_inegi/opendata")
df = pd.read_excel('datos_inegi/icmm_2024_tabulados.xlsx', header=None, skiprows=5, usecols=[0,1,2,3], names=['ent','mun','est','val'])
df = df.dropna(subset=['est','val'])
df = df[df['mun'].astype(str).str.match(r'^\d{3} ')]
w = df.pivot_table(index=['ent','mun'], columns='est', values='val', aggfunc='first').reset_index()
w.columns.name=None
w = w.rename(columns={'Valor':'estimacion','Error estándar':'ee','Límite inferior de confianza':'li90_inegi','Límite superior de confianza':'ls90_inegi','Coeficiente de variación (%)':'cv_pct'})
print(len(w), 'municipios')
# cross-check with open data csv
od = pd.read_csv('datos_inegi/opendata/conjunto_de_datos/conjunto_de_datos_icmm_2024.csv', dtype=str)
od['icpth']=od['icpth'].str.replace(',','').astype(float)
odw = od[od.cve_mun!='000'].pivot(index='cvegeo', columns='est', values='icpth')
print(len(odw), 'municipios en datos abiertos')
w['cvegeo'] = w['ent'].str[:2] + w['mun'].str[:3]
m = w.merge(odw, left_on='cvegeo', right_index=True)
for k,c in [('1','estimacion'),('2','ee'),('3','li90_inegi'),('4','ls90_inegi'),('5','cv_pct')]:
    print(c, 'max abs diff xlsx vs csv:', (m[k]-m[c]).abs().max())
# check implied z of INEGI limits
z = (w.estimacion - w.li90_inegi)/w.ee
print('implied z INEGI limits: min %.5f max %.5f' % (z.min(), z.max()))
print('CV check max |cv - 100*ee/est|:', (w.cv_pct - 100*w.ee/w.estimacion).abs().max())
top = w.sort_values('estimacion', ascending=False).head(40).reset_index(drop=True)
top['rank']=top.index+1
top['entidad']=top['ent'].str[3:]
top['municipio']=top['mun'].str[4:]
top['li95']=top.estimacion-1.96*top.ee
top['ls95']=top.estimacion+1.96*top.ee
cols=['rank','cvegeo','municipio','entidad','estimacion','ee','cv_pct','li95','ls95','li90_inegi','ls90_inegi']
top[cols].to_csv('datos.csv', index=False, float_format='%.2f')
pd.set_option('display.width',250)
print(top[cols].round(1).to_string(index=False))
print('CV min/max for all municipios', w.cv_pct.min(), w.cv_pct.max())
