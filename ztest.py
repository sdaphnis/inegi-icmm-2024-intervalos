"""Prueba z de diferencia de medias: municipio #1 contra cada uno del top 40.
Supone estimaciones independientes (simplificación: las estimaciones de áreas
pequeñas comparten el mismo modelo e INEGI no publica covarianzas)."""
import pandas as pd, numpy as np
from scipy.stats import norm
d = pd.read_csv('datos.csv', dtype={'cvegeo': str})
top = d.iloc[0]
d['z'] = (top.estimacion - d.estimacion) / np.sqrt(top.ee**2 + d.ee**2)
d['p_bilateral'] = 2 * norm.sf(d.z.abs())
d['traslape_ic95'] = d.ls95 >= top.li95
out = d.iloc[1:][['rank', 'municipio', 'entidad', 'estimacion', 'ee', 'z', 'p_bilateral', 'traslape_ic95']]
print(f"Referencia: #1 {top.municipio} ({top.estimacion:,.0f}, EE {top.ee:,.0f})")
print(out.head(10).round(3).to_string(index=False))
out.to_csv('ztest_vs_1.csv', index=False, float_format='%.4f')
