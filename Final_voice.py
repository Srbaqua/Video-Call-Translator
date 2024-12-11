import langdetect
import elevenlabs
from elevenlabs import generate
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
import os

# Api keys
elevenlabs.set_api_key('312fda3be276915ac4ea999308a48982') 

def detect_language(text):
    try:
        lang = langdetect.detect(text)
        return lang
    except:
        return None


def play_audio_bytes(audio_bytes):
    with open("temp_audio.mp3", "wb") as f:
        f.write(audio_bytes)
    playsound("temp_audio.mp3")

# Function to capture voice input from the user
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        audio = r.listen(source)
         
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"The user said: {query}\n")
        return query
    except Exception as e:
        print("Please say that again...")
        return None

# Main function for translation
def translate_text(query, dest_lang='en'):
    translator = Translator()
    translated_text = translator.translate(query, dest=dest_lang).text
    return translated_text

#Convert text to voice
def play_audio(text):
    audio = generate(
        text=text,
        voice="Emily",
        model="eleven_multilingual_v2"
    )

    play_audio_bytes(audio)
    
# Main function
def main():
    while True:
        # Capture voice input
        query = takecommand()
        
        while query is None:
            query = takecommand()

        # Determine the language of the input
        language = detect_language(query)

        # Translate the text to English
        translated_text = translate_text(query, dest_lang='en' if language != 'en' else 'hi')

        # Convert translated text to speech
        #speak = gTTS(text=translated_text, lang='en' if language == 'hi' else 'hi', slow=False)
        #speak.save("translated_voice.mp3")

        # Play the translated voice
        #playsound('translated_voice.mp3') This plays the sound 
        
        play_audio(translated_text)
        os.remove('temp_audio.mp3')
        
        # Print the translated text
        print(f"Translated text: {translated_text}")
        
if __name__ == "__main__":
    main()