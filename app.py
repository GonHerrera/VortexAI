import json
import requests

import streamlit as st

# Initialize session state to store the conversation history
if "messages" not in st.session_state:
	mensaje_inicial = "Para comenzar por favor indique el nombre de la organización con la que va a estar trabajando."
	st.session_state.messages = [{"sender": "Asistente", "text": mensaje_inicial}]
	st.session_state.conversation_point = "carga_organizacion"
	st.session_state.context = {}

GEMINI_KEY = "AIzaSyBsDMtRe_EA5XcI0u5oAYkNT54bdI7dt_w"
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
	elif st.session_state.conversation_point == "carga_servicios":
		prompt = "En el siguiente texto se encuentran los principales servicios de la organización - interpretá estos servicios y devolvelos separados por coma: '" + user_input + "'"
	elif st.session_state.conversation_point == "carga_actividades":
		prompt = "En el siguiente texto se encuentran las principales actividades de la organización - interpretá estas actividades y devolvelas separadas por coma: '" + user_input + "'"
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
		respuesta = "Cual es el sector en el que opera " + st.session_state.context["nombre"]
	elif st.session_state.conversation_point == "carga_sector":
		prompt = get_prompt(user_input)
		st.session_state.context["sector"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_industria"
		respuesta = "Cual es la industria en la que opera " + st.session_state.context["nombre"]
	elif st.session_state.conversation_point == "carga_industria":
		prompt = get_prompt(user_input)
		st.session_state.context["industria"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_servicios"
		respuesta = "Cuales son los principales servicios que ofrece " + st.session_state.context["nombre"]
	elif st.session_state.conversation_point == "carga_servicios":
		prompt = get_prompt(user_input)
		st.session_state.context["servicios"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "carga_actividades"
		respuesta = "Cuales son las principales actividades que realiza " + st.session_state.context["nombre"]
	elif st.session_state.conversation_point == "carga_actividades":
		prompt = get_prompt(user_input)
		st.session_state.context["actividades"] = prompt_gemini(prompt)
		st.session_state.conversation_point = "validacion"
		prompt = get_prompt()
		respuesta = prompt_gemini(prompt)
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



# Display the chat history
st.title("Chat Interface")

# Iterate through messages and display them in a chat format
for message in st.session_state.messages:
    if message["sender"] == "user":
        st.markdown(f"""
        <div style="text-align: right; margin: 10px 0; clear: both;">
            <div style="display: inline-block; padding: 10px; background-color: #DFF2BF; border-radius: 10px; float: right;">
                <strong>You:</strong> {message['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: left; margin: 10px 0; clear: both;">
            <div style="display: inline-block; padding: 10px; background-color: #E0EBFF; border-radius: 10px; float: left;">
                <strong>Asistente:</strong> {message['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input box for the user to type their message, positioned at the bottom
st.text_input("Your message:", key="user_input", on_change=send_message)


