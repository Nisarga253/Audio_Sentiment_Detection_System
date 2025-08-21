import speech_recognition as sr
import pyttsx3
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import random

nltk.download('vader_lexicon')
 
engine = pyttsx3.init()

def say(text):
    """Converts text to speech and prints"""
    engine.say(text)
    engine.runAndWait()
    print(f"Bot: {text}")

def take_command():
    """Takes voice input from the user and converts it into text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            say("Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            say("Could not request results. Check your internet connection.")
            return ""
        except Exception as e:
            say("Something went wrong while listening.")
            print(f"Error: {e}")
            return ""

def get_emotion_response(emotion, user_input):
    """Generates a conversational reply based on emotion and user speech"""
    # You can improve this with ChatGPT API or fine-tuned models later
    responses = {
        "happy or excited": [
            "That’s awesome! I’m so happy for you!",
            "Wow, that sounds exciting!",
            "Congratulations! You deserve it!"
        ],
        "calm or content": [
            "That’s great. Peaceful days are the best.",
            "I'm glad to hear you're feeling good.",
            "Sounds like you’re having a nice time."
        ],
        "neutral": [
            "Alright, feel free to tell me more.",
            "Got it. I’m here if you want to talk.",
            "Okay, let’s keep chatting."
        ],
        "sad or disappointed": [
            "I’m really sorry you feel that way. Want to talk about it?",
            "It's okay to be sad sometimes. I'm here with you.",
            "That sounds tough. You're not alone."
        ],
        "angry or frustrated": [
            "That sounds frustrating. Let it out, I’m listening.",
            "Take a deep breath. I'm here with you.",
            "That must be annoying. I'm here to help if I can."
        ]
    }
    return random.choice(responses[emotion])

def analyze_emotion(text):
    """Analyzes emotion and responds conversationally"""
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)['compound']

    if score >= 0.5:
        emotion = "happy or excited"
    elif 0.1 <= score < 0.5:
        emotion = "calm or content"
    elif -0.1 < score < 0.1:
        emotion = "neutral"
    elif -0.5 < score <= -0.1:
        emotion = "sad or disappointed"
    else:
        emotion = "angry or frustrated"

    print(f"Detected emotion: {emotion}")
    reply = get_emotion_response(emotion, text)
    say(reply)

if __name__ == '__main__':
    say("Hello! I'm here to chat with you. Speak to me anytime!")

    while True:
        command = take_command()

        if "exit" in command or "quit" in command or "stop" in command:
            say("Goodbye! Take care.")
            break

        if command:
            analyze_emotion(command)