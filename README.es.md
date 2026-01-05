[![English](https://img.shields.io/badge/Language-English-blue)](README.md)

# Reputación AI

Herramienta avanzada de análisis de reputación online y monitoreo de marca basada en Inteligencia Artificial.

## Descripción General

Esta aplicación permite introducir el nombre de una empresa o persona para obtener un análisis detallado de su presencia online. El sistema utiliza modelos de lenguaje (LLMs) para procesar información y devuelve métricas clave como sentimiento general, puntuación de salud de marca y un resumen ejecutivo. Además, ofrece la capacidad de generar exportables en PDF para la presentación de informes corporativos.

## Demo y Capturas

Para ver la aplicación en funcionamiento, consulte las siguientes capturas:

### Panel de Análisis
![Panel Principal](docs/screenshots/dashboard_placeholder.png)
*Vista principal donde el usuario introduce la entidad a analizar.*

### Informe breve
![Informe breve](docs/screenshots/quick_report_placeholder.png)
*Informe breve con el análisis de sentimiento general, puntuación de salud de marca y un resumen ejecutivo.*

### Informe PDF Generado
![Reporte PDF](docs/screenshots/pdf_sample.png)
*Ejemplo, del informe ejecutivo generado en formato PDF.*

### Descargar ejemplo de informe PDF generado
![Descargar informe PDF](docs/screenshots/download_pdf_placeholder.pdf)
*ejecutivo generado en formato PDF de la empresa Microsoft Corp.*

## Requisitos Previos

Antes de desplegar la aplicación, es necesario configurar las variables de entorno para el acceso a la API del modelo de lenguaje.

### Configuración del Entorno (.env)

Cree un archivo `.env` en el directorio `mysite/` con las siguientes credenciales. Puede obtener su API Key gratuita en [Groq Console](https://console.groq.com/).

```bash
# mysite/.env
GROQ_API_KEY=gsk_...
```

**Nota:** Asegúrese de que el modelo `openai/gpt-oss-120b` (o el configurado en `services.py`) esté disponible en su cuenta.

## Despliegue con Docker (Containerization)

Este proyecto está totalmente "dockerizado" para facilitar su despliegue y orquestación.

### Construcción y Ejecución

Para levantar el entorno completo (build & run), utilice Docker Compose. Este comando construirá la imagen optimizada y ejecutará el contenedor exponiendo el servicio en el puerto `8000`.

```bash
docker-compose up --build
```

### Servicios

- **Web**: Aplicación Django accesible en `http://localhost:8000`.

## Estructura del Proyecto

- `mysite/`: Código fuente de la aplicación Django.
- `mysite/Dockerfile`: Definición de la imagen de contenedor (basada en Python Slim).
- `mysite/docker-compose.yml`: Orquestación de servicios.

### Acerca de mi
Senior developer (20+ años PHP/MySQL e-commerce) en transición a AI/ML.
👔 Abierto a roles remotos AI/ML roles en consultorías europeas
📧 Contacto: hola@josemayor.dev | LinkedIn: https://www.linkedin.com/in/josemayor-ai-ml-developer/
