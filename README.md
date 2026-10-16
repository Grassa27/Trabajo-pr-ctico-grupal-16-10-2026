# Pipeline de control de presión arterial

**Integrantes:** Gonzalo Bonadeo, Juan Manuel Rodon, Valentino Grassini

## Problema y usuario
Un equipo de salud recibe mediciones de presión arterial en CSV y JSON con errores de carga.
El programa descarta los registros inválidos, informa el motivo de cada rechazo y resume
la presión sistólica por grupo del estudio.

## Datos
Ver [`data/README.md`](data/README.md). Cada fila corresponde a un paciente con una medición.

## Estructura
```
├── data/            mediciones.csv, mediciones.json y su descripción
├── src/
│   ├── fuentes.py   FuenteDatos (abstracta), FuenteCSV, FuenteJSON
│   ├── modelo.py    Clase Paciente
│   ├── pipeline.py  Validación, limpieza, reporte y guardado
│   └── main.py      Punto de entrada
└── tests/
    └── test_pipeline.py
```

## Ejecución
No requiere bibliotecas externas (Python 3.10 o superior).
```bash
python src/main.py data/mediciones.csv
```
Genera `outputs/reporte.csv` y `outputs/rechazos.csv`.

## Pruebas
```bash
python tests/test_pipeline.py
```

## Reglas de limpieza
- Código con formato `PAC-` y tres dígitos (expresión regular `PAC-\d{3}`, validada con `fullmatch`).
- Rangos válidos: edad 18 a 100 años, IMC 12 a 60 kg/m², presión sistólica 70 a 250 mmHg.
- Grupos admitidos: `A` (control) y `B` (intervención).
- Valores faltantes (`""` en CSV, `null` en JSON) o no numéricos: el registro se rechaza.
- Códigos duplicados: se conserva la primera aparición y se rechazan las siguientes.
- Cada rechazo se guarda con su fila (contando desde 1), su código y el motivo.

## Resultado de ejemplo
```
Leídos: 58 | válidos: 50 | rechazados: 8
{'grupo': 'A', 'cantidad': 27, 'presion_media': 127.26, 'proporcion_hipertensos': 0.185}
{'grupo': 'B', 'cantidad': 23, 'presion_media': 118.61, 'proporcion_hipertensos': 0.13}
```

Registros rechazados:

| Fila | Código | Motivo |
|---|---|---|
| 6 | PAC01 | código con formato inválido |
| 17 | PAC-051 | edad faltante |
| 23 | PAC-052 | presion_sistolica fuera de rango |
| 34 | PAC-012 | código duplicado |
| 40 | PAC-053 | imc no numérico |
| 46 | PAC-054 | grupo inválido |
| 52 | PAC-055 | edad fuera de rango |
| 58 | PAC-056 | presion_sistolica faltante |

## Limitaciones
- Datos simulados con fines didácticos (50 pacientes).
- El umbral de hipertensión (PAS ≥ 140 mmHg) es un criterio simplificado, no un diagnóstico clínico.
- `main.py` solo procesa archivos CSV.
- Los rangos válidos son fijos en el código.
