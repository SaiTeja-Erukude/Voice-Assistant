import pyttsx3                                          # Python text to speech library
import datetime                                         
import speech_recognition as sr                         # used for speech recognition
import webbrowser                                       # used to open web browsers
from time import sleep
import wikipedia                                        # access data from wikipedia
import os
import wolframalpha                                     # used to compute expert level answers
import pyjokes
import pywhatkit as kit                                 # to send whatapp texts
import pandas                                           

engine = pyttsx3.init("sapi5")                          # Speech API that helps in synthesis & voice recognition

voices = engine.getProperty("voices")                   
engine.setProperty(engine, voices[0].id)                # assigning our desktop assistant a voice 

assistantName = "Ultron".lower()


# speak function pronounces the msg
def speak(msg):
    print(assistantName+": "+msg)
    engine.say(msg)
    engine.runAndWait()    


# greet function greets the user based on the time
def greet():
    time = datetime.datetime.now().hour
    
    if 0 <= time < 12:
        speak("Good morning sir! I'm " + assistantName + ", your desktop assistant.")
    elif 12 <= time < 18:
        speak("Good day sir!, I'm " + assistantName +", your desktop assistant.")
    else:
        speak("Good evening sir!, I'm " + assistantName +", your desktop assistant.")
    
    
# listen function recognizes the user's voice and returns a string
def listen():  
    r = sr.Recognizer()
    with sr.Microphone() as source:    
        print("Listening...")
        r.pause_threshold = 1.2
        r.energy_threshold = 4000
        audio = r.listen(source)        
    try:    
        audio_text = r.recognize_google(audio)
        print("You: ",audio_text)
        return audio_text
    except Exception:
        return "None"
 
 
# speaks the current time   
def speakTime():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak("Time right now is "+time)      
 
 
# main function
if __name__ == "__main__":    
    greet()
    
    # registering the chrome browser
    webbrowser.register('chrome', None, 
                        webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    
    greetings = ["hey", "hi", "hello"]
    greetings_response = ["i am good", "i'm good", "good", "fine", "great", "awesome", "i am doing great", "i am fine", "thanks for asking, i am doing good", "thank you", "thanks"] 
    status = ["how are you", "how are you doing"]
    closures = ["bye", "shutdown", "quit", "exit", "talk later", "see you", "goodbye"]
    write_notes = ["take notes", "write notes", "note down", "reminder", "add a reminder", "write a note"]
    read_notes = ["open notes", "read notes", "open reminders", "read my notes", "open my notes"]
    
    # wolfram alpha api id
    app_id = "XXXXX-XXXXXXXXXX"
    client = wolframalpha.Client(app_id)
    
    # news api key
    newsapi_key = "XXXXXXXXXXXXXXXXXXXXX"
    
    while True:
        command = listen().lower().replace(assistantName, "").strip()        
        if command in status:
            speak("I am doing great. How about you sir?")
        
        elif command in greetings:
            speak("Hello sir, how can I help you?")
            
        elif command in greetings_response:
            speak("Awesome! What else can I do for you?")
        
        
        # to compute expert level answers unsing wolframalpha
        elif "what is " in command or "who is " in command or "what are " in command:
            if "time" in command:
                speakTime()
            else:
                result = client.query(command)
                try:
                    speak(next(result.results).text)
                except Exception:
                    speak("Could not find anything.")
        
        
        # to open YouTube                        
        elif "youtube" in command:
            speak("Opening YouTube!")
            webbrowser.get('chrome').open("youtube.com")
            sleep(5)
        
        
        # to do a google search   
        elif "google" in command:
            speak("What do you want me to search?")
            search_topic = listen()  
            while search_topic == "None": search_topic = listen()   
            if search_topic not in closures:
                kit.search(search_topic)      
                sleep(5)
        
        
        # to do a wikipedia search                        
        elif "wikipedia" in command:
            speak("On it! Just a sec.")
            try:
                command = command.replace("wikepedia", "").strip()
                result = wikipedia.summary(command, sentences=1)
                speak("According to Wikipedia "+ result)          
            except:
                speak("Could not find anything.")  
            sleep(5)
                      
                      
        elif "time" in command:
            speakTime()
            sleep(5)
        
        
        # to take notes
        elif command in write_notes:
            path = "C://Users//SAI TEJA//Desktop//Python//Virtual_Assistant//notes.txt"
            mode = "a" if os.path.exists(path) else "w+"
            speak("What do you want me to note?")
            note = listen()
            while note == "None": note = listen()
            if note not in closures:
                with open(path, mode) as f:
                    f.write(note)
                    f.write(" -- "+str(datetime.date.today())+" "+str(datetime.datetime.now().strftime("%I:%M %p")))
                    f.write("\n")
                speak("Roger that.")
                sleep(5)
        
        
        # read the existing notes        
        elif command in read_notes:
            with open("notes.txt", "r") as f:
                lines = f.readlines()
                speak("Your notes says ")
                for line in lines:
                    line = line.split("--")[0]
                    speak(line)                
                        
                                
        # to hear a joke
        elif "joke" in command or "another one" in command or "one more" in command:
            speak(pyjokes.get_joke())
        
        
        # asking assistant to sleep               
        elif "sleep" in command or "offline" in command:
            speak("Please specify time")
            try: 
                sleepTime = int(listen())
                speak("Going offline for", sleepTime)
                sleep(sleepTime)
            except:
                sleep(5)
            speak("Hi there, I am back at your service.")
        
        
        # play songs on YouTube
        elif "play" in command:
            command = command.replace("play", "").strip()
            speak("Playing "+ command)
            kit.playonyt(command)
            sleep(10)
        
        
        # send a whatsapp text
        elif "text" in command or "message" in command:
            contacts = {
                "mum" : "+91XXXXXXXXXX",
                "dad" : "+91XXXXXXXXXX",
                "bro" : "+91XXXXXXXXXX"
            }
            if "text" in command:
                person = command.replace("text", "").strip().lower()
            elif "message" in command:
                person = command.replace("message", "").strip().lower()
            
            speak("What is the message?")
            msg = listen()
            while msg == "None": msg = listen()
            
            if msg not in closures:
                hour = datetime.datetime.now().hour
                mins = datetime.datetime.now().minute
                speak("Sending your message. It might take a minute.")          
                try:  
                    kit.sendwhatmsg(contacts[person], msg, hour, mins+1)
                except:
                    kit.sendwhatmsg(contacts[person], msg, hour, mins+2)                 
                speak("Message sent!")
            sleep(5)
        
        
        # get the latest news
        elif "read news" in command or "read headlines" in command:
            
            url = ('https://newsapi.org/v2/top-headlines?'
                    'country=in&'
                    'apiKey='+newsapi_key)
            
            response = pandas.read_json(url, encoding='UTF-8')
            i = 1
            for item in response["articles"]:
                if i < 4:
                    speak(str(i) + ". " + item["title"])
                    i += 1
                else: break     
            sleep(5)     
        
        
        # locate a place in maps   
        elif "where is" in command or "locate" in command:
            location = command.replace("where is", "").strip()
            location = location.replace("locate", "").strip()
            speak("Locating " + location)
            webbrowser.get('chrome').open("https://www.google.nl/maps/place/" + location)
            sleep(5)

                      
        elif "who are you" in command or "what are you" in command:
            speak("I'm " + assistantName +", your desktop assistant.")
            
        elif "who created you" in command or "who built you" in command or "who developed you" in command:
            speak("I was built by 'Sai Teja Erukude'. Thanks to him.")
                  
        elif command in closures:
            speak("See you again sir, BYE!")
            exit()   
                    
        else:
            speak("I'm afraid that I could not help you with that.")
            sleep(3)