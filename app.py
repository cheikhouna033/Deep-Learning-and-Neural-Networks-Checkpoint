import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import speech_recognition as sr

# ===========================
# 1. Téléchargement des ressources NLTK
# ===========================
nltk.download('punkt')

# ===========================
# 2. Définir un petit jeu de paires pour le chatbot
# (À remplacer par ton propre fichier texte si besoin)
# ===========================
pairs = [
    [
        r"bonjour|salut|hey",
        ["Bonjour ! Comment puis-je vous aider ?", "Salut ! Je suis là pour vous aider."]
    ],
    [
        r"(.*) ton nom ?",
        ["Je suis un chatbot vocal créé avec Streamlit et NLTK !"]
    ],
    [
        r"(.*) (aide|aider)",
        ["Je peux répondre à vos questions textuelles ou vocales."]
    ],
    [
        r"quit|exit",
        ["Au revoir !"]
    ],
    [
        r"(.*)",
        ["Je n'ai pas compris, peux-tu reformuler ?"]
    ],
]

chatbot = Chat(pairs, reflections)

# ===========================
# 3. Fonction de reconnaissance vocale
# ===========================
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Parlez maintenant...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="fr-FR")
        return text
    except sr.UnknownValueError:
        return "Désolé, je n'ai pas compris."
    except sr.RequestError:
        return "Erreur avec le service de reconnaissance vocale."

# ===========================
# 4. Fonction du chatbot modifiée
# ===========================
def chatbot_response(user_input):
    return chatbot.respond(user_input)

# ===========================
# 5. Interface Streamlit
# ===========================
st.title("💬 Chatbot Vocal avec NLTK & Reconnaissance Vocale")

st.write("Utilisez **du texte** ou **votre voix** pour discuter avec le chatbot.")

# ----- Entrée textuelle -----
text_input = st.text_input("Tapez votre message ici :")

# Bouton vocal
if st.button("🎤 Parler"):
    user_speech = speech_to_text()
    st.write(f"Vous avez dit : **{user_speech}**")
    response = chatbot_response(user_speech)
    st.write(f"🤖 Chatbot : {response}")

# Traitement texte normal
if text_input:
    response = chatbot_response(text_input)
    st.write(f"🤖 Chatbot : {response}")
