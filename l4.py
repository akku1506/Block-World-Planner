import sys
import time
import random
from heapq import *


argType=['variable','terminal']

checkArg=['positive','negative']

propositionList=['on','ontable','clear','hold','empty']
actionList=[]
blocks=[]
method=''

def gettingAllActions():
	preconditionList=[]
	effectList=[]
	preconditionList.append(Sentence(propositionList[1],[Argument('block',argType[0], 0)],0))
	preconditionList.append(Sentence(propositionList[2],[Argument('block',argType[0],0)],0))
	preconditionList.append(Sentence(propositionList[4], [],0))
	effectList.append(Sentence(propositionList[3],[Argument('block',argType[0],0)],0))
	effectList.append(Sentence(propositionList[2],[Argument('block',argType[0],0)], 1))
	effectList.append(Sentence(propositionList[1],[Argument('block',argType[0],0)], 1))
	effectList.append(Sentence(propositionList[4], [], 1))	

	actionList.append(Action('pick', ['block'],preconditionList,effectList))

	preconditionList=[]
	effectList=[]

	preconditionList.append(Sentence(propositionList[0],[Argument('blocka',argType[0], 0),Argument('blockb',argType[0], 0)],0))
	preconditionList.append(Sentence(propositionList[2],[Argument('blocka',argType[0], 0)],0))
	preconditionList.append(Sentence(propositionList[4], [],0))
	effectList.append(Sentence(propositionList[3],[Argument('blocka',argType[0],0)],0))
	effectList.append(Sentence(propositionList[2],[Argument('blockb',argType[0],0)], 0))
	effectList.append(Sentence(propositionList[0],[Argument('blocka',argType[0],0),Argument('blockb',argType[0],0)], 1))
	effectList.append(Sentence(propositionList[2],[Argument('blocka',argType[0], 0)],1))
	effectList.append(Sentence(propositionList[4], [], 1))	
	
	actionList.append(Action('unstack',['blocka','blockb'], preconditionList, effectList))
	
	preconditionList=[]
	effectList=[]

	preconditionList.append(Sentence(propositionList[3],[Argument('block',argType[0],0)],0))
	effectList.append(Sentence(propositionList[1],[Argument('block',argType[0],0)], 0))
	effectList.append(Sentence(propositionList[2],[Argument('block',argType[0],0)], 0))
	effectList.append(Sentence(propositionList[3],[Argument('block',argType[0],0)],1))	
	effectList.append(Sentence(propositionList[4], [], 0))

	actionList.append(Action('release',['block'], preconditionList, effectList))

	preconditionList=[]
	effectList=[]

	preconditionList.append(Sentence(propositionList[2],[Argument('blockb',argType[0], 0)],0))
	preconditionList.append(Sentence(propositionList[3],[Argument('blocka',argType[0],0)],0))
	effectList.append(Sentence(propositionList[0],[Argument('blocka',argType[0],0),Argument('blockb',argType[0],0)], 0))
	effectList.append(Sentence(propositionList[2],[Argument('blocka',argType[0],0)], 0))
	effectList.append(Sentence(propositionList[3],[Argument('blocka',argType[0],0)],1))	
	effectList.append(Sentence(propositionList[2],[Argument('blockb',argType[0],0)], 1))
	effectList.append(Sentence(propositionList[4], [], 0))

	actionList.append(Action('stack',['blocka','blockb'], preconditionList, effectList))
	#print actionList

def bfs(initialState,goalState):	
	
	queue=[]
	noOfExpandedNodes=0
	queue.append(initialState)
	
	while queue:
		currState=queue.pop(0)
		#print "new queue is",queue
		#print "Searching at",currState.depth

		if currState.isGoal(goalState):
			#print "goal"
			#print str(currState)
			return noOfExpandedNodes,currState
			
		noOfExpandedNodes=noOfExpandedNodes+1

		newStateList=currState.getNewState()	
		for newState in newStateList:
			queue.append(newState)
			newState.prevState=currState
			newState.depth=currState.depth+1
			#print str(newState)
					            
	return -1,-1



def aStar(initialState,goalState):

	queue=[]
	noOfExpandedNodes=0
	heappush(queue,(initialState.depth+initialState.heuristic,initialState))

	while queue:
		currHeapElement=heappop(queue)
		currState=currHeapElement[1]
		#print "curr",str(currState)
		if currState.isGoal(goalState):
			return noOfExpandedNodes,currState
		#print 'currState'
		#print str(currState)
		noOfExpandedNodes=noOfExpandedNodes+1
		newStateList=currState.getNewState()
		#for newState in newStateList:
		#	print "neighbours:"+str(newState)
		#sys.exit(0)
		#for neighborState in newStateList:
		#	print 'neighbouts'
		#	print str(neighborState)			
		for newState in newStateList:
			newState.prevState=currState
			newState.depth=currState.depth + 1
			newState.assigningHeuristic(goalState)

			heappush(queue,(newState.depth+newState.heuristic,newState))

	return -1,-1	


def gsp(startState, goalState):
	
	planList = []
	stack = []
	currentState = State(startState.sentenceList, startState.groundList)

	stack.append(goalState.sentenceList)
	for sentence in goalState.sentenceList:
		stack.append([sentence])

	while stack:
		# print("***new***")
		# printList(stack)
		poppedElement = stack.pop()

		if type(poppedElement) is list:

			if not currentState.hasSentence(poppedElement):

				if len(poppedElement) > 1:
					stack.append(poppedElement)
					random.shuffle(poppedElement)
					for sentence in poppedElement:
						stack.append([sentence])

				else:
					newGoalsData = poppedElement[0].getNewGoals(currentState)

					if newGoalsData == None:
						stack = []
						currentState = State(startState.sentenceList, \
								startState.groundList)
						planList = []
						stack.append(goalState.sentenceList)
						for sentence in goalState.sentenceList:
							stack.append([sentence])
						continue

					actionDict = dict()
					actionDict['action'] = newGoalsData['action']
					actionDict['assignment'] = newGoalsData['assignment']
					stack.append(actionDict)
					stack.append(newGoalsData['sentenceList'])
					for sentence in newGoalsData['sentenceList']:
						stack.append([sentence])
		else:
			action = poppedElement['action']
			assignment = poppedElement['assignment']
			currentState = getStates(currentState,action, assignment)
			planList.append(poppedElement)
			# printDict(poppedElement)

	return planList	

class Action:

	def __init__(self,name,args,preconditionList,effectList):

		self.name = name
		self.arguments = args
		self.preconditionList = list(preconditionList)
		self.effectList = list(effectList)
		self.variableList = []

		for precondition in preconditionList:
			for arg in precondition.arguments:
				flag=0
				for varArg in self.variableList:
					if varArg.argType==arg.argType and varArg.argValue==arg.argValue and varArg.isPositive==arg.isPositive:
						flag=1
						break
				if flag==0:
					self.variableList.append(arg)

	def __str__(self):

		string=""
		string=string+'Action: '+self.name +'\n'+'Precondition: '
		for conjucts in self.preconditionList:
			string=string+str(conjucts)
		string=string+"\n"+'Effect: '
		for conjucts in self.effectList:
			string=string+str(conjucts)
		string=string+'\n'
		return string

class State:

	def __init__(self, sentenceList, groundList):
		self.sentenceList = list(sentenceList)
		self.groundList = list(groundList)
		self.depth = 0
		self.heuristic = 0
		self.prevState = None
		self.prevActionInstr = ''


	def __str__(self):	
		string=''
		for sentence in self.sentenceList:
			string=string+str(sentence)+'\n'
		string=string+'Previous Action : '+self.prevActionInstr+'\n'#+str(self.prevAction)		

		return string		

	def isGoal(self, goalState, heuristicValue=0):

		if not heuristicValue:

			first=self.sentenceList
			second=goalState.sentenceList
			if not len(first) == len(second):
				return 0

			dupFirst = list(first)
			dupSecond = list(second)

			for item in dupFirst:
				flag = 0
				itemInList = None
				for other in dupSecond:
					if item.propositionType==other.propositionType and item.isPositive==other.isPositive and compareList(list(item.arguments),list(other.arguments)):	
						flag=1
						itemInList = other
						break

				if flag==0:
					return 0

				dupSecond.remove(itemInList)

			return 1


		elif heuristicValue:
			return self.hasSentence(goalState.sentenceList)

	def hasSentence(self, sentenceList):

		for sentence in sentenceList:
			flag=0
			for stateSentence in self.sentenceList:
				if stateSentence.propositionType==sentence.propositionType and stateSentence.isPositive==sentence.isPositive and compareList(list(stateSentence.arguments),list(sentence.arguments)):	
					flag=1
					break
			if flag==0:
				return flag
		return 1

	def getNewState(self, heuristicValue=0):

		newList = []

		for action in actionList:
			newList.extend(getStatesOnAction(self,action,[],{},heuristicValue))

		return newList


	def assigningHeuristic(self, goalState):

		currState = State(self.sentenceList, self.groundList)
		goalSentence=list(goalState.sentenceList)
		count = 0
		while (1<2):
			for action in actionList:
				stateList=getStatesOnAction(currState,action,[],{},1)
				#print "states are"
				#for i in stateList:
				#	print str(i)+"\n\n\n"
				#sys.exit(0)	
				if stateList:
					currState=stateList[0]

				count=count+1
				#print "outside"
				if currState.hasSentence(goalSentence):
					#print "inside"
					#sys.exit(0)
					self.heuristic=count
					return
		# self.heuristic = currState.heuristic
		self.heuristic = count

	def getPathtoGoal(self):
		currState=self
		allPath=[]
		while currState:
			allPath.append(currState)
			currState=currState.prevState

		return allPath	


class Sentence:

	def __init__(self,propositionType,arguments,isPositive):

		self.propositionType = propositionType
		self.arguments = arguments
		self.isPositive = isPositive


	def __str__(self):

		string=''
		if self.isPositive==1:
			string=string+'~'

		string=string+'('+self.propositionType
		for arg in self.arguments:
			string=string+' '
			string=string+str(arg)
		string=string.strip()
		string=string+')'
		return string

	def getNewGoals(self, currState):

		newDict = {}
		assignment = {}
		possibleActions = []
		

		pickAction = actionList[0]
		unstackAction = actionList[1]
		releaseAction = actionList[2]
		stackAction = actionList[3]

		possibleassignment = list(currState.groundList)
		if self.propositionType == propositionList[0]:
			nextAction = stackAction
		elif self.propositionType == propositionList[1]:
			nextAction = releaseAction
		elif self.propositionType == propositionList[2]:
			checkSentence = Sentence(propositionList[3], self.arguments, 0)
			if currState.hasSentence([checkSentence]):
				nextAction = releaseAction
			else:
				nextAction = unstackAction
		elif self.propositionType == propositionList[3]:
			checkSentence = Sentence(propositionList[1], self.arguments, 0)
			if currState.hasSentence([checkSentence]):
				nextAction = pickAction
			else:
				nextAction = unstackAction

		elif self.propositionType == propositionList[4]:
			nextAction = releaseAction

		else:
			return None

		for trueSentence in nextAction.effectList:
			if trueSentence.propositionType == self.propositionType and self.isPositive == trueSentence.isPositive:
				for ii in range(len(self.arguments)):
					assignment[trueSentence.arguments[ii].argValue] = self.arguments[ii]
				if nextAction == unstackAction:
					if self.propositionType == propositionList[3]:
						for terminal in possibleassignment:
							checkSentence = Sentence(propositionList[0], [self.arguments[0], terminal], 0)
							if currState.hasSentence([checkSentence]):
								possibleassignment = [terminal]
								break
					elif self.propositionType == propositionList[2]:
						for terminal in possibleassignment:
							checkSentence = Sentence(propositionList[0], [terminal, self.arguments[0]], 0)
							if currState.hasSentence([checkSentence]):
								possibleassignment = [terminal]
								break
					else:
						return None
				elif self.propositionType == propositionList[4]:
					for terminal in possibleassignment:
							checkSentence = Sentence(propositionList[3], [terminal], 0)
							if currState.hasSentence([checkSentence]):
								possibleassignment = [terminal]
								break

				break

		newDict['action'] = nextAction

		for arg in nextAction.variableList:
			if not assignment.has_key(arg.argValue):
				if len(possibleassignment) == 0:
					break
				randomIndex = random.randrange(0, len(possibleassignment))
				assignment[arg.argValue] = possibleassignment[randomIndex]
				possibleassignment.pop(randomIndex)

		newDict['assignment'] = assignment

		retTrueList = []
		for trueSentence in nextAction.preconditionList:
			assignedSentence = Sentence(trueSentence.propositionType, trueSentence.arguments, trueSentence.isPositive)
			newarguments = []
			for arg in assignedSentence.arguments:
				if arg.argType == argType[0]:
					newarguments.append(assignment[arg.argValue])
				else:
					newarguments.append(arg)
			assignedSentence.arguments = newarguments
			retTrueList.append(assignedSentence)

		newDict['sentenceList'] = retTrueList

		return newDict


class Argument:

	def __init__(self,argValue,argType,isPositive,):

		self.argType = argType
		self.argValue = argValue
		self.isPositive = isPositive

	def __str__(self):

		string=""
		if self.isPositive==1:
			string=string+"~"
		string=string+str(self.argValue)
		return string	
	
def getStates(stateObj,actionObj,assignment,heuristicValue=0):
	newState = State(stateObj.sentenceList,stateObj.groundList)
	for trueSentence in actionObj.effectList:
		newTrueSentence = Sentence(trueSentence.propositionType, [],0)
		groundList = []
		for variable in trueSentence.arguments:
			savedArg = assignment[variable.argValue]
			groundList.append(savedArg)

		newTrueSentence.arguments = groundList
		if trueSentence.isPositive:
			if not heuristicValue:
				#newState.removeTrueSentence(newTrueSentence)
				temp=[]
				for sentence in newState.sentenceList:
					if (newTrueSentence.propositionType!=sentence.propositionType or newTrueSentence.isPositive!=sentence.isPositive or not(compareList(list(sentence.arguments),list(newTrueSentence.arguments)))):
						temp.append(sentence)	
				newState.sentenceList=temp				
		else:
			addSentence(newState,newTrueSentence)
	if heuristicValue:
		newState.heuristic = stateObj.heuristic + 1
	argumentsString = ''
	for arg in actionObj.arguments:
		argumentsString += ' ' + str(assignment[arg])

	newState.prevActionInstr = '(' + actionObj.name + argumentsString + ')'

	return newState


def getStatesOnAction(stateObject,actionObj,newList,assignment,heuristicValue=0):

	variablesList=actionObj.variableList	
	if len(variablesList) == 0:

		effectList = []
		for trueSentence in actionObj.effectList:
			positivegroundList = []
			if trueSentence.isPositive:
				continue
			for variable in trueSentence.arguments:
				positivegroundList.append(assignment[variable.argValue])
			effectList.append(Sentence(trueSentence.propositionType,positivegroundList,0))

		if stateObject.hasSentence(effectList):
			return newList

		groundTermTrueSentencesList = []
		for trueSentence in actionObj.preconditionList:
			groundList = []
			for variable in trueSentence.arguments:
				groundList.append(assignment[variable.argValue])
			groundTermTrueSentencesList.append(Sentence(trueSentence.propositionType,groundList,0))

		if stateObject.hasSentence(groundTermTrueSentencesList):
			if not heuristicValue:
				newList.append(getStates(stateObject,actionObj,
								   assignment, heuristicValue))
			else:
				stateObject = getStates(stateObject,actionObj,assignment, heuristicValue)
				newList = [stateObject]
		return newList


	thisVariable = variablesList.pop()
	for groundTerm in stateObject.groundList:
		assignment[thisVariable.argValue] = groundTerm
		newList = getStatesOnAction(stateObject,actionObj,newList, assignment,heuristicValue)
		if heuristicValue and newList:
			stateObject = newList[0]
		assignment.pop(thisVariable.argValue)

	variablesList.append(thisVariable)
	return newList

	
def addSentence(stateObj, sentence):

	for arg in sentence.arguments:
		if arg.argType==argType[0]:
			return

	for arg in sentence.arguments:
		flag=0
		for varArg in stateObj.groundList:
			if varArg.argType==arg.argType and varArg.argValue==arg.argValue and varArg.isPositive==arg.isPositive:
				flag=1
				break
		if flag==0:
			stateObj.groundList.append(arg)

	stateObj.sentenceList.append(sentence)

def compareList(first,second):

    if not len(first) == len(second):
        return 0

    for i,item in enumerate(first):
        if item.argValue!=second[i].argValue or item.argType!=second[i].argType or item.isPositive!=second[i].isPositive:       
            return 0
    return 1


def gettingState(file):

	propositionPositive=0
	lines=file.readline().strip()
	words=lines.split(" ")
	#sentenceList=[]
	proposition=""
	newState=State([],[])
	#print "values is "+str(blocks[0].isPositive)
	for word in words:

		if word[0]=='(':
			arguments=[]
			proposition=word[1:len(word)]
			proposition=proposition.strip(')')					
		else:
			argValue=int(word.strip(')'))
			arguments.append(blocks[argValue-1])

		if word[len(word)-1]==')':
			#sentenceList.append(Sentence(proposition,arguments,propositionPositive))		
			#newState.addTrueSentence(TrueSentence(proposition,arguments,propositionPositive))
			addSentence(newState,Sentence(proposition,arguments,propositionPositive))
	#return State(sentenceList)
	return newState

######main function


if len(sys.argv) < 2:
	print 'Invalid/insufficient arguments!'
	sys.exit(0)


filename=sys.argv[1]
file=open(filename,"r")

lines=file.readline().strip()
try:
	numberOfBlocks=int(lines)
except:
	print "Enter a number"
	sys.exit(0)


methodList=['f','a','g']	
lines=file.readline().strip()
if lines not in methodList:
	print "Enter a valid method"
	sys.exit(0)	
method=lines


lines=file.readline().strip()
if lines!="initial":
	print "Initial state not given"
	sys.exit(0)


arg=argType[1]
#as initial state would always contain only positive ground terms
propositionPositive=0
for i in range(1,numberOfBlocks+1):
	blocks.append(Argument(i,arg,propositionPositive))

initState=gettingState(file)

"""
print "initial"
for sentence in initState.sentenceList:
	print sentence.proposition
"""
lines=file.readline().strip()
if lines!="goal":
	print "Goal state not given"
	sys.exit(0)

goalState=gettingState(file)

gettingAllActions()
outputString=''
noOfActions=0
initTime=time.time()
if method=='f':
	#print "bfs"
	noOfExpandedNodes,goalState=bfs(initState,goalState)
	print "Number of nodes expanded are:  "+str(noOfExpandedNodes)
	print "\n"
	totalPath=goalState.getPathtoGoal()
	#for state in totalPath:
	
	state=totalPath.pop()
	while(state):
		outputString=outputString+state.prevActionInstr+"\n"
		if totalPath:
			state=totalPath.pop()
		else:
			state=None	
	#print outputString
	noOfActions=str(goalState.depth).strip()	
	print "Goal state found at depth:  ",goalState.depth
	print "\n"
elif method=='a':
	noOfExpandedNodes,goalState=aStar(initState,goalState)
	print "Number of nodes expanded are:  "+str(noOfExpandedNodes)
	print "\n"
	
	totalPath=goalState.getPathtoGoal()
	#for state in totalPath:
	
	state=totalPath.pop()
	while(state):
		outputString=outputString+state.prevActionInstr+"\n"
		if totalPath:
			state=totalPath.pop()
		else:
			state=None	
	#print outputString
	noOfActions=str(goalState.depth).strip()	
	print "Goal state found at depth:  ",goalState.depth
	print "\n"	
	#print "astar"
	
elif method=='g':	
	gspPlan = gsp(initState, goalState)
	for plan in gspPlan:
		action = plan['action']
		assignment = plan['assignment']
		argumentsString = ''
		for arg in action.arguments:
			argumentsString += ' ' + str(assignment[arg])
		outputString += '(' + action.name + argumentsString + ')' + '\n'
	noOfActions = len(gspPlan)
	noOfExpandedNodes= -1
	print "Number of nodes expanded are:  "+"Not Applicable"
	print "\n"
	print "Goal state found at depth:  ", noOfActions
	print "\n"

else:
	print "Invalid Planner"	

file=open('output.txt','w')
file.write(str(noOfActions)+'\n')
file.write(outputString.strip())
file.close()	
endTime=time.time()
print "Time taken:  "+str(endTime-initTime)