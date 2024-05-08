# Import modules
import os
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
from uutils import insertText

# Set up gemini ai api
genai.configure(api_key="<PASTE YOUR GEMINI AI API KEY HERE>")

# Set up the model
generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

system_instruction = ("You are Akash, A helpful and informative ai assistant. Give short "
                      "and precise answers. And Only If asked to "
                      "open an website reply with /c firefox <url> /c, followed by your response")

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)


class GetAI:
    def __init__(self, root, status_text_var, chatbox) -> None:
        # Initialize speech recognizer class
        self.recog = sr.Recognizer()
        self.status_text_var = status_text_var
        self.chatbox = chatbox
        self.root = root

    def generateResponse(self):
        with sr.Microphone() as source:
            # Listen for user input
            self.status_text_var.set("                "
                                     "Listening..."
                                     "                ")
            self.root.update_idletasks()
            # Stop listening if the user is not speaking for 2000ms
            audio = self.recog.listen(source, 2000)

            try:
                # Recognize user input
                user_input_text = self.recog.recognize_google(audio)
                insertText(self.chatbox, "You: " + user_input_text + "\n")
                self.root.update_idletasks()

                # Show processing status
                self.status_text_var.set("Thinking...")
                self.root.update_idletasks()

                # Generate response
                convo = model.start_chat()
                convo.send_message(user_input_text)

                # Speak response
                engine = pyttsx3.init()
                engine.setProperty('voice', 'english+f1')
                if convo.last.text.startswith("/c"):
                    response = convo.last.text.split("/c")[2].strip()
                    os.system(convo.last.text.split("/c")[1].strip())
                    insertText(self.chatbox, "Akash: " + response + "\n")
                    self.root.update_idletasks()
                    engine.say(response)
                else:
                    insertText(self.chatbox, "Akash: " + convo.last.text + "\n\n")
                    self.root.update_idletasks()
                    engine.say(convo.last.text)

                engine.runAndWait()
                self.status_text_var.set("Hi, click on the mic to speak")
                self.root.update_idletasks()

            except Exception as e:
                self.status_text_var.set("Sorry, I did not get that")
                self.root.update_idletasks()
                print("An error occurred; {0}".format(e))
