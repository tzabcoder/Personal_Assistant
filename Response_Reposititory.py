import random
from datetime import datetime

class Repository:
    greeting_am = "Good morning"
    greeting_noon = "Good afternoon"
    greeting_pm = "Good evening"

    unknown_user_stmt = "I do not seem to recognize you. What is your name?"

    urlprob_stmt = "I couldn't seem to find that site"
    help_stmt = "My name is Reach, how may I help you?"
    next_stmt1 = "What else may I help you with?"
    next_stmt2 = "How else may I assist you?"
    next_stmt3 = "Any other requests?"
    end_stmt = "Looking forward to helping again!"
    rep_stmt = "I didn't get that, please say that again"
    time_stmt = "The current time is "
    rephow_stmt = "I am well thank you. I am ready to serve your inquiries."
    repwho_stmt = "My name is Reach. I exist as 1s and 0s in your computer. But don't let that fool you, I am an abstraction from my creators imagination."
    cando_stmt = "I can do many things. I can answer questions to math and geography questions. I can process search requests, open browsers, and I can tell you the time. "
    lang_stmt = "I am programmed purely in Python."
    ques_prob_stmt = "I was unable to process that question."

    #Precessed Statements 
    news_proc = "Here is today's most current events."
    search_proc = "Here is what I found."
    url_proc = "Going there now."

    url_request_keywords = ["go", "visit", "open"]
    terminate_keywords = ["exit", "nothing", "terminate", "end", "goodbye", "bye", "stop", "no"]
    #for searching the internet
    search_keywords = ["search", "look", "show"]
    time_keywords = ["time"]
    ask_keywords = ["how", "are", "you"]
    id_keywords = ["who", "are", "you"]
    cando_keywords = ["what", "can", "you", "do"]
    lan_keywords = ["what", "language", "you", "in"]
    whylan_keywords = ["why", "you", "in", "python"]
    #Query Keywords
    query_keywords = ["who", "what", "where", "when", "why", "how"]
    #News keywords
    news_keywords = ["news"]

    #Code Generation Keywords
    define_keywords = ["define", "declare"]
    print_keywords = ["output", "print", "display"]

    def welcome_name(self, name):
        user_greeting = f"{self.get_greet()}. Welcome back {name}. How may I help you?"
        return user_greeting

    def get_greet(self):
        """Returns a greeting based on the time of day"""
        curr_time = self.get_current_time()

        if curr_time >= 0 and curr_time < 120000:
            return self.greeting_am
        elif curr_time >= 120000 and curr_time <= 165900:
            return self.greeting_noon
        elif curr_time >= 170000:
            return self.greeting_pm

    #Return the greeting based on the time of day
    def return_greeting(self):
        """Returns a greeting based on the time of day"""
        curr_time = self.get_current_time()

        if curr_time >= 0 and curr_time < 120000:
            return self.greeting_am + self.help_stmt
        elif curr_time >= 120000 and curr_time <= 165900:
            return self.greeting_noon + self.help_stmt
        elif curr_time >= 170000:
            return self.greeting_pm + self.help_stmt

    #Randomy generate the next statement
    def get_next_stmt(self):
        next_num = random.randint(1, 3)
        if next_num == 1:
            return self.next_stmt1
        if next_num == 2:
            return self.next_stmt2
        if next_num == 3:
            return self.next_stmt3
    
    #Get the current time 
    def get_current_time(self):
        now = datetime.now()

        time = now.strftime("%H:%M:%S")
        time = time.replace(":", '')
        time = int(time)

        return time

    #Zen of python (by Tim Peters)
    def zen(self):
        return "Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex. Complex is better than complicated. Flat is better than nested. Sparse is better than dense. Readability counts. Special cases aren't special enough to break the rules. Although practicality beats purity. Errors should never pass silently. Unless explicitly silenced. In the face of ambiguity, refuse the temptation to guess. There should be one and preferably only one obvious way to do it. Although that way may not be obvious at first unless you're Dutch. Now is better than never. Although never is often better than right now. If the implementation is hard to explain, it's a bad idea. If the implementation is easy to explain, it may be a good idea. Namespaces are one honking great idea, let's do more of those!"