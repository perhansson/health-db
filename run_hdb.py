#!/usr/bin/python
import sys
import getopt

def usage():
    print "Usage: ",sys.argv[0], " [hd]"


def parseArgs(argv):
    try:
        opts, args = getopt.getopt(argv,"hd", ["help","debug"])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()                     
            sys.exit()                  
        elif opt == '-d':
            global _debug               
            _debug = 1                  

class Food:
    strFormat = "<name>,<amount>,<amount unit>,<energy> [kcal],carbs [g],protein [g],fat[g],comment"
    def __init__(self,str):
        self.identifier = ""
        self.name = ""
        self.amount = 0.0
        self.amount_unit = ""
        self.E = 0.0
        self.carbs = 0.0
        self.protein = 0.0
        self.fat = 0.0
        self.comment = ""
        self.parse(str)
    def parse(self,str):
        print "should parse the input data here"
    def ok(self):
        """check if this is ok"""
        return True


class ActionType:
    BADANSWER = 1    
    GOODANSWER = 0    
    def __init__(self):
        self.name = ""    
        self.Q = ""
        self.D = {}
        self.d = -1
    def build(self):
        s = "Choose " + self.name + ":\n"
        for k,v in self.D.iteritems():
            s += "[" + str(k) + "] " + v + "\n"
        s += "(press \'q\' to abort)\n" 
        self.Q = s
    def check(self,ans):
        if int(ans) not in self.D: return self.BADANSWER
        else: return self.GOODANSWER
    def process(self,ans):
        self.d = int(ans)
        print "This is where I should read in a ",self.d," to the DB..."
    

    
class Meal(ActionType):
    def __init__(self):
        ActionType.__init__(self)
        #ActionType.__init__(self)
        self.name = "meal"    
        self.D = {0:"breakfast",1:"lunch",2:"dinner",3:"generic"}
        self.foodList = []
    def process(self,ans):
        self.d = int(ans)
        print "Add a ", self.D[self.d], " meal by adding a set of food items."
        self.process_food()
    def process_food(self):
        print "Add food item.\nData format:"
        print Food.strFormat
        ans = raw_input("(\'q\' to abort)\nInput string here: ")
        if( ans=="q" or ans=="quit"):
            return
        food = Food(ans)
        if food.ok():
            print "adding ", food.name
            self.foodList.append(food)
        else:
            print "Something is wrong, not adding this food"
        process_food()

            

class Exercise(ActionType):
    def __init__(self):
        ActionType.__init__(self)
        self.name = "exercise"
        self.D = {0:"generic"}



class Action(ActionType):
    def __init__(self):
        ActionType.__init__(self)
        self.name = "action"
        self.D = {0:"Add meal",1:"Add Exercise"}
        print "end of init action with name ", self.name
    def process(self,ans):
        self.d = int(ans)
        r = None
        if self.d == 0:
            r = Meal()
        elif self.d == 1:
            r = Exercise()
        else:
            print "this answer ", ans, " is not ok!? "
            sys.exit(1)
        return r


if __name__ == "__main__":
    parseArgs(sys.argv[1:])
    
    print "==========================="
    print "==== Start ================"

    topLevel = Action()
    topLevel.build()


    while( True ):
        ans = raw_input(topLevel.Q)
        print "Your answer: ", ans
        if( ans=="q" or ans=="quit"):
            break;
        if topLevel.check(ans) == topLevel.BADANSWER:
            print "Choose among the action list please."
            continue
        action = topLevel.process(ans)        
        action.build()
        while( True ):
            ans = raw_input(action.Q)
            if( ans=="q" or ans=="quit"):
                break;
            if action.check(ans) == action.BADANSWER:
                print "Choose among the types listed please."
                continue
            action.process(ans)
    
    
            
        
    print "==== End =================="
    print "==========================="

