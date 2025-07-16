import speech_recognition as sr
import pyttsx3
import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText
import os
import webbrowser
import datetime

# Gemini API Key setup
genai.configure(api_key="Enter your own api key")  # Replace with your API key
model = genai.GenerativeModel("gemini-pro")

# Initialize Text-to-Speechhi
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Female voice

# Speak output
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# Send email function
def send_email(recipient, subject, body):
    sender = "ranjithdevaraj45@gmail.com"  # Replace with your email
    password = "2231"  # Replace with your Gmail App Password

    msg = MIMEText(body)
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"
    

# Listen for user voice
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        r.adjust_for_ambient_noise(source, duration=0.3)  # Shorter adjustment
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)  # Faster listen
        except sr.WaitTimeoutError:
            speak("❌ No voice detected")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print("You:", query)
        return query
    except sr.UnknownValueError:
        speak("❌ Could not understand.")
        return None
    except sr.RequestError:
        speak("Network error. ")
        return None

# Main loop
def run_assistant():
    speak(" I'm your sadhana . how can i help u!")

    while True:
        user_input = listen()
        if user_input:
            command = user_input.lower()

            # Stop command
            if command in ['thanks', 'goodbye', 'done', 'finish', ]:
                speak(" thank for use me ")
                break

            # 🔧 Custom commands
            elif 'open notepad' in command:
                speak("Opening Notepad")
                os.system("notepad.exe")
            #open figma 
            elif 'open figma' in command:
                speak("opening the figma app")
                os.startfile(r"c:\\users\\appdata\\local\\Figma\\Figma.exe")
            #open youtube
            elif 'open youtube' in command:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")
            #open google 
            elif 'open google' in command:
                speak("Opening Google")
                webbrowser.open("https://google.com")
            #open mail and send mail
            elif 'email' in command and 'send' in command:
                speak("Who should I send it to?")
                recipient_input = listen()
                if recipient_input:
                    recipient_email = recipient_input.replace(" ", "") + "@gmail.com"

                    speak("What is the subject?")
                    subject = listen()

                    speak("What is the message?")
                    body = listen()

                    if subject and body:
                        result = send_email(recipient_email, subject, body)
                        speak(result)
                    else:
                        speak("Subject or message was empty.")

            #open github 
            elif 'open Github' in command:
                speak("opening Github ")
                try:
                    chrome_pathn = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
                    webbrowser.get(chrome_pathn).open("https:github.com")
                except:
                    speak("Failed to open in chrome. opening in default browers.")
                    webbrowser.open("https://github.com")
            #for open vs code 
            elif 'open  code' in command:
                speak("speak vs code")
                try:
                    os.system("code")
                except:
                    speak("VS code can not be open, some technical issuse")
             #generated code 

            elif 'write code' in command or 'generate code ' in command :
                speak(" sure, ask the title")
                code_request = listen()

                if code_request:
                    try:
                        speak(" wait for few secound , i will write a code")
                        response = model.generate_content(code_request)
                        generate_code = response.text.stripI()

                        #save the code file 
                        with open("generate_code.py" , "w", encoding="utf-8") as f :
                            f.write(generate_code)
                        speak("I wrote the code to a file named generated_code.py. Want me to open it? ")
                        print("\n generated code:\n", generate_code)
                    except Exception as e:
                        speak(f"sorry, I can not generate the code. Error:v {str(e)} ")


            elif 'what time is it' in command or 'current time' in command:
                time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {time}")

            elif 'tell me a joke' in command:
                speak("Why don’t scientists trust atoms? Because they make up everything!")

            # 🤖 Default: send to Gemini AI
            else:
                try:
                    response = model.generate_content(command)
                    speak(response.text)
                except Exception as e:
                    speak(f"Error: {str(e)}")

if __name__ == "__main__":
    run_assistant(true)
