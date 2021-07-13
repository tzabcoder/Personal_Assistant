from VoiceHandling import Handler
from Response_Reposititory import Repository
from Face_Recognizer import FaceRecognizer

#Main function handles program logic flow
def main():
    handler = Handler()
    repos = Repository()
    
    try:
        face_rec = FaceRecognizer()
        name = face_rec.process_face()
        if name == -1:
            response = handler.unknown_user()
            #get the image of the person
            #then store the image of the person as their name
        elif name == 0:
            handler.greeting()
        else:
            handler.welcome_user(name) 
    except:
        handler.greeting()

    speak = True 
    while speak: #Continue to process more requests
        print("Listening...")

        command = handler.talk_in() #Get the user command  
        handler.parse_command(command) #Parse the user command 

        handler.speak_out(repos.get_next_stmt()) #prompt for more commands

if __name__ == '__main__': 
    main()