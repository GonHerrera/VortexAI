import json
import requests

import streamlit as st

# Initialize session state to store the conversation history
if "messages" not in st.session_state:
	mensaje_inicial = "Bienvenido a VortexAI su asistente en el proceso Pentagrowth. \nPara comenzar por favor indique el nombre de la organización con la que va a estar trabajando."
	st.session_state.messages = [{"sender": "VortexAI", "text": mensaje_inicial}]
	st.session_state.conversation_point = "carga_organizacion"
	st.session_state.context = {}

# Agregar API key:
GEMINI_KEY = ""
# Define the URL (make sure to include your actual API key at the end)
url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + GEMINI_KEY

# Define the headers
headers = {
    "Content-Type": "application/json"
}

def prompt_gemini(prompt: str) -> str:

  # Define the data payload
  data = {
      "contents": [
          {
              "role": "user",
              "parts": [
                  {"text": prompt}
              ]
          }
      ]
  }

  # Send the POST request
  response = requests.post(url, headers=headers, json=data)

  # Check if the request was successful
  if response.status_code == 200:
      # Parse the response JSON data
      response_data = response.json()
      # Print the response to verify
      return response_data['candidates'][0]['content']['parts'][0]['text']
  else:
    return None

def get_prompt(user_input: str = None) -> str:
	if st.session_state.conversation_point == "carga_organizacion":
		prompt = "En el siguiente texto se encuentra el nombre de una organización - devolvé solamente el nombre de la organización mencionada: '" + user_input + "'"
	elif st.session_state.conversation_point == "carga_pais":
		prompt = "En el siguiente texto se encuentra el país de la organización - devolvé solamente el nombre del país mencioando: '" + user_input + "'"
	elif st.session_state.conversation_point == "carga_tamanio":
		prompt = "En el siguiente texto se encuentra el tamaño de la organización - interpretalo entre las opciones micro, pequeña, mediana, grande - también podés incluir la cantidad aproximada de empleados - devolvé solo el restulado: '" + user_input + "'"
	elif st.session_state.conversation_point == "carga_industria":
		prompt = "En el siguiente texto se encuentra la industria de la organización - devolvé solamente el nombre de la industria mencioanda: '" + user_input + "'"
	elif st.session_state.conversation_point == "carga_sector":
		prompt = "En el siguiente texto se encuentra el sector de la organización - devolvé solamente el nombre del sector mencioando: '" + user_input + "'"
	elif st.session_state.conversation_point == "carga_servicios_inicial":
		prompt = "Eres un asistente o facilitador de la metodología Pentagrowth ayudando en el proceso de análisis inicial de " + st.session_state.context["nombre"] + " una organización de " + st.session_state.context["sector"] + " en " + st.session_state.context["pais"] + ". Realice una búsqueda web de links de referencia de las webs empresas de " + st.session_state.context["sector"] + " y sus productos o servicio principales, en lo posible de " + st.session_state.context["pais"] + ", proporcione también un listado de sus productos/servicios, se conciso, no incluir saludos, valoraciones adicionales, no sugerir Próximos pasos ni Consideraciones adicionales, debe incluir links."
	elif st.session_state.conversation_point == "carga_servicios":
		prompt = "En el siguiente texto se encuentran los principales servicios de la organización - interpretá estos servicios y devolvelos separados por coma: '" + user_input + "'"
	elif st.session_state.conversation_point == "carga_actividades_inicial":
		prompt = "Eres un asistente o facilitador de la metodología Pentagrowth ayudando en el proceso de análisis inicial de " + st.session_state.context["nombre"] + " una organización de " + st.session_state.context["sector"] + " en " + st.session_state.context["pais"] + ", cuyas principales productos o servicios son: " + st.session_state.context["servicios"] + " En base a la empresa, sector de actividad y principales servicios realiza un listado de las posibles principales actividades de la organización. Responde sin el párrafo de introducción, sin decir absolutamente aquí lo tienes, no agregar más productos o servicios de los que están en la lista, no saludar ni agregar recomendaciones, Pasos futuros o nada más."
	elif st.session_state.conversation_point == "carga_actividades":
		prompt = "En el siguiente texto se encuentran las principales actividades de la organización - interpretá estas actividades y devolvelas separadas por coma: '" + user_input + "'"
	elif st.session_state.conversation_point == "estructura_organizacional_inicial":
		prompt = "Eres un asistente o facilitador de la metodología Pentagrowth ayudando en el proceso de análisis inicial de " + st.session_state.context["nombre"] + " una organización de " + st.session_state.context["sector"] + " en " + st.session_state.context["pais"] + ". Detalle un posible organigrama para una empresa de esas características, establezca la estructura organizacional y cuáles son las principales áreas de operación. El formato de respuesta debe ser: ## Estructura Organizacional (no es necesario diagrama visual, se requiere simplemente un listado de los niveles jerárquicos y detalle tipo del estructura elegido): ##Principales áreas de operación: Ceñirse a ese formato, sin agregar información adicional, ni saludos, ni conclusiones, se conciso, no agregar recomendaciones, Pasos futuros o nada más. Al final agregar un párrafo con una referencia web a un link de información de posibles estructuras jerárquicas en ese sector de actividad."
	elif st.session_state.conversation_point == "estructura_organizacional":
		prompt = "En el siguiente texto se encuentran la estructura de la organización - interpreta principales sectores, areas y dependencias  y devolvelas separadas por coma: '" + user_input + "'"		
	elif st.session_state.conversation_point == "empresas_pioneras":
		prompt = "Eres un asistente o facilitador de la metodología Pentagrowth ayudando en el proceso de análisis inicial de " + st.session_state.context["nombre"] + " una organización de " + st.session_state.context["sector"] + " en " + st.session_state.context["pais"] + "\
		Realice una búsqueda web para encontrar referencias con links de organizaciones y empresas pioneras en el sector " + st.session_state.context["sector"] + " en " + st.session_state.context["pais"] + " e internacionalmente y alguna noticia o link de porque son pioneras. Se conciso, debe incluir al menos 3 empresas nacionales y 5 internacionales. También incluir un listado de 3 empresas nacionales y 5 internacionales innovadoras y lideres en el mercado (buscar información de cuadrantes de Gartner o fuentes similares, evaluaciones de mercado de MIT, Stanford, otras consultoras). Con el siguiente formato: \
		### Formato de respuesta  \
		Empresas pioneras nacional \
		1.	Nombre empresa 1, (enlace a su homepage, de no encontrarlo quitar esto) \
		Link y resumen de noticia o artículo de porque es pionera. \
		Empresas innovadoras y lideres en el mercado nacional \
		1.	Nombre empresa 1, (enlace a su homepage, de no encontrarlo quitar esto) \
		Link y resumen de noticia o artículo de porque lidera el mercado o que innovación llevo a cabo. \
		\
		Si para el país no se encuentra información de empresas pioneras, ampliar la búsqueda a la región, buscar las empresas lideres en el mercado, sugerir únicamente donde buscar la informacion, no presentar el listado vacio.\
		\
		Empresas pioneras internacional\
		1.	Nombre empresa internacional 1, (enlace a su homepage, de no encontrarlo quitar esto)\
		Link y resumen de noticia o articulo de porque es pionera.\
		\
		Empresas innovadoras y lideres en el mercado internacional\
		1.	Nombre empresa 1, (enlace a su homepage, de no encontrarlo quitar esto)\
		Link y resumen de noticia o artículo de porque lidera el mercado o que innovación llevo a cabo.\
		### Fin respuesta\
		La respuesta debe contener únicamente la información pedida en el formato de respuesta, no debe incluir párrafo resumen de la tarea, valoraciones adicionales, no incluir Próximos pasos, no incluir Consideraciones adicionales, no incluir apartados de Cómo utilizar esta información para"  + st.session_state.context["nombre"] + ", si debe incluir links a las webs de las empresas y a las referencias."
	elif st.session_state.conversation_point == "tecnologias_emergentes":
		prompt = "Eres un asistente o facilitador de la metodología Pentagrowth ayudando en el proceso de análisis inicial de " + st.session_state.context["nombre"] + " una organización de " + st.session_state.context["sector"] + " en " + st.session_state.context["pais"] + "\
			Al día de hoy, identifica que tecnologías emergentes (desarrolladas o implementadas en los últimos 5 años) emergentes han adoptado las organizaciones exitosas en otros países en el sector de " + st.session_state.context["sector"] + ".\
			\
			Para cada tecnología incluir un caso de éxito de implementación en algún país por alguna empresa, en lo posible incluir referencias a links webs de tenerlos. En formato: \
			\
			### Tecnología emergente (hace cuanto apareció o se popularizo)\
			Ejemplo de caso de éxito, nombre de la empresa y en qué país\
			Referencia (Proporcionar fuente de datos de referencia si existe el enlace, únicamente para el caso que no lo encuentres eliminar este punto y no mostrar nada)\
			\
			La respuesta debe contener únicamente la información pedida, como cierre agregar un párrafo apartado luego de cómo podría ser posible aplicar estas tecnologías a una organización hipotética en el mismo sector pero que difiera de servicios/productos ofrecidos, no debe incluir párrafo resumen de la tarea, valoraciones adicionales, no incluir Próximos pasos, o preguntas adicionales para continuar la conversación."		
	elif st.session_state.conversation_point == "tecnologias_emergentes_implementacion":
		prompt = "Eres un asistente o facilitador de la metodología Pentagrowth ayudando en el proceso de análisis inicial de " + st.session_state.context["nombre"] + " una organización de " + st.session_state.context["sector"] + " en " + st.session_state.context["pais"] + "\
			En base a la siguiente lista de tecnologias emergentes relevantes para el sector de " + st.session_state.context["sector"] + ": " + st.session_state.context["tecnologias_emergentes"] + "Para cada tecnología mencionada realiza una búsqueda web para buscar un caso de éxito en el formato: ### Tecnologia emergente (hace cuanto apareció o se popularizo) -Ejemplo de caso de éxito, nombre de la empresa y en que país -Referencia (Proporcionar fuente de datos de referencia si existe el enlace, únicamente para el caso que no lo encuentres eliminar este punto y no mostrar nada) -Implementación (camino recorrido por esa empresa o como implemento la tecnologia). A su vez agregar para una empresa que busca implementarlo los apartados -Pasos para implementar (los pasos a seguir para implementar innovaciones con alguna de estas tecnologías en una empresa) -Madurez (requisitos técnicos y humanos) -Horizonte temporal requerido.   La respuesta debe contener únicamente la información pedida, no debe incluir párrafo resumen de la tarea, valoraciones adicionales, no incluir Próximos pasos, o preguntas adicionales para continuar la conversación."
	elif st.session_state.conversation_point == "validacion" and user_input is None:
		prompt = "Dada la siguiente información de la empresa presentala y preguntá si es correcta: " + str(st.session_state.context)
	elif st.session_state.conversation_point == "validacion":
		prompt = "Respondé S si la respuesta del usuario es afirmativa - respondé N en cualquier otro caso: " + user_input
	elif st.session_state.conversation_point == "empresas_pioneras":
		prompt = "Qué empresas pioneras hay en el mundo en el sector " + st.session_state.context["sector"] + " y la industria " + st.session_state.context["industria"] + " que provean servicios de " + st.session_state.context["servicios"] + " y actividades de " + st.session_state.context["actividades"] + "?"
	return prompt

def context_load(respuesta_gemini: str) -> bool:
	campos = respuesta_gemini.split("\n")
	for campo in campos:
		if "=" in campo:
			cv = campo.split("=")
			clave = cv[0]
			valor = cv[1]
			if "No especificado" not in valor and clave in st.session_state.context and st.session_state.context[clave] is None:
				st.session_state.context[clave] = valor
			elif "No especificado" not in valor and clave in st.session_state.context:
				prompt = "Resumí la siguiente información para representar el campo " + clave + " :'" + st.session_state.context[clave] + "' y '" + valor + "'"
				st.session_state.context[clave] = prompt_gemini(prompt)
				print(st.session_state.context[clave])
	for clave in st.session_state.context:
		if st.session_state.context[clave] is None:
			return False
	return True

def state_machine_answer(user_input: str = None) -> str:
	if st.session_state.conversation_point == "carga_organizacion":
		prompt = get_prompt(user_input)
		st.session_state.context["nombre"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_pais"
		respuesta = "En qué país opera " + st.session_state.context["nombre"]
	elif st.session_state.conversation_point == "carga_pais":
		prompt = get_prompt(user_input)
		st.session_state.context["pais"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_tamanio"
		respuesta = "Cuál es el tamaño y qué cantidad de gente trabaja en " + st.session_state.context["nombre"]
	elif st.session_state.conversation_point == "carga_tamanio":
		prompt = get_prompt(user_input)
		st.session_state.context["tamanio"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_sector"
		respuesta = "Cual es el sector e industria en el que opera " + st.session_state.context["nombre"]
	elif st.session_state.conversation_point == "carga_sector":
		prompt = get_prompt(user_input)
		st.session_state.context["sector"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_servicios_inicial"
		respuesta = "Cuales son los principales servicios que ofrece " + st.session_state.context["nombre"] + '? Para ayudarte a responder esta pregunta puedo facilitarte información y referencias de otras empresas en el sector de productos como disparador, si la quieres ingresa ayuda. De lo contrario detallar los principales productos o servicios en forma de lista.'
	elif st.session_state.conversation_point == "carga_servicios_inicial":
		if user_input.strip().lower() == 'ayuda':
			prompt = get_prompt(user_input)
			st.session_state.conversation_point = "carga_servicios"
			respuesta = prompt_gemini(prompt) + "\n\nEspero que le haya sido útil, a continuación detalle los principales servicios que ofrece " + st.session_state.context["nombre"]
			st.markdown(respuesta)
		else:
			st.session_state.conversation_point = "carga_servicios"
	elif st.session_state.conversation_point == "carga_servicios":
		prompt = get_prompt(user_input)
		st.session_state.context["servicios"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_actividades_inicial"
		prompt = get_prompt(user_input)
		st.session_state.context["actividades_gemini"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_actividades"
		respuesta = "Cuales son las principales actividades que realiza, en base al listado de productos/servicios principales de " + st.session_state.context["nombre"] + " te proporcionaré para ayudarte un listado de actividades de ejemplo para cada uno.\n\n" + st.session_state.context["actividades_gemini"] + "\n\n\nEspero que le haya sido útil, si esta de acuerdo con las actividades responda SI, de lo contrario liste a continuación las actividades principales de " +  st.session_state.context["nombre"]
		st.markdown(respuesta)
	elif st.session_state.conversation_point == "carga_actividades":
		if user_input.strip().lower() == 'si':
			st.session_state.context["actividades"] = st.session_state.context["actividades_gemini"]
			st.session_state.conversation_point = "estructura_organizacional_inicial"
			respuesta = "¿Cómo es la estructura organizacional y cuáles son las principales áreas de operación? \nLa estructura organizacional es algo vivo y depende de la propia evolución de la organización. \n\n Para ayudarte a responder esta pregunta puedo facilitarte referencias de estructura y divisiones de una empresas prototipo en el sector de productos como disparador. Si lo quieres responde ayuda"
			st.markdown(respuesta)
		else:
			prompt = get_prompt(user_input)
			st.session_state.context["actividades"] = prompt_gemini(prompt)
			st.session_state.conversation_point = "estructura_organizacional_inicial"
			respuesta = "¿Cómo es la estructura organizacional y cuáles son las principales áreas de operación? \nLa estructura organizacional es algo vivo y depende de la propia evolución de la organización. \n\n Para ayudarte a responder esta pregunta puedo facilitarte referencias de estructura y divisiones de una empresas prototipo en el sector de productos como disparador. Si lo quieres responde ayuda"
			st.markdown(respuesta)
	elif st.session_state.conversation_point == "estructura_organizacional_inicial":
		if user_input.strip().lower() == 'ayuda':
			prompt = get_prompt(user_input)
			respuesta = prompt_gemini(prompt) + "\n\nEspero que le haya sido útil, a continuación detalle la estructura organizacional de " + st.session_state.context["nombre"]
			st.session_state.conversation_point = "estructura_organizacional"
			st.markdown(respuesta)
		else:
			st.session_state.conversation_point = "estructura_organizacional"
	elif st.session_state.conversation_point == "estructura_organizacional":
		prompt = get_prompt(user_input)
		st.session_state.context["servicios"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "empresas_pioneras"
		respuesta = "Ahora para analizar la situación en el sector, le puedo proporcionar ejemplos de organizaciones o empresas que sean pioneras a modo de disparador, si lo quiere comente SI, de lo contrario ingrese las empresas pioneras en el sector " + st.session_state.context["sector"] + " a nivel internacional y nacional."
	elif st.session_state.conversation_point == "empresas_pioneras":
		prompt = get_prompt(user_input)
		st.session_state.context["empresas_pioneras"] = prompt_gemini(prompt)
		respuesta = st.session_state.context["empresas_pioneras"] + "\n\nEspero que le haya sido de ayuda el listado, puede adicionar otras empresas pioneras de considerarlo relevante, de lo contrario responda SI para continuar."
		st.session_state.conversation_point = "tecnologias_emergentes"
		prompt = get_prompt(user_input)
		st.session_state.context["tecnologias_emergentes"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "implementacion_tecnologias_emergentes"
		respuesta = "En el siguiente paso, buscaremos ejemplos de tecnologías emergentes han adoptado las organizaciones exitosas en otros países: \n\n" + st.session_state.context["tecnologias_emergentes"] + "\n\nTambién es importante pensar cómo han implementado estas tecnologías para mejorar sus operaciones y servicios las empresas. Si desea que le proporcionemos ejemplos de implementación para cada tecnología mencionada en el paso anterior conteste SI."	
	elif st.session_state.conversation_point == "tecnologias_emergentes_implementacion":
		prompt = get_prompt(user_input)
		st.session_state.context["tecnologias_emergentes_implementacion"] = prompt_gemini(prompt)
		respuesta = st.session_state.context["tecnologias_emergentes_implementacion"] + "\n\nAhora pensando a nivel de " + st.session_state.context["nombre"] + "Qué tecnologías emergentes podrían impactar a la organización en los próximos 5 a 10 años"	
		st.session_state.conversation_point = "validacion"
	elif st.session_state.conversation_point == "validacion":
		prompt = get_prompt(user_input)
		resp = prompt_gemini(prompt)
		print(resp)
		validado = resp == "S"
		if validado:
			st.session_state.conversation_point = "empresas_pioneras"
			prompt = get_prompt()
			respuesta = prompt_gemini(prompt)
		else:
			respuesta = "Volvemos a empezar"
	else:
		respuesta = "Hasta acá llegué."
	return respuesta

# Function to handle user input and update chat history
def send_message():
    user_input = st.session_state.user_input
    if user_input:
        # Add the user's message to the chat history
        st.session_state.messages.append({"sender": "user", "text": user_input})
        
        # Simulate a bot response (for demo purposes)
        bot_response = state_machine_answer(user_input)
        st.session_state.messages.append({"sender": "Asistente", "text": bot_response})
        
        # Clear the input box
        st.session_state.user_input = ""



st.image("vortex_h.png", width=400)

st.markdown(
    """
    <style>
    .chat-container {
        background-color: rgba(255, 255, 255, 0.1);  /* White background with 10% opacity */
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .chat-container {
        background-color: rgba(255, 255, 255, 0.1); 
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Iterate through messages and display them in a chat format
for message in st.session_state.messages:
    if message["sender"] == "user":
        st.markdown(f"""
        <div style="text-align: right; margin: 10px 0; clear: both;">
            <div style="display: inline-block; padding: 10px; background-color: #27106A; border-radius: 10px; float: right;">
                <strong>You:</strong> {message['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)  # Light purple background for user input (Thistle color)
    else:
        st.markdown(f"""
        <div style="text-align: left; margin: 10px 0; clear: both;">
            <div style="display: inline-block; padding: 10px; background-color: #4A2569; border-radius: 10px; float: left;">
                <strong>Asistente:</strong> {message['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)  # Light orange background for bot response (Peach Puff color)

# Input box for the user to type their message, positioned at the bottom
st.text_input("Your message:", key="user_input", on_change=send_message)