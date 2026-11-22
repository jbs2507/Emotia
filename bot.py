"""EMOTIA: robot, juegos variados y consejos de voz para Telegram, sin web app."""
import asyncio
import logging
import os
import random
import sqlite3
import tempfile
import html
import uuid
from datetime import date
from pathlib import Path

from telegram import InlineKeyboardButton as B, InlineKeyboardMarkup as K, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

BASE = Path(__file__).resolve().parent
DB = BASE / 'emotia.sqlite3'
ROBOT = BASE / 'assets' / 'emotia.png'
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)

MOODS = {'alegria':'😄 Alegría', 'tristeza':'💙 Tristeza', 'estres':'🌪️ Estrés', 'enojo':'🔥 Enojo', 'calma':'🌿 Calma'}
ADVICE = {'alegria': ['¡Qué bonito que hoy haya una chispa de alegría! Haz una pequeña pausa para disfrutarla. Puedes '
             'guardar ese recuerdo en una nota, una canción o una foto. Los días felices también merecen ser '
             'recordados.',
             'Hay alegrías enormes y otras diminutas, como una conversación bonita o una canción inesperada. '
             'No necesitas hacer algo extraordinario: disfrutar lo sencillo también cuenta.',
             'Si hoy te sientes con energía, compártela de una forma que te guste: un mensaje amable, una '
             'idea creativa o una actividad divertida. Y si prefieres descansar, también está bien.',
             '¿Sabes qué es especial de este momento? Que lo estás reconociendo. A veces pasamos tan rápido '
             'por los días que olvidamos celebrar lo bueno. Hoy regálate unos segundos para apreciarlo.',
             'La alegría no tiene que durar todo el día para ser real. Disfruta este ratito tal como es, sin '
             'exigirte mantener la sonrisa a cada instante.',
             'Si algo te salió bien, por pequeño que parezca, reconoce tu esfuerzo. No necesitas compararte '
             'con nadie para sentir orgullo de tu propio camino.',
             'Prueba hacer una mini lista de tres cosas que te gustaron de hoy. Tal vez descubras detalles '
             'que te gustaría repetir mañana.',
             '¿Y si conviertes esta buena energía en algo creativo? Dibuja, canta, escribe o inventa una '
             'pequeña historia. Lo importante es disfrutar, no hacerlo perfecto.',
             'Puedes compartir tu alegría con alguien de confianza, pero también guardarla como un tesoro '
             'personal. Las dos formas son valiosas.',
             'Hoy tu corazón encontró un momento agradable. Ojalá puedas saborearlo con calma, sin '
             'convertirlo en otra tarea pendiente.'],
 'tristeza': ['Hay días en los que todo se siente un poquito más pesado. No tienes que fingir estar bien. '
              'Busca algo sencillo que te dé comodidad: una bebida, una manta o una canción tranquila. Un '
              'paso pequeño también es cuidado.',
              'Si hoy las palabras no salen, no pasa nada. Puedes escribir una frase sobre cómo te sientes o '
              'dibujar algo sin preocuparte por el resultado. A veces expresar un poquito ayuda a ordenar lo '
              'que llevamos dentro.',
              'No tienes que resolver todo hoy. Piensa en una sola cosa amable que puedas hacer por ti: '
              'descansar un rato, comer algo que disfrutes o hablar con alguien de confianza.',
              'Sentirse triste no significa que el día esté perdido. Tal vez haya espacio para un momento '
              'suave: mirar el cielo, escuchar música o sentarte en un lugar tranquilo.',
              'Si te gustaría compañía, podrías escribirle a alguien: «Hoy no me siento muy bien, ¿podemos '
              'hablar un rato?». Pedir escucha es una forma valiente de cuidarte.',
              'No hace falta encontrar una explicación perfecta para lo que sientes. Puedes reconocerlo con '
              'una frase sencilla: «Hoy estoy triste y necesito un poco de paciencia».',
              'A veces lo mejor que puedes ofrecerte es bajar el ritmo. Elige una actividad tranquila que te '
              'guste y date permiso de hacerla sin prisas.',
              'Si algo no salió como esperabas, recuerda que una experiencia difícil no define quién eres. '
              'Puedes aprender de ella cuando tengas más calma.',
              'Imagínate qué le dirías con cariño a una amistad que está pasando un día complicado. Quizás '
              'algunas de esas palabras también puedan acompañarte hoy.',
              'No tienes que cargar con todo en silencio. Si esta tristeza se mantiene o te supera, hablar '
              'con una persona adulta de confianza o un profesional puede ayudarte a sentirte acompañada.'],
 'estres': ['Cuando tienes muchas cosas en la cabeza, prueba elegir solo la siguiente. No todo necesita '
            'resolverse al mismo tiempo. Una tarea pequeña y posible es un buen comienzo.',
            'Antes de continuar, mira a tu alrededor y nombra tres cosas que puedas ver. Es una forma '
            'sencilla de volver al presente cuando los pensamientos van muy rápido.',
            'Si tu lista de pendientes parece interminable, escribe todo en un papel y marca una sola '
            'prioridad. Lo demás puede esperar su turno.',
            'No necesitas hacerlo perfecto para hacerlo bien. A veces avanzar un poquito, con pausas, vale '
            'más que exigirte terminar todo de una vez.',
            'Prueba una pausa de dos minutos: toma agua, cambia de posición y descansa la vista. Luego '
            'decide cuál será tu siguiente paso.',
            'Cuando algo te preocupa, separa lo que puedes hacer hoy de lo que no depende de ti. '
            'Concentrarte en lo primero puede darte más claridad.',
            'Si te sientes saturada, puedes pedir apoyo con una frase concreta: «¿Me ayudas a organizar '
            'esto?». Compartir una tarea no te hace menos capaz.',
            'Está bien cambiar de plan cuando necesitas más tiempo. Cuidar tu energía también forma parte de '
            'aprender a organizarte.',
            'No tienes que responder cada mensaje inmediatamente. Si puedes, reserva un ratito sin '
            'notificaciones para terminar una sola cosa.',
            '¿Qué sería suficiente por hoy, aunque no sea perfecto? Elegir una meta realista puede aliviar '
            'la presión y dejar espacio para descansar.'],
 'enojo': ['El enojo puede avisarte que algo te importa o que un límite fue cruzado. Antes de responder, '
           'busca un momento para ordenar tus ideas y decidir qué quieres expresar.',
           'Si estás molesta, no tienes que resolver la conversación en este instante. Puedes decir: '
           '«Necesito un momento y luego hablamos». Tomar distancia breve también es comunicarse.',
           'Prueba distinguir entre lo que pasó, lo que sentiste y lo que necesitas. Decir esas tres cosas '
           'con calma puede ayudarte a que te entiendan.',
           'Es válido sentir rabia; lo importante es cómo eliges actuar. Si puedes, aléjate un rato del '
           'conflicto y vuelve cuando te sientas preparada.',
           'A veces el enojo esconde cansancio o frustración. Pregúntate con curiosidad: «¿Qué necesito '
           'ahora mismo?». Tal vez sea descanso, apoyo o espacio.',
           'No tienes que ganar una discusión para que tus sentimientos sean importantes. Expresar tu punto '
           'con respeto también es una forma de fortaleza.',
           'Si escribes un mensaje mientras estás muy molesta, puedes guardarlo como borrador y revisarlo '
           'después. Así eliges las palabras con más claridad.',
           'Puedes poner límites con amabilidad y firmeza: «Eso me incomodó y prefiero que no vuelva a '
           'pasar». Tu voz merece espacio.',
           'El enojo no te convierte en una mala persona. Date un momento para entender qué ocurrió antes de '
           'decidir qué hacer.',
           'Busca una actividad que te ayude a despejarte, como dibujar, caminar tranquilamente o escuchar '
           'música. Después será más fácil conversar.'],
 'calma': ['Qué agradable encontrar un ratito de tranquilidad. No tienes que llenarlo de tareas. Puedes '
           'simplemente disfrutarlo y notar algo bonito de tu alrededor.',
           'Si hoy estás en calma, observa qué te ayudó a llegar aquí. Quizás una rutina, una persona o un '
           'espacio. Reconocerlo puede servirte en otros días.',
           'La tranquilidad también merece celebrarse. Regálate unos minutos sin prisas, sin sentir que '
           'debes aprovechar cada segundo.',
           '¿Te gustaría guardar este momento? Escribe una palabra que lo describa y una cosa que te hizo '
           'sentir bien. Puede convertirse en un recuerdo especial.',
           'Un día tranquilo puede ser una buena oportunidad para crear: colorear, leer, escuchar música o '
           'cuidar una planta.',
           'No todos los días necesitan grandes aventuras. A veces una tarde sencilla es exactamente lo que '
           'necesitamos.',
           'Piensa en un pequeño detalle que agradeces de hoy. Puede ser tan simple como una conversación '
           'amable o un momento de silencio.',
           'Puedes compartir tu calma con un gesto bonito hacia alguien: escucharle, enviar un saludo o '
           'dedicarle unos minutos.',
           'Si te apetece, organiza un rincón agradable para ti. Un espacio sencillo y cómodo puede hacer '
           'que el descanso se sienta especial.',
           'Quédate con esta idea: descansar no es perder el tiempo. También es una forma de cuidar tu '
           'bienestar.']}

MEMORY_ICONS = ['💙','💜','🌟','🌸']
SEQUENCES = [(['🌱','🌷','🌻'],'🌻'), (['☁️','🌦️','🌈'],'🌈'), (['💜','⭐','💜'],'💜'), (['🌙','⭐','🌙'],'🌙')]
WORDS = [('C','A','L','M','A'),('A','M','O','R'),('P','A','Z')]
STORIES = [
 ('Una amiga está callada y parece triste. ¿Cómo continúa la historia?', [('Le pregunto si quiere hablar','💙 A veces escuchar es el mejor regalo.'),('Le doy espacio y le digo que estoy disponible','💙 Respetar su espacio también es acompañar.')]),
 ('Un compañero está nervioso antes de presentar. ¿Qué le dices?', [('Podemos practicar un momento','🌟 ¡Una idea de apoyo!'),('Estoy aquí para animarte','🌟 ¡Qué bonito acompañarlo!')]),
 ('Hoy tuviste un día difícil. ¿Qué pequeño final eliges?', [('Pedir un rato de descanso','🌿 Descansar es válido.'),('Hablar con alguien de confianza','🌿 Compartir lo que sientes puede ayudar.')])
]

def db():
 c=sqlite3.connect(DB)
 c.execute('CREATE TABLE IF NOT EXISTS users (uid INTEGER PRIMARY KEY, stars INTEGER DEFAULT 0, games INTEGER DEFAULT 0)')
 c.execute('CREATE TABLE IF NOT EXISTS results (uid INTEGER, game TEXT, stars INTEGER, created TEXT DEFAULT CURRENT_TIMESTAMP)')
 c.execute('CREATE TABLE IF NOT EXISTS advice_history (uid INTEGER, mood TEXT, advice_index INTEGER, created TEXT DEFAULT CURRENT_TIMESTAMP)')
 c.execute('CREATE TABLE IF NOT EXISTS daily_gifts (uid INTEGER, day TEXT, PRIMARY KEY(uid,day))')
 c.commit()
 return c

def ensure(uid):
 with db() as c:c.execute('INSERT OR IGNORE INTO users(uid) VALUES (?)',(uid,))

def stats(uid):
 ensure(uid)
 with db() as c:return c.execute('SELECT stars,games FROM users WHERE uid=?',(uid,)).fetchone()

def award(uid,game,amount):
 ensure(uid)
 with db() as c:
  c.execute('UPDATE users SET stars=stars+?, games=games+1 WHERE uid=?',(amount,uid))
  c.execute('INSERT INTO results(uid,game,stars) VALUES(?,?,?)',(uid,game,amount))

def next_advice(uid, mood):
    ensure(uid)
    with db() as conn:
        used = {row[0] for row in conn.execute(
            'SELECT advice_index FROM advice_history WHERE uid=? AND mood=?', (uid,mood))}
        options = [i for i in range(len(ADVICE[mood])) if i not in used]
        if not options:
            conn.execute('DELETE FROM advice_history WHERE uid=? AND mood=?',(uid,mood))
            options = list(range(len(ADVICE[mood])))
        i = random.choice(options)
        conn.execute('INSERT INTO advice_history(uid,mood,advice_index) VALUES (?,?,?)',(uid,mood,i))
    return ADVICE[mood][i]

def kb(rows):return K([[B(text=label,callback_data=action) for label,action in row] for row in rows])
def home():return kb([[('💌 ¿Cómo me siento?','moods')],[('🎮 Mundo de juegos','games'),('⭐ Mi progreso','stats')],[('🎁 Regalo del día','daily'),('🏅 Insignias','badges')],[('🤖 Conóceme','intro'),('🆘 Ayuda','help')]])
def mood_buttons():return kb([[(name,'mood:'+m)] for m,name in MOODS.items()]+[[('🏠 Menú principal','home')]])
def games_menu():return kb([[('🃏 Memoria de corazones','game:memory')],[('✨ Sigue el patrón','game:pattern')],[('🔤 Palabras mágicas','game:word')],[('📖 Crea una historia','game:story')],[('🌿 Jardín de calma','game:garden')],[('🏠 Menú principal','home')]])

async def mascot(message,caption,reply_markup=None):
 if ROBOT.exists():
  with ROBOT.open('rb') as image:
   await message.reply_photo(image,caption=caption,reply_markup=reply_markup)
 else:await message.reply_text(caption,reply_markup=reply_markup)

INTRO_STEPS = [
 ('✨ CAPÍTULO 1 · HOLA, SOY EMOTIA 💜',
  '¡Qué emoción conocerte! Soy EMOTIA, un robotito que vive entre estrellas y emociones. 🤖🌷\n\nNo tengo una varita mágica para arreglarlo todo, pero sí ideas bonitas, juegos y un espacio para expresarte.\n\n¿Quieres descubrir mis superpoderes?'),
 ('💌 CAPÍTULO 2 · TUS EMOCIONES IMPORTAN',
  'Aquí caben los días felices, los complicados y los que no sabes explicar. 🌈\n\nPuedes escoger cómo te sientes y recibir un consejo distinto. También puedes escribir con tus propias palabras.\n\n¡Y sí! Puedo leerte mis consejos en voz alta. 🔊'),
 ('🎮 CAPÍTULO 3 · EL UNIVERSO DE JUEGOS',
  'Tenemos cartas de memoria, patrones, palabras, historias y un jardín que crece con tus decisiones. 🌸\n\nCada juego terminado suma estrellas para subir de nivel y desbloquear insignias. ⭐'),
 ('🚀 CAPÍTULO 4 · ¡COMIENZA TU AVENTURA!',
  'Tu historia en EMOTIA comienza ahora. Puedes explorar sin prisas, pedir otro consejo cuando quieras y regresar al menú con /menu.\n\n¿Empezamos con una emoción o con un juego? 💜')
]

async def send_spoken(message, spoken, buttons=None, title='EMOTIA 💜'):
    """Audio MP3 reproducible dentro de Telegram; nunca publica el guion como texto."""
    try:
        import edge_tts
        with tempfile.TemporaryDirectory() as tmp:
            mp3=Path(tmp)/'emotia.mp3'
            await asyncio.wait_for(edge_tts.Communicate(
                spoken, voice='es-CO-SalomeNeural', rate='-8%', pitch='+0Hz'
            ).save(str(mp3)), timeout=50)
            if not mp3.exists() or mp3.stat().st_size < 500:
                raise RuntimeError('El audio no se generó')
            with mp3.open('rb') as audio:
                await message.reply_audio(audio, title=title, performer='EMOTIA',
                                          reply_markup=buttons)
        return True
    except Exception as exc:
        logging.warning('No se pudo crear el audio (%s): %s', type(exc).__name__, str(exc)[:120])
        await message.reply_text('🔊 No pude generar el audio por ahora. Revisa Internet y toca Reintentar.',
                                 reply_markup=buttons)
        return False

async def introduction(message):
    """Una única presentación hablada, seguida del botón para abrir el menú."""
    spoken = ' '.join(body.replace('\n', ' ') for _, body in INTRO_STEPS)
    buttons = kb([[('🏠 Abrir menú principal', 'finish_intro')],
                  [('🔁 Volver a escuchar', 'intro')]])
    await send_spoken(message, spoken, buttons, title='EMOTIA · Mi presentación completa')

async def show_home(message, uid):
    """El menú se muestra después de terminar la presentación."""
    stars, games = stats(uid)
    await mascot(message,
                 f'🏠💜 ¡Bienvenido al universo EMOTIA!\n⭐ {stars} estrellas · 🚀 Nivel {1+stars//100}\n\nElige qué quieres hacer:',
                 home())

async def start(u:Update,c:ContextTypes.DEFAULT_TYPE):
    """/start muestra únicamente el botón de presentación, nunca el menú."""
    uid = u.effective_user.id
    ensure(uid)
    await mascot(u.effective_message,
                 '🤖💜 ¡Hola! Soy EMOTIA.\n\n🎧 Tengo algo especial que contarte. Pulsa el botón para escuchar mi presentación.',
                 kb([[('🎙️ Escuchar mi presentación completa', 'intro')]]))

async def menu_command(u:Update,c:ContextTypes.DEFAULT_TYPE):
    await show_home(u.effective_message, u.effective_user.id)

async def daily_gift(message, uid):
 ensure(uid)
 today=date.today().isoformat()
 with db() as conn:
  cursor=conn.execute('INSERT OR IGNORE INTO daily_gifts(uid,day) VALUES (?,?)',(uid,today))
  granted=cursor.rowcount==1
  if granted:
   conn.execute('UPDATE users SET stars=stars+? WHERE uid=?',(10,uid))
 if granted:
  await message.reply_text('🎁✨ ¡SORPRESA DEL DÍA!\n\n¡Encontraste una cajita de estrellas! ⭐ +10 estrellas para tu colección.\n\n💜 Tu mini reto opcional: descubre algo agradable de hoy, aunque sea muy pequeñito.',reply_markup=home())
 else:
  await message.reply_text('🌷 Ya abriste tu regalo de hoy. ¡Qué bueno que volviste! Mañana habrá otra cajita de estrellas. 💜',reply_markup=home())

async def show_help(message):
 await message.reply_text('🧭✨ GUÍA DE EMOTIA\n\n💌 *Emociones:* elige cómo te sientes y recibe un consejo.\n🔊 *Voz:* los consejos y la presentación llegan directamente como audio.\n✨ *Otro consejo:* recibes un audio distinto, sin repetirlo enseguida.\n🎮 *Juegos:* completa minijuegos para ganar estrellas.\n🎁 *Regalo del día:* recibe una sorpresa una vez al día.\n⭐ *Progreso:* consulta tu nivel e insignias.\n\nComandos: /start · /menu · /emocion · /jugar · /voz · /perfil · /ayuda\n\n💜 Soy un acompañante digital, no reemplazo el apoyo de personas de confianza o profesionales.',parse_mode='Markdown',reply_markup=home())

async def show_games(message):
 await mascot(message,'🎮✨ ¡BIENVENIDA A LA ARCADE EMOTIA!\n\nCinco aventuras con botones, sorpresas y estrellas. No tienes que enviar fotos ni tareas. ¡Elige una!',games_menu())

async def choose_mood(message):await message.reply_text('🤖💜 ¿Cómo está tu corazón hoy? No hay respuestas incorrectas.',reply_markup=mood_buttons())

def advice_controls():
    return kb([[('🔁 Escuchar otra vez','voice'), ('✨ Otro consejo','another')],
               [('💜 Cambiar emoción','moods'), ('🎮 Juegos','games')],
               [('🏠 Menú','home')]])

async def set_mood(message,c,mood):
    c.user_data['mood']=mood
    c.user_data['advice']=next_advice(message.chat.id,mood)
    await send_spoken(message, c.user_data['advice'], advice_controls(),
                      title=f'EMOTIA · {MOODS[mood]}')

async def voice(u,c):
    mood=c.user_data.get('mood')
    if not mood:
        await choose_mood(u.effective_message)
        return
    message=c.user_data.get('advice')
    if not message:
        message=next_advice(u.effective_chat.id,mood)
        c.user_data['advice']=message
    await send_spoken(u.effective_message, message, advice_controls(),
                      title=f'EMOTIA · {MOODS[mood]}')

def new_session(c,kind):
 sid=uuid.uuid4().hex[:7]
 c.user_data['session']={'id':sid,'kind':kind,'step':0,'points':0}
 return c.user_data['session']

def current(c,sid,kind=None):
 s=c.user_data.get('session')
 return s if s and s['id']==sid and (kind is None or s['kind']==kind) else None

async def launch(message,c,kind):
 s=new_session(c,kind)
 if kind=='memory':
  cards=MEMORY_ICONS*2;random.shuffle(cards)
  s.update(cards=cards,shown=[],matched=[],tries=0)
  await mascot(message,'🤖🃏 MEMORIA DE CORAZONES\nEncuentra las 4 parejas. ¡Toca dos tarjetas para descubrirlas!')
 elif kind=='pattern':
  seq=random.choice(SEQUENCES)[0];s.update(seq=seq,position=0,round=0)
  await mascot(message,'🤖✨ SIGUE EL PATRÓN\nMira la secuencia y toca los emojis en el mismo orden. ¡Cada ronda es un poquito más larga!')
 elif kind=='word':
  word=random.choice(WORDS);s.update(target=''.join(word),letters=list(word),picked=[],used=[])
  await mascot(message,'🤖🔤 PALABRAS MÁGICAS\nOrdena las letras para formar una palabra bonita. ¡Puedes probar de nuevo!')
 elif kind=='story':
  s.update(story=random.sample(STORIES,len(STORIES)))
  await mascot(message,'🤖📖 CREA TU HISTORIA\nTú decides cómo continúa. No hay respuestas malas: ¡exploraremos distintas maneras de acompañar!')
 elif kind=='garden':
  s.update(garden=0)
  await mascot(message,'🤖🌿 JARDÍN DE CALMA\nHaremos crecer un jardín tocando botones. Puedes seguir tu propio ritmo y parar cuando quieras.')
 await render(message,c)

async def render(message,c):
 s=c.user_data.get('session')
 if not s:return
 sid=s['id'];kind=s['kind'];step=s['step']
 if kind=='memory':
  lines=[]
  for i,icon in enumerate(s['cards']):
   if i in s['matched'] or i in s['shown']: label=icon
   else:label='❔'
   lines.append((label,f'p:{sid}:{i}'))
  board=kb([lines[i:i+4] for i in range(0,8,4)]+[[('🚪 Salir','games')]])
  await message.reply_text(f'🤖🃏 Parejas encontradas: {len(s["matched"])//2}/4\nIntentos: {s["tries"]}',reply_markup=board)
 elif kind=='pattern':
  length=min(2+s['round'],3)
  seq=s['seq'][:length]
  await message.reply_text(f'🤖✨ Ronda {s["round"]+1}/2\nMemoriza: {"  ".join(seq)}\n\nAhora toca el emoji número {s["position"]+1}:',reply_markup=kb([[ (x,f'p:{sid}:{x}') for x in dict.fromkeys(['🌱','🌷','🌻','☁️','🌦️','🌈','💜','⭐','🌙'])][i:i+3] for i in range(0,9,3)]+[[('🚪 Salir','games')]]))
 elif kind=='word':
  letters=s['letters'];used=s['used']
  buttons=[(f'{letter}',f'p:{sid}:{i}') for i,letter in enumerate(letters) if i not in used]
  await message.reply_text(f'🤖🔤 Arma la palabra ({len(letters)} letras)\n\n✨ {" ".join(s["picked"]) or "_ "*len(letters)}',reply_markup=kb([buttons[i:i+3] for i in range(0,len(buttons),3)]+[[('↩️ Reiniciar palabra',f'p:{sid}:reset'),('🚪 Salir','games')]]))
 elif kind=='story':
  text,options=s['story'][step]
  await message.reply_text(f'🤖📖 Escena {step+1}/3\n\n{text}',reply_markup=kb([[(name,f'p:{sid}:{i}')] for i,(name,_) in enumerate(options)]+[[('🚪 Salir','games')]]))
 elif kind=='garden':
  stages=['🟫 🟫 🟫','🌱 🌱 🌱','🌷 🌱 🌷','🌸 🌷 🌸','🌼 🌸 🌼']
  await message.reply_text(f'🤖🌿 Tu jardín: {stages[s["garden"]]}\n\nElige una acción tranquila para cuidarlo.\nPaso {s["garden"]}/4',reply_markup=kb([[('💧 Regar',f'p:{sid}:water'),('☀️ Dar luz',f'p:{sid}:sun')],[('💜 Darle cariño',f'p:{sid}:care')],[('🚪 Salir','games')]]))

async def finish(message,c,uid):
 s=c.user_data.pop('session',None)
 if not s:return
 stars={'memory':40,'pattern':30,'word':25,'story':30,'garden':25}[s['kind']]
 award(uid,s['kind'],stars)
 total,games=stats(uid)
 await mascot(message,f'🤖🎉 ¡LO LOGRASTE!\n\n⭐ +{stars} estrellas\n💜 Total: {total} estrellas\n🚀 Nivel {1+total//100}\n🏅 Juegos completados: {games}\n\n¡Gracias por jugar conmigo!',kb([[('🎮 Otro juego','games'),('⭐ Mi progreso','stats')]]))

async def play(message,c,uid,sid,value):
 s=current(c,sid)
 if not s:return
 kind=s['kind']
 if kind=='memory':
  try:i=int(value)
  except ValueError:return
  if i not in range(8) or i in s['matched'] or i in s['shown']:return
  s['shown'].append(i)
  if len(s['shown'])==2:
   a,b=s['shown'];s['tries']+=1
   if s['cards'][a]==s['cards'][b]:
    s['matched'].extend([a,b]);s['shown']=[]
    await message.reply_text('🤖💜 ¡Encontraste una pareja! ✨')
   else:
    await message.reply_text(f'🤖🔍 Descubriste {s["cards"][a]} y {s["cards"][b]}. ¡No son pareja! Vamos otra vez.')
    s['shown']=[]
  if len(s['matched'])==8:await finish(message,c,uid)
  else:await render(message,c)
 elif kind=='pattern':
  seq=s['seq'][:2+s['round']]
  if value==seq[s['position']]:
   s['position']+=1
   if s['position']==len(seq):
    s['round']+=1;s['position']=0
    if s['round']==2:await finish(message,c,uid);return
    await message.reply_text('🤖🌟 ¡Memoria brillante! Pasamos a una secuencia más larga.')
  else:
   s['position']=0
   await message.reply_text('🤖💜 Casi. No pasa nada: ¡mira la secuencia e inténtalo de nuevo!')
  await render(message,c)
 elif kind=='word':
  if value=='reset':s['picked']=[];s['used']=[]
  else:
   try:i=int(value)
   except ValueError:return
   if i not in range(len(s['letters'])) or i in s['used']:return
   s['used'].append(i);s['picked'].append(s['letters'][i])
   if len(s['picked'])==len(s['letters']):
    if ''.join(s['picked'])==s['target']:
     await message.reply_text('🤖✨ ¡Palabra descubierta! '+s['target']+' 💜')
     await finish(message,c,uid);return
    await message.reply_text('🤖💜 Esa combinación no es la palabra secreta. ¡Puedes volver a probar!')
    s['picked']=[];s['used']=[]
  await render(message,c)
 elif kind=='story':
  try:i=int(value)
  except ValueError:return
  options=s['story'][s['step']][1]
  if i not in range(len(options)):return
  await message.reply_text('🤖💌 '+options[i][1])
  s['step']+=1
  if s['step']==3:await finish(message,c,uid)
  else:await render(message,c)
 elif kind=='garden':
  if value not in ('water','sun','care'):return
  s['garden']+=1
  messages={'water':'💧 ¡Tus plantitas recibieron agua!','sun':'☀️ ¡Un poquito de luz para el jardín!','care':'💜 ¡Un gesto de cariño para tu jardín!'}
  await message.reply_text('🤖 '+messages[value])
  if s['garden']>=4:await finish(message,c,uid)
  else:await render(message,c)

async def cb(u:Update,c:ContextTypes.DEFAULT_TYPE):
 q=u.callback_query;await q.answer();d=q.data;uid=q.from_user.id
 ensure(uid)
 if d=='home':await show_home(q.message,uid)
 elif d=='finish_intro':await show_home(q.message,uid)
 elif d=='games':c.user_data.pop('session',None);await show_games(q.message)
 elif d=='moods':await choose_mood(q.message)
 elif d in ('robot','intro') or d.startswith('intro:'):await introduction(q.message)
 elif d=='daily':await daily_gift(q.message,uid)
 elif d=='help':await show_help(q.message)
 elif d.startswith('mood:'):
  mood=d.split(':',1)[1]
  if mood in MOODS:await set_mood(q.message,c,mood)
 elif d.startswith('game:'):
  kind=d.split(':',1)[1]
  if kind in ('memory','pattern','word','story','garden'):await launch(q.message,c,kind)
 elif d.startswith('p:'):
  _,sid,value=d.split(':',2)
  # Clear old keyboard to avoid repeated clicks on the same turn.
  if not current(c,sid):return
  try:await q.edit_message_reply_markup(reply_markup=None)
  except Exception:pass
  await play(q.message,c,uid,sid,value)
 elif d=='voice':await voice(u,c)
 elif d=='another':
  mood=c.user_data.get('mood')
  if mood:await set_mood(q.message,c,mood)
  else:await choose_mood(q.message)
 elif d=='stats':
  stars,games=stats(uid)
  await q.message.reply_text(f'🌟 TU PERFIL EMOTIA 🌟\n\n⭐ Estrellas: {stars}\n🎮 Aventuras completadas: {games}\n🚀 Nivel: {1+stars//100}\n📈 Para el siguiente nivel: {100-(stars%100)} estrellas\n\n💜 Cada aventura cuenta.',reply_markup=home())
 elif d=='badges':
  _,games=stats(uid)
  labels=[(1,'🌱 Primer juego'),(3,'✨ Exploradora emocional'),(7,'💜 Amiga de EMOTIA'),(15,'🏆 Estrella emocional')]
  await q.message.reply_text('🏅✨ MI COLECCIÓN DE INSIGNIAS\n\n'+'\n'.join(('✅ ' if games>=n else '🔒 ')+name+f' — {n} juegos' for n,name in labels),reply_markup=home())

async def text_handler(u:Update,c:ContextTypes.DEFAULT_TYPE):
 t=(u.message.text or '').lower()
 words={'tristeza':['triste','desanim','llorar','sola'],'estres':['estres','nervios','ansios','preocup','agobi'],'enojo':['enoj','rabia','furia','molest'],'alegria':['feliz','alegre','content','emocionad'],'calma':['tranquil','calma','relajad']}
 mood=next((m for m,ws in words.items() if any(w in t for w in ws)),None)
 if mood:await set_mood(u.message,c,mood)
 else:await u.message.reply_text('🤖💜 Te leo. Puedes contarme cómo te sientes o elegir un juego para compartir un momento divertido.',reply_markup=home())

async def on_error(update,context):
 logging.error('Error del bot: %s',type(context.error).__name__)

def main():
 token=os.getenv('TELEGRAM_BOT_TOKEN','').strip()
 if not token:raise SystemExit('Falta TELEGRAM_BOT_TOKEN. Configúralo en PowerShell.')
 app=Application.builder().token(token).build()
 app.add_handler(CommandHandler('start',start))
 app.add_handler(CommandHandler('menu',menu_command))
 app.add_handler(CommandHandler('ayuda',lambda u,c:show_help(u.effective_message)))
 app.add_handler(CommandHandler('presentacion',lambda u,c:introduction(u.effective_message)))
 app.add_handler(CommandHandler('regalo',lambda u,c:daily_gift(u.effective_message,u.effective_user.id)))
 app.add_handler(CommandHandler('jugar',lambda u,c:show_games(u.effective_message)))
 app.add_handler(CommandHandler('voz',voice))
 app.add_handler(CommandHandler('perfil',lambda u,c:u.effective_message.reply_text('⭐ Para ver tu nivel y tus estrellas, abre /start y toca ⭐ Mi progreso.',reply_markup=home())))
 app.add_handler(CommandHandler('emocion',lambda u,c:choose_mood(u.effective_message)))
 app.add_handler(CallbackQueryHandler(cb))
 app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,text_handler))
 app.add_error_handler(on_error)
 print('EMOTIA listo. Abre Telegram y escribe /start.')
 app.run_polling(drop_pending_updates=True)

if __name__=='__main__':main()
