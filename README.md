# FBRef Scrap Python

Este proyecto en Python extrae datos de estadísticas de futbol (como tablas de clasificación, estadísticas de equipos y partidos) de fbref.com y los almacena en base de datos mysql.

## **Requisitos Previos**

- Python 3.12.1

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd fbref-scrap-py
   ```

2. Crear un entorno virtual:
   ```bash
   python -m venv entorno
   ```

3. Activar el entorno virtual:
   - **Windows:**
     ```powershell
     .\entorno\Scripts\Activate.ps1
     ```
   - **Linux/Mac:**
     ```bash
     source entorno/bin/activate
     ```

4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```


## **Configuración**

El archivo `competitions.yaml` contiene las configuraciones de las competiciones que se procesarán.

Comenta las competiciones que no desees extraer información.

## **Uso**

Ejecuta el script principal para iniciar la extracción y el procesamiento de datos:

```bash
python src/init.py
```