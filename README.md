# LabTrack-backend

Perfecto, aquí tienes todo el texto en un solo documento Markdown listo para tu README de GitHub:

````markdown
# Instrucciones para ejecutar el proyecto

Clonar repositorio:

git clone https://github.com/J0RG3-/LabTrack-backend.git
````


Iniciar gitflow:

```bash
git flow init
```

Crear un entorno virtual (se presupone que tiene las dependencias de Python instaladas en su máquina):

```bash
python3 -m venv .venv
```

Activar el entorno virtual:

* Linux (bash):

```bash
source .venv/bin/activate
```

* Windows (PowerShell):

```powershell
.\.venv\Scripts\activate
```

Instalar dependencias necesarias (Linux y Windows):

```bash
pip install -r requirements.txt
```

Ejecutar el servidor del backend (Linux y Windows):

```bash
uvicorn main:app --reload
```

```

