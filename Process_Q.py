import wolframalpha
from Response_Reposititory import Repository

"""
Technical questions handles the following main question types:
-Music
-Astronomy
-Weather/Meteorology
-Health/Medicine
-Engineering
-Food/Nutrition
-Sports/Games
-Web/Computer Systems
-Math
-Physics
(any many more)
"""
class TechnicalQuestions:
    app_id = "JPE32H-PLR8R9RJ88"
    client = wolframalpha.Client(app_id) #Create the wolfphramalpha client
    question = ""
    repos = Repository()

    def processQuestion(self, command):
        self.question = ""
        query_pos = 0
        cmd_len = len(command)

        #First search for the query word. Then form the question
        for word in command:    
            if word in self.repos.query_keywords: #if the word is a query word
                break #save the query position
            else: 
                query_pos = query_pos + 1 #otherwise increase the query position

        #Formulate the question based off of the query word location
        cont = True
        while cont:
            if query_pos == cmd_len:
                cont = False
            else:
                self.question = self.question + " " + command[query_pos] #create the question

            query_pos += 1

        try:
            result = self.client.query(self.question) #ask the question to wolframalpha
            answer = next(result.results).text #turn the answer into text
            return answer
        except: #handle API errors 
            return None