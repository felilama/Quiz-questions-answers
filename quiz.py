import random

class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer 
        
    
    def ask_and_check(self):

        print(self.question)
        answer = input("What is your answer? ")
        if(answer == self.answer): 
            print("Correct !")
        else:
            print("Sorry no. Correct answer is:",self.answer)   
        
        return (answer == self.answer)

class WrongAnswer():
    def __init__(self,string_answer):
        self.value = string_answer
        self.choosen_times = 0
        self.displayed = 0
    
    def __str__(self):
        return self.value

    def score(self):
        return (2 * self.choosen_times + 1 ) / (self.displayed + 1)
        

class MCQuestion (Question):
    ALTERNATIVES_NUMBER = 7
    def __init__(self, question, answer, wrong_answers = None):
        super().__init__(question, answer)
        if(wrong_answers != None):
            self.wrong_answers = [WrongAnswer(string_value) for string_value in wrong_answers]
        else:
            self.wrong_answers = []
    
    def ask_and_check(self):
        print(self.question)
        choices = sorted(self.wrong_answers,key = lambda x : x.score(), reverse = True)[:self.ALTERNATIVES_NUMBER-1]
        choices.insert(random.randrange(0,len(choices)),self.answer)
        for i in range(len(choices)):
            print(f'{i+1}: {choices[i]}')
            if (type(choices[i]) is WrongAnswer):
                choices[i].displayed += 1
        answer = int(input("What is your answer? "))  

        if(answer > 0  and answer <= len(choices)):
            if(choices[answer-1] == self.answer): 
                print("Correct!")
            else:
                print("Sorry no. Correct answer is:",self.answer)
                choices[answer-1].choosen_times += 1   
        else:
                print("Sorry. This is not an acceptable answer number")
                return False

        return (choices[answer-1] == self.answer)
    
    def add_wrong(self,answer):
        self.wrong_answers.append(WrongAnswer(answer))
     

class Quiz:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def do(self):
        correctly_answered = 0
        for q in self.questions:
            correctly_answered = correctly_answered + 1 if q.ask_and_check() else correctly_answered 
        
        print("You answered",str(correctly_answered), "of",len(self.questions),"correctly")
        return correctly_answered
    def do_until_right(self):
        while(True):
           correctly_answered = self.do()  
           if(correctly_answered == len(self.questions)):
               break

def create_quiz_from_file(filename):
    with open(filename, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            command, data = line.split(' ', 1)
            data = data.strip()
            if command == 'name':
                quiz = Quiz(data)
            elif command == 'q':
                text = data
            elif command == 'a':
                question = Question(text, data)
                quiz.add_question(question)
            elif command == 'mca':
                question = MCQuestion(text, data)
                quiz.add_question(question)
            elif command == 'w':
                question.add_wrong(data)
    return quiz

q = Question('Dog in Swedish?', 'hund')
q3 = MCQuestion('Capital of Sweden?',
'Stockholm',["Tierp","Uppsala"])

quiz = Quiz('Example quiz')
quiz.add_question(q3)
quiz.add_question(q)

quiz.do_until_right()
dquiz = create_quiz_from_file("marvels.quiz")
dquiz.do()
