🤖 EMOTIA – Acompañante Emocional Interactivo para Telegram 💜

EMOTIA es un bot desarrollado en Python e integrado con Telegram, diseñado para ofrecer un espacio interactivo de acompañamiento emocional y entretenimiento. Permite identificar cómo se siente una persona mediante palabras clave, proporcionar consejos personalizados según su estado de ánimo y reproducirlos mediante mensajes de voz.

Además, cuenta con diferentes minijuegos, un sistema de recompensas, niveles e insignias que hacen que la experiencia sea dinámica y entretenida.

⸻

📋 Tabla de contenidos

* Descripción del proyecto
* Objetivos
* Características principales
* Tecnologías utilizadas
* Requisitos previos
* Instalación
* Configuración
* Ejecución
* Comandos disponibles
* Funcionamiento del bot
* Base de datos
* Estructura del proyecto
* Consideraciones
* Posibles mejoras
* Autor

⸻

📌 Descripción del proyecto

EMOTIA nace como una propuesta tecnológica enfocada en el acompañamiento emocional y el bienestar personal.

A través de una interfaz conversacional en Telegram, los usuarios pueden expresar cómo se sienten, recibir mensajes de orientación y escuchar consejos mediante audios generados automáticamente.

El bot también incorpora actividades interactivas que permiten fortalecer la memoria, la concentración y la creatividad mediante dinámicas sencillas.

Su diseño utiliza botones, emojis, mensajes y una mascota virtual para ofrecer una experiencia amigable y fácil de utilizar.

🎯 Objetivos

Objetivo general

Desarrollar un bot interactivo en Telegram que proporcione acompañamiento emocional mediante consejos personalizados, respuestas de voz y actividades recreativas.

Objetivos específicos

* Identificar estados emocionales mediante palabras clave.
* Proporcionar consejos relacionados con diferentes estados de ánimo.
* Generar respuestas de voz en español.
* Implementar minijuegos interactivos.
* Registrar el progreso de cada usuario mediante una base de datos.
* Incorporar recompensas, niveles e insignias para incentivar la participación.

⸻

✨ Características principales

Funcionalidad	Descripción
💌 Acompañamiento emocional	Reconoce cinco estados de ánimo: alegría, tristeza, estrés, enojo y calma.
🔊 Respuestas por voz	Genera audios con una voz en español colombiano.
💬 Detección por palabras clave	Identifica expresiones relacionadas con estados emocionales.
🎮 Minijuegos	Incluye cinco actividades interactivas.
⭐ Sistema de recompensas	Otorga estrellas al completar actividades.
📊 Perfil de usuario	Permite consultar estrellas, juegos completados y nivel.
🏅 Insignias	Desbloquea reconocimientos según el progreso.
🎁 Regalo diario	Entrega 10 estrellas una vez al día.
🤖 Presentación interactiva	Permite conocer las funciones y características de EMOTIA.

🎮 Minijuegos disponibles

EMOTIA cuenta con cinco minijuegos diseñados para ofrecer entretenimiento e interacción:

1. Memoria de corazones: consiste en encontrar cuatro parejas de tarjetas iguales.
2. Sigue el patrón: permite memorizar y repetir secuencias de emojis.
3. Palabras mágicas: consiste en ordenar letras para descubrir palabras.
4. Crea una historia: presenta situaciones en las que el usuario elige cómo continúa la historia.
5. Jardín de calma: permite cuidar y hacer crecer un jardín mediante diferentes acciones.

Cada juego completado otorga una cantidad de estrellas que se acumulan en el perfil del usuario.

⭐ Sistema de recompensas y progreso

EMOTIA incorpora un sistema de gamificación que permite registrar la participación de los usuarios mediante estrellas, niveles e insignias.

Insignias disponibles:

* 🌱 Primer juego: por completar 1 juego.
* ✨ Exploradora emocional: por completar 3 juegos.
* 💜 Amiga de EMOTIA: por completar 7 juegos.
* 🏆 Estrella emocional: por completar 15 juegos.

También cuenta con un regalo diario que permite reclamar 10 estrellas una vez al día.

⸻

🛠️ Tecnologías utilizadas

Tecnología	Función
Python	Lenguaje principal de programación.
Telegram Bot API	Comunicación e interacción con los usuarios.
python-telegram-bot	Administración de comandos, mensajes y botones interactivos.
Edge TTS	Generación de audios a partir de texto.
SQLite	Almacenamiento de usuarios, estadísticas y registros.
asyncio	Ejecución de operaciones asíncronas.
HTML	Interpretación y manejo de caracteres especiales en mensajes.

Dependencias principales

Las dependencias necesarias para ejecutar el proyecto se encuentran en el archivo requirements.txt.

* python-telegram-bot>=21,<23
* edge-tts>=7,<9

⸻

💻 Requisitos previos

Para ejecutar EMOTIA se necesita:

* Python instalado.
* Una cuenta de Telegram.
* Un bot creado mediante BotFather.
* Conexión a Internet.
* Git instalado para clonar el repositorio.

⸻

📦 Instalación

1. Clonar el repositorio

Abrir una terminal y ejecutar:

git clone https://github.com/jbs2507/Emotia.git

2. Ingresar a la carpeta del proyecto

cd Emotia

3. Crear un entorno virtual

Windows:

python -m venv .venv

Activar el entorno:

.venv\Scripts\activate

Linux / macOS:

python3 -m venv .venv

Activar el entorno:

source .venv/bin/activate

4. Instalar las dependencias

pip install -r requirements.txt

⸻

⚙️ Configuración

1. Crear el bot en Telegram

Para utilizar EMOTIA es necesario crear un bot mediante Telegram.

1. Abrir Telegram.
2. Buscar el usuario oficial @BotFather.
3. Enviar el comando /newbot.
4. Asignar un nombre al bot.
5. Configurar un nombre de usuario.
6. Guardar el token proporcionado.

2. Configurar el token de Telegram

El proyecto utiliza una variable de entorno llamada TELEGRAM_BOT_TOKEN para establecer la conexión con Telegram.

Windows PowerShell:

$env:TELEGRAM_BOT_TOKEN="TU_TOKEN_DE_TELEGRAM"

Linux / macOS:

export TELEGRAM_BOT_TOKEN="TU_TOKEN_DE_TELEGRAM"

Importante: El token es privado y no debe publicarse ni compartirse en repositorios públicos.

⸻

🚀 Ejecución

Después de instalar las dependencias y configurar el token, ejecutar el archivo principal:

python bot.py

Si la configuración es correcta, aparecerá el siguiente mensaje:

EMOTIA listo. Abre Telegram y escribe /start.

Posteriormente:

1. Abrir Telegram.
2. Buscar el bot mediante su nombre de usuario.
3. Ejecutar el comando /start.
4. Escuchar la presentación de EMOTIA.
5. Acceder al menú principal.
6. Explorar las funcionalidades disponibles.

⸻

🤖 Comandos disponibles

Comando	Función
/start	Inicia EMOTIA y muestra la presentación.
/menu	Abre el menú principal.
/presentacion	Reproduce la presentación completa.
/emocion	Permite seleccionar un estado de ánimo.
/voz	Reproduce nuevamente el consejo de voz.
/jugar	Abre el menú de minijuegos.
/perfil	Permite consultar el perfil y progreso del usuario.
/regalo	Permite reclamar el regalo diario.
/ayuda	Muestra la guía de utilización.

⸻

🔄 Funcionamiento del bot

El funcionamiento general de EMOTIA se desarrolla mediante los siguientes pasos:

1. Inicio: el usuario ejecuta el comando /start y recibe la presentación del bot.

2. Presentación: EMOTIA genera un audio con su presentación y permite acceder al menú principal.

3. Interacción: el usuario selecciona una de las funcionalidades disponibles.

4. Acompañamiento emocional: el usuario puede seleccionar una emoción o escribir un mensaje. El sistema identifica palabras clave y selecciona un consejo correspondiente.

5. Generación de voz: el texto del consejo se convierte en un archivo de audio MP3 mediante Edge TTS.

6. Entretenimiento: el usuario puede participar en cualquiera de los cinco minijuegos disponibles.

7. Registro del progreso: al completar un juego, el sistema registra las estrellas obtenidas y actualiza las estadísticas del usuario.

8. Recompensas: el usuario puede consultar sus niveles, insignias y reclamar el regalo diario.

⸻

🗄️ Base de datos

EMOTIA utiliza SQLite para almacenar la información necesaria para el funcionamiento del sistema.

La base de datos se crea automáticamente cuando se ejecuta el bot.

Tablas principales

Tabla	Descripción
users	Almacena el identificador del usuario, sus estrellas y juegos completados.
results	Registra los resultados obtenidos en los minijuegos.
advice_history	Guarda el historial de consejos entregados según el estado emocional.
daily_gifts	Registra los regalos diarios reclamados por cada usuario.

La información se almacena en el archivo emotia.sqlite3.

⸻

📁 Estructura del proyecto

Emotia/
│
├── bot.py
│   └── Código principal del bot.
│
├── requirements.txt
│   └── Dependencias necesarias para ejecutar el proyecto.
│
├── assets/
│   └── emotia.png
│       └── Imagen de la mascota del bot.
│
├── README.md
│   └── Documentación del proyecto.
│
└── emotia.sqlite3
    └── Base de datos generada durante la ejecución.

La estructura anterior representa los componentes principales del proyecto. La base de datos se genera automáticamente y no es necesario crearla manualmente.

⸻

⚠️ Consideraciones

* Es necesario tener conexión a Internet para utilizar Telegram y generar los audios mediante Edge TTS.
* El bot necesita un token válido de Telegram para funcionar.
* La identificación de emociones se realiza mediante palabras clave y reglas definidas en el código; no utiliza un modelo de inteligencia artificial entrenado.
* Los consejos proporcionados son orientativos y no reemplazan el acompañamiento de personas de confianza ni la atención de profesionales.
* La base de datos se genera automáticamente al ejecutar el proyecto.
* Se recomienda mantener las credenciales privadas y evitar subir archivos sensibles al repositorio.

⸻

🔮 Posibles mejoras

Entre las mejoras que se pueden implementar en futuras versiones se encuentran:

* Incorporar modelos de inteligencia artificial para mejorar la identificación de emociones.
* Agregar nuevos minijuegos y actividades interactivas.
* Implementar nuevas voces y opciones de personalización.
* Incorporar estadísticas más detalladas sobre el progreso de los usuarios.
* Mejorar el sistema de seguimiento emocional.
* Agregar nuevas funcionalidades de interacción y personalización.

⸻

👩‍💻 Autor

Desarrollado por: Juliana Betancur Salcedo.

Proyecto: EMOTIA – Acompañante Emocional Interactivo para Telegram.

Repositorio en GitHub:

https://github.com/jbs2507/Emotia

⸻

💜 EMOTIA: un espacio para expresar emociones, descubrir nuevas experiencias y disfrutar de pequeños momentos.
