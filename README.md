# Exámenes
## Generador de cuestionarios con resultados en tiempo real

Una aplicación web para generar y evaluar cuestionarios de forma interactiva, ideal para estudiantes que deseen practicar y visualizar sus resultados en tiempo real. Los usuarios pueden responder preguntas organizadas en bloques, obtener su puntuación, ver los errores cometidos y las respuestas correctas.

![Captura de pantalla](https://rnlagos.com/images/ksnip_20241204-144309.png)

### Características:

- Generación de cuestionarios dinámicos a partir de un archivo CSV.
- Organización de preguntas por bloques temáticos.
- Visualización de resultados en tiempo real en un menú lateral o en una nueva pestaña.
- Cálculo de tiempo total tomado para responder.
- Identificación de preguntas falladas con sus respuestas correctas.
- Diseño responsivo e interactivo utilizando Bootstrap 5.
- Cada respuesta incorrecta descuenta 0.25 puntos del cómputo global.

### Requisitos

- Python 3.10+ pip o conda para la instalación de dependencias.
- Un entorno Linux o Windows (también funciona en MacOS).
- Un archivo preguntas.csv que contenga las preguntas del cuestionario.

### Dependencias

Las siguientes dependencias se gestionan mediante pip:

- fastapi: Framework web para el backend.
- uvicorn: Servidor ASGI para ejecutar la aplicación.
- jinja2: Motor de plantillas para renderizar las páginas HTML.
- pandas: Manejo y procesamiento de datos desde el archivo CSV.

Para instalar estas dependencias, usa:

`pip install -r requirements.txt`

Instalación y Configuración

Clonar el repositorio

`git clone https://github.com/rnlagos/examenes.git`  

`cd examenes`

Crear un entorno virtual Si usas pip:

`python -m venv env`  

`source env/bin/activate  # En Windows: env\Scripts\activate`

Si usas conda:

`conda create -n cuestionarios python=3.10`  

`conda activate cuestionarios`

Instalar las dependencias

`pip install -r requirements.txt`

Agregar un archivo preguntas.csv Asegúrate de que el archivo preguntas.csv tenga el siguiente formato:

Bloque,Pregunta,A,B,C,D,Correcta
1, "¿Cuál es la capital de Francia?", "París", "Londres", "Berlín", "Madrid", "A" ```

Ejecutar la aplicación

`uvicorn app.main:app --reload`
Abrir la aplicación en el navegador Ve a http://127.0.0.1:8000.
