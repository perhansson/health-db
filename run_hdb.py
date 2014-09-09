#!/usr/bin/python
import sys
import getopt
import MySQLdb

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
    strFormat = "name,energy [kcal],carbs [g],protein [g],fat[g],comment"
    host="localhost"
    port=3306
    user="root"
    pw="pellestjej"
    dbname="hdb"
    tablename="foodtest"
    def __init__(self):
        """creating food"""
    def set(self,str):
        s = str.split(",")
        self.name = s[0]
        self.E = float(s[1])
        self.carbs = float(s[2])
        self.protein = float(s[3])
        self.fat = float(s[4])
        self.comment = s[5]
    def ok(self):
        """check if this is ok"""
        return True
    @staticmethod
    def printFoodList():
        foods = Food.getFoodList()
        s = ""
        i=0
        for food in foods:
            s += "[" + str(i) + "] "
            for col in food:
                s += str(col) + " "
            s += "\n" 
            i=i+1
        print "List of foods available (total %d): \n%s" % (len(foods),s)
    @staticmethod
    def getFoodList():
        sqlq = """SELECT * FROM foodtest"""
        db = MySQLdb.connect(host=Food.host, port=Food.port, user=Food.user, passwd=Food.pw, db=Food.dbname)
        cursor = db.cursor()
        data = None
        try:
            cursor.execute(sqlq)
            data = cursor.fetchall()
            #print "Result is %d long:" % len(data)
            #for row in data:
            #    print row
                #for col in row: 
                #    print col            
            #db.commit()
        except:
            db.rollback()
        db.close
        return data
    @staticmethod
    def getFood(food_id):
        sqlq = "SELECT id,name FROM foodtest WHERE id==%d" % food_id
        db = MySQLdb.connect(host=Food.host, port=Food.port, user=Food.user, passwd=Food.pw, db=Food.dbname)
        cursor = db.cursor()
        data = None
        try:
            cursor.execute(sqlq)
            data = cursor.fetchall()
            if len(data)>1:
                print "error, found %d foods for single id %d" % (len(data),id)
        except:
            db.rollback()
        db.close
        return data
    def addFoodToDB(self):
        sqlq = "INSERT INTO %s (name,energy,carbs,protein,fat,comment) VALUES (\"%s\",%f,%f,%f,%f,\"%s\")" % (Food.tablename,self.name,self.E,self.carbs,self.protein,self.fat,self.comment)
        db = MySQLdb.connect(host=Food.host, port=Food.port, user=Food.user, passwd=Food.pw, db=Food.dbname)
        cursor = db.cursor()
        data = None
        try:
            print sqlq
            cursor.execute(sqlq)
            db.commit()
        except:
            db.rollback()
        db.close


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
        if ans=="" or int(ans) not in self.D: return self.BADANSWER
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
        self.d = -1
    def pr(self):
        print "%s for %s:" % (self.D[self.d],self.person)
        for f in self.foodList:
            print f
    def process(self,ans):
        self.__init__()
        self.d = int(ans)
        print "Add a ", self.D[self.d], " meal by adding a set of food items."
        self.process_food()
        self.process_name()
        print "Current meal to be added to DB is:"
        self.pr()
        while True:
            ans = raw_input("Press Y/n to proceed and add meal to DB")
            if ans=="":
                print "cannot be empty"
                continue
            elif ans=="Y":
                print "this should add meal to DB!"
                break
            else:
                print "Not adding anyting"
                break
        print "done process return "
        return
    def process_name(self):
        ans = raw_input("Enter name (\'q\' to abort) here: ")
        if ans=="": 
            print "cannot be empty"
            self.process_name()
        self.person = ans
    def process_food(self):
        print "Select food item from list."
        Food.printFoodList()
        ans = raw_input("(\'a\' to add new food, \'q\' to abort or finish)\nInput here: ")
        if ans=="": 
            print "cannot be empty"
            self.process_food()
        elif ans=="q" or ans=="quit":
            return
        elif ans == "a" or ans == "add":
            print "Add new food item to DB\nData format:" + Food.strFormat
            ans = raw_input("(\'q\' to abort)\nInput string here: ")
            food = Food()
            food.set(ans)
            if food.ok():
                print "adding ", food.name, " to DB"
                food.addFoodToDB()
        else:
            food_id = int(ans)
            f = Food.getFood(food_id)
            if f!=None:
                print "invalid food id ", food_id
            else:
                self.foodList.append(food_id)
        self.process_food()

            

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
        if( ans==""):
            print "Cannot be empty"
            continue
        if( ans=="q" or ans=="quit"):
            break;
        if topLevel.check(ans) == topLevel.BADANSWER:
            print "Choose among the action list please."
            continue
        action = topLevel.process(ans)        
        action.build()
        ans = raw_input(action.Q)
        if( ans=="q" or ans=="quit"):
            continue
        if action.check(ans) == action.BADANSWER:
            print "Choose among the types listed please."
            continue
        action.process(ans)
        print "action process done, now Q is ", action.Q
        
    
            
        
    print "==== End =================="
    print "==========================="

