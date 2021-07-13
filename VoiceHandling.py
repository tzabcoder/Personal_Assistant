import pyttsx3
import webbrowser
import speech_recognition as sr
import datetime
from Response_Reposititory import Repository
from Process_Q import TechnicalQuestions

#Handler processes the commands from the user  
class Handler:
    repos = Repository()
    tq = TechnicalQuestions()

    #Initialize the speech engine
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'voices[0].id') #set voice type

    #Microphone variables
    mic = sr.Microphone(device_index=1)
    rec = sr.Recognizer()

    def welcome_user(self, name):
        greeting = self.repos.welcome_name(name)
        self.speak_out(greeting)

    def unknown_user(self):
        self.speak_out(self.repos.unknown_user_stmt)
        #Get the name from the user 
        #return the name

    #Greet the user with a message 
    def greeting(self):
        self.speak_out(self.repos.return_greeting())

    #Output the text recieved as an arguement 
    def speak_out(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    #Handle the user talking into the microphone 
    def talk_in(self):
        with self.mic as source: #while the microphone is active 
            try:
                self.rec.adjust_for_ambient_noise(source) #Adjust for background noise 
                audio = self.rec.listen(source) #listen for input 
                out_p = self.rec.recognize_google(audio) #translate the audio from google's engine 
            except:
                self.speak_out(self.repos.rep_stmt) #If audio input was not understood
                return ''
        
        out_p = out_p.lower() #convert command to lowercase 
        out_p_list = out_p.split(" ") #create a command list 
        return out_p_list

    #Speaking ouput upon assistant termination
    def process_end(self):
        self.speak_out(self.repos.end_stmt)
        exit() #Exit the program

    #Process user URL requests 
    def process_URL(self, command, position): 
        key_word = command[position]

        if key_word == "go": #Handle semantics for the command "go to"
            site = command[position + 2]
        else:
            site = command[position + 1]
        try:
            if ".com" in site: #if the user specifies .com
                self.speak_out(self.repos.url_proc)  
                webbrowser.open_new_tab(site) #open the site in a webbrowser 
            else:
                site = site + ".com" #include .com if not specified
                self.speak_out(self.repos.url_proc) 
                webbrowser.open_new_tab(site) 
        except:
            self.speak_out(self.repos.urlprob_stmt) #handle browser errors 

    #Process a current time request
    def process_time(self):
        time = self.repos.get_current_time()

        #Handle the time of the day
        if time >= 120000:
            time_var = "p m"
            if time >= 130000:
                time = time - 120000
        else:
            time_var = "a m"

        #Format the time 
        time = str(time)
        time = time[:-2]
        hours = time[:-2]
        minutes = time[1:3]
        time = f"{hours} {minutes} {time_var}"

        self.speak_out(self.repos.time_stmt + time) #Output the time 

    #Process a search request
    def process_search(self, command):
        key_pos = 0
        search_pos = 0
        search_query = ""
        length = len(command)

        for word in command:
            if word in self.repos.search_keywords: #If there is a keyword in the command 
                break
            else:
                key_pos += 1
        
        #look for the keywords in the command 
        if command[key_pos] == "show":
            if command[key_pos+1] == "me":
                search_pos = key_pos + 2
            else:
                search_pos = key_pos + 1
        if command[key_pos] == "look":
            search_pos = key_pos + 2
        if command[key_pos] == "search":
            search_pos = key_pos + 1

        temp_c = command[search_pos:length] #Concatination of the command
        for temp in temp_c:
            search_query = search_query + temp + " " #Create a search query from the command 
        
        #Search the web
        self.speak_out(self.repos.search_proc)
        webbrowser.open_new_tab(search_query) #Open a browser with the search query

    #Handle news requests
    def open_news(self):
        self.speak_out(self.repos.news_proc)
        webbrowser.open_new_tab("https://www.foxnews.com/") #Open the Fox news site
    
    #Parses the user input command 
    def parse_command(self, command):
        valid_command = False 

        #Check to see if there is a terminating word 
        check = any(item in self.repos.terminate_keywords for item in command)
        if check:
            self.process_end()
            valid_command = True
        else:
            pass #if not a terminate command

        #Process Basic Conversation (Reach can respond to simple questions)
        #__________________________________________________________________________
        cont = all(item in command for item in self.repos.ask_keywords)
        if cont:
            self.speak_out(self.repos.rephow_stmt)
            valid_command = True 
        
        cont = all(item in command for item in self.repos.id_keywords)
        if cont:
            self.speak_out(self.repos.repwho_stmt)
            valid_command = True
        
        cont = all(item in command for item in self.repos.cando_keywords)
        if cont:
            self.speak_out(self.repos.cando_stmt)
            valid_command = True

        cont = all(item in command for item in self.repos.lan_keywords)
        if cont:
            self.speak_out(self.repos.lang_stmt)
            valid_command = True

        cont = all(item in command for item in self.repos.whylan_keywords)
        if cont:
            self.speak_out(self.repos.zen())
            valid_command = True
        #__________________________________________________________________________
        
        #Process URL Request
        pos = 0 #holds the position of the keyword
        for key_word in command:
            if key_word in self.repos.url_request_keywords:
                self.process_URL(command, pos)
                valid_command = True
                break
            else:
                pos += 1

        #Process user asking for the time
        for key_word in command:
            if key_word in self.repos.time_keywords:
                self.process_time()
                valid_command = True
                break

        #Search the internet
        for key_word in command:
            if key_word in self.repos.search_keywords:
                self.process_search(command)
                valid_command = True
                break
        
        #Handle news requests 
        cont = any(item in self.repos.news_keywords for item in command)
        if cont:
            self.open_news()
            valid_command = True

        #Process a question
        cont = any(item in self.repos.query_keywords for item in command)
        if cont and valid_command is False:
            answer = self.tq.processQuestion(command)
            if answer == None:
                self.speak_out(self.repos.ques_prob_stmt)
            else:
                self.speak_out(answer)
            valid_command = True

        if valid_command == False:
            self.speak_out(self.repos.rep_stmt)