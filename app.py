import streamlit as st
import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ===========================================================
# 1️⃣ Chargement du modèle IA
# ===========================================================
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return tokenizer, model

tokenizer, model = load_model()

# Historique des messages
if "history" not in st.session_state:
    st.session_state.history = None


# ===========================================================
# 2️⃣ Reconnaissance vocale
# ===========================================================
def transcribe_speech():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("🎤 Parlez maintenant...")
            audio = recognizer.listen(source)

        st.info("⏳ Transcription...")
        text = recognizer.recognize_google(audio, language="fr-FR")
        return text

    except sr.UnknownValueError:
        return "Désolé, je n'ai pas compris."
    except:
        return "Erreur avec le microphone ou Google Speech."


# ===========================================================
# 3️⃣ Assistant IA intelligent
# ===========================================================
def ia_response(message):
    # encode le message utilisateur
    input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")

    # concaténer avec historique si existe
    if st.session_state.history is not None:
        bot_input = torch.cat([st.session_state.history, input_ids], dim=-1)
    else:
        bot_input = input_ids

    # réponse générée
    st.session_state.history = model.generate(
        bot_input,
        max_length=250,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        st.session_state.history[:, bot_input.shape[-1]:][0],
        skip_special_tokens=True
    )

    return response


# ===========================================================
# 4️⃣ Interface Streamlit
# ===========================================================
def main():
    st.title("🤖 Assistant IA Vocal & Textuel")
    st.write("📌 Posez vos questions par **texte ou voix**.")

    # ======== Entrée textuelle ===========
    user_text = st.text_input("💬 Votre message (texte) :")

    if user_text:
        bot_reply = ia_response(user_text)
        st.write(f"🤖 **Assistant IA :** {bot_reply}")

    # ======== Entrée vocale ===========
    if st.button("🎤 Parler avec le micro"):
        spoken_text = transcribe_speech()
        st.write(f"🗣️ Vous avez dit : **{spoken_text}**")

        bot_reply = ia_response(spoken_text)
        st.write(f"🤖 **Assistant IA :** {bot_reply}")


if __name__ == "__main__":
    main()
