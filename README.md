# Proyecto de Pruebas con Chaos Toolkit

## Descripción

Este proyecto demuestra el uso de **Chaos Toolkit** para realizar pruebas de ingeniería del caos en un servicio backend simple desarrollado con Flask. El objetivo es validar la resiliencia y capacidad de recuperación del sistema ante fallos controlados.

## ¿Qué es Chaos Toolkit?

Chaos Toolkit es una herramienta de código abierto para realizar **ingeniería del caos** - una disciplina que consiste en experimentar con sistemas distribuidos para construir confianza en su capacidad de resistir condiciones turbulentas en producción.

### Conceptos Clave

- **Steady State Hypothesis**: Define el estado normal del sistema
- **Method**: Acciones que introducen el caos (experimentos)
- **Probes**: Verificaciones del estado del sistema
- **Rollbacks**: Acciones para restaurar el sistema

## Componentes del Proyecto

### 1. Servicio Flask (`app.py`)

Servicio web simple que expone un endpoint de salud:

```python
GET /health -> {"status": "ok"}
```

El servicio:

- Escucha en el puerto `8080`
- Registra su PID en `service.pid`
- Maneja señales de apagado limpiamente

### 2. Experimento de Chaos (`service-crash-experiment.json`)

Experimento que prueba: **"¿Qué sucede si el servicio backend se cae?"**

**Hipótesis de Estado Estable:**

- El archivo `service.pid` existe (servicio en ejecución)
- El endpoint `/health` responde con código 200

**Método (Inyección de Caos):**

1. Mata el proceso del servicio usando su PID
2. Intenta acceder al endpoint `/health`

**Rollback:**

- Reinicia el servicio automáticamente

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Ferkhan/chaos-toolkit.git
cd chaos-toolkit
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```cmd
.\.venv\Scripts\activate.bat
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Paso 1: Iniciar el Servicio

**Opción A - Manual:**

```bash
python app.py
```

**Opción B - Script (Linux/Mac):**

```bash
bash start-service.sh
```

**Opción C - PowerShell (Windows):**

```powershell
Start-Process python -ArgumentList "app.py"
```

Verifica que el servicio esté corriendo:

```bash
curl http://localhost:8080/health
```

Deberías ver: `{"status":"ok"}`

### Paso 2: Ejecutar el Experimento de Chaos

```bash
chaos run service-crash-experiment.json
```

### Paso 3: Analizar Resultados

Chaos Toolkit generará un archivo `journal.json` con los resultados detallados del experimento:

```bash
# Ver resumen
chaos report journal.json

# Ver reporte en formato HTML (si tienes chaostoolkit-reporting)
chaos report --export-format=html journal.json report.html
```

## Interpretación de Resultados

### Resultado Exitoso ✅

```cmd
[INFO] Steady-state hypothesis: Service is responding normally
[INFO] Probe: service-is-running
[INFO] => passed
[INFO] Probe: api-responds
[INFO] => passed
[INFO] Action: kill-backend-service
[INFO] Probe: wait-for-recovery
[INFO] => failed (expected)
[INFO] Rollback: restart-service
```

### Resultado Fallido ❌

Si alguna prueba del estado estable falla, el experimento se detiene y no se inyecta el caos.
