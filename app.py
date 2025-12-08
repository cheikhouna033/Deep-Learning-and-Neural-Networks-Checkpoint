import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import speech_recognition as sr

# Téléchargement des ressources NLTK
nltk.download('punkt')

# ============================================================
# 1️⃣ Définir les paires du chatbot (basique)
# ============================================================
pairs = [
    [
        r"bonjour|salut|hey",
        ["Bonjour ! Comment puis-je vous aider ?"]
    ],
    [
        r"(.*) ton nom",
        ["Je suis un petit chatbot créé pour l'exercice !"]
    ],
    [
        r"(.*) aide",
        ["Je peux répondre à des questions simples ou transcrire votre voix."]
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

# ============================================================
# 2️⃣ Fonction de reconnaissance vocale
# ============================================================
def transcribe_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Parlez maintenant...")
            audio = recognizer.listen(source)
            st.info("⏳ Transcription en cours...")
            text = recognizer.recognize_google(audio, language="fr-FR")
            return text
    except:
        return "Désolé, je n'ai pas compris."

# ============================================================
# 3️⃣ Fonction de réponse du chatbot
# ============================================================
def chatbot_response(user_input):
    return chatbot.respond(user_input)

# ============================================================
# 4️⃣ Interface Streamlit (TEXTE + VOIX)
# ============================================================
def main():
    st.title("💬 Chatbot Vocal - Version du cours")

    st.write("Vous pouvez taper un texte ou utiliser le microphone.")

    # ------ Entrée TEXTUELLE ------
    user_text = st.text_input("Votre message (texte) :")
    if user_text:
        reply = chatbot_response(user_text)
        st.write(f"🤖 Chatbot : {reply}")

    # ------ Entrée VOCALE ------
    if st.button("🎤 Parler au micro"):
        spoken_text = transcribe_speech()
        st.write(f"🗣️ Vous avez dit : **{spoken_text}**")

        reply = chatbot_response(spoken_text)
        st.write(f"🤖 Chatbot : {reply}")

if __name__ == "__main__":
    main()
