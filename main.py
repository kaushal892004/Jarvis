import os
import time
import datetime
import webbrowser
import speech_recognition as sr
import pyfiglet
import smtplib
import pywhatkit
from gtts import gTTS
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from google.generativeai import configure, GenerativeModel
import re

# ========== INITIALIZE ==========
console = Console()
QUERY_LOG_FILE = "jarvis_query_log.txt"

# ========== SPEAK ==========
def speak(text):
    console.print(f"[bold cyan]JARVIS:[/bold cyan] {text}")
    tts = gTTS(text=text, lang='en')
    tts.save("voice.mp3")
    os.system("start voice.mp3" if os.name == "nt" else "afplay voice.mp3")
    time.sleep(1.5)
    os.remove("voice.mp3")

# ========== WISHING ==========
def wish_me():
    hour = datetime.datetime.now().hour
    greeting = "Good morning!" if hour < 12 else "Good afternoon!" if hour < 18 else "Good evening!"
    speak(greeting)
    speak("I am JARVIS. How can I assist you today?")

# ========== VOICE INPUT ==========
def take_voice_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        console.print("[yellow]🎙 Listening...[/yellow]")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        console.print("[green]🧠 Recognizing...[/green]")
        query = r.recognize_google(audio, language='en-in')
        console.print(f"[bold magenta]🗣 You:[/bold magenta] {query}")
    except Exception:
        console.print("[red]❌ Sorry, I didn't catch that.[/red]")
        return "none"
    return query.lower()

# ========== TEXT INPUT ==========
def take_text_command():
    return Prompt.ask("[bold green]⌨️ Enter your command[/bold green]").lower()

# ========== LOGGING ==========
def log_query(query):
    with open(QUERY_LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {query}\n")

# ========== GEMINI AI ==========
def gemini_summary_response(prompt):
    configure(api_key="AIzaSyDOfOQEIGNGtZeuZv4rSRzAuvWtLEvcZnE")
    model = GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"Give a short, simple, and accurate answer to: {prompt}",
        generation_config={"temperature": 0.5, "max_output_tokens": 60}
    )
    return response.text.strip()

# ========== EMAIL SENDING ==========
def send_email(to_address, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("kaushalparmarofficial@gmail.com", "jchj rbwn lndp pypd")
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail("kaushalparmarofficial@gmail.com", to_address, message)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I was unable to send the email.")
        console.print(str(e), style="red")

# ========== WHATSAPP MESSAGING ==========
def send_whatsapp(phone_number, message):
    try:
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute + 1
        pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
        speak("Message scheduled on WhatsApp.")
    except Exception as e:
        speak("Failed to send WhatsApp message.")
        console.print(str(e), style="red")


# ========== PERFORM ACTION ==========
def perform_task(command):
    speak("Processing your request...")
    log_query(command)
    time.sleep(1)

    command = command.lower()

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram.")
    elif re.search(r"play (.+) on youtube", command):
        song = re.search(r"play (.+) on youtube", command).group(1)
        speak(f"Searching and playing {song} on YouTube.")
        try:
            pywhatkit.playonyt(song)
        except Exception as e:
            speak("I couldn't play the video. Something went wrong.")
            console.print(str(e), style="red")
    elif re.search(r"search (.+) on google", command):
        query = re.search(r"search (.+) on google", command).group(1)
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query} on Google.")
    elif "the time" in command:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
    elif "send email" in command:
        to = Prompt.ask("Enter recipient email")
        subject = Prompt.ask("Enter subject")
        body = Prompt.ask("Enter message")
        send_email(to, subject, body)
    elif "send whatsapp" in command:
        phone = Prompt.ask("Enter phone number with country code")
        message = Prompt.ask("Enter your message")
        send_whatsapp(phone, message)
    elif "stop" in command or "exit" in command:
        speak("Shutting down. Have a nice day!")
        exit()
    else:
        # fallback to Gemini AI
        answer = gemini_summary_response(command)
        speak(answer)


# ========== DASHBOARD ==========
def show_dashboard():
    banner = pyfiglet.figlet_format("JARVIS", font="slant")
    centered = "\n".join(line.center(80) for line in banner.split("\n"))
    console.print(centered, style="bold blue")

    profile_text = Text()
    profile_text.append("Kaushal Parmar Here; ", style="bold white")
    profile_text.append("✓\n", style="blue")
    profile_text.append("Hi there, I am a software developer. Passionate about web developmentand Cloud/DevOps.\n\n", style="white")
    profile_text.append("\U0001F419 GitHub: ", style="bold yellow")
    profile_text.append("@kaushal892004\n", style="blue")
    profile_text.append("\U0001F4BC LinkedIn: ", style="bold yellow")
    profile_text.append("@kaushalparmar\n", style="blue")
    profile_text.append("\U0001F4E7 Email: ", style="bold yellow")
    profile_text.append("kaushalparmarofficial@gmail.com\n", style="blue")
    console.print(Panel(profile_text, title="\U0001F468‍\U0001F4BB About Me", style="bold cyan", padding=(1, 2)))

# ========== MAIN ==========
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    show_dashboard()
    speak("Initializing JARVIS. Please wait...")
    time.sleep(1)
    speak("JARVIS initialized.")
    wish_me()

    while True:
        mode = Prompt.ask("\n[bold cyan]\U0001F9E0 Choose input mode[/bold cyan] ", choices=["text", "voice"])
        command = take_text_command() if mode == "text" else take_voice_command()
        if command != "none":
            perform_task(command)
