"""Python Helper for Alexa.  Allows a beginner to write Python code
calling print(), input(), random and time.  Repeats their values as
necessary to restore state for further interactions.
Version 1.2 (c) Silas S. Brown 2025.  No warranty.

To deploy to your Alexa devices: Go to developer.amazon.com to add
the developer role to your Amazon account, and under "Alexa Skills
Kit" Console use "Create Skill", name it, set model type to "Custom",
hosting type to "Alexa-hosted (Python)", template start from scratch
then under "Interaction Model" choose "JSON Editor" and paste this:

{"interactionModel": { "languageModel": {
     "invocationName": "python helper",
     "intents": [
       {"name": "InputIntent","slots": [{"name": "UserInput","type": "AMAZON.SearchQuery"}],"samples": ["answer {UserInput}"]},
       {"name": "AMAZON.HelpIntent",  "samples": []},
       {"name": "AMAZON.CancelIntent","samples": []},
       {"name": "AMAZON.StopIntent",  "samples": []}], "types":[]},
     "prompts":[{"id":"1","variations":[{"type":"PlainText","value":"Waiting for input"}]}],
     "dialog": {"intents": [{"name": "InputIntent","confirmationRequired": false,"prompts": {},"slots":[{"name": "UserInput","type":"AMAZON.SearchQuery","confirmationRequired": false,"elicitationRequired": true,"prompts":{"elicitation":"1"}}]}],"delegationStrategy": "SKILL_RESPONSE"}}}

Save and Build, then under "Code" replace all the content with this
file, Save and Deploy, then under Test enable testing and try saying
"open Python Helper".
You should be able to answer your program's questions just by speaking.
If that doesn't work, try saying the word "answer" before your answer.

If there's an error go back to Code and check under CloudWatch Logs.
"""

import time,random,inspect,sys,re
class FunctionWrapper:
  def __init__(self): self.logs = {}
  def wrapF(self,func,call_real_again = False):
    k = f"{func.__module__}.{func.__name__}"
    def iterator(args,kw):
        self.logs.setdefault(k,[])
        for i in self.logs[k]:
            if call_real_again: func(*args,**kw)
            args,kw=(yield i)
        while True:
            i = func(*args,**kw)
            self.logs[k].append(i)
            args,kw=(yield i)
    it = []
    def newFunc(*args,**kw):
        if it: return it[0].send((args,kw))
        it.append(iterator(args,kw))
        return it[0].send(None) # 1st value
    newFunc.oldFunc=func
    return newFunc
  def wrapM(self,module,again=False):
    for n,m in inspect.getmembers(module,lambda x:any(f(x) for f in [inspect.isfunction,inspect.ismethod,inspect.isbuiltin])):
      setattr(module,n,self.wrapF(m,again))
  def unwrapM(self,module):
    for n,m in inspect.getmembers(module,inspect.isfunction): setattr(module,n,m.oldFunc)
fw = FunctionWrapper()
def print(*P): fw.outBuf.append(' '.join(f'{a}'for a in P))
def input(prompt=None):
  if prompt is not None: print(prompt)
  fw.inputWait = True ; sys.exit()
def wrapPrintInput():
  try:    __builtins__.print   =fw.wrapF(print)
  except: __builtins__['print']=fw.wrapF(print)
  try:    __builtins__.input   =fw.wrapF(input)
  except: __builtins__['input']=fw.wrapF(input)

def lambda_handler(event, context):
  fw.outBuf,fw.inputWait,fw.logs = [],False,{}
  if event['session'].get('new',False): fw.outBuf=["Python program starting."]
  else: fw.logs=event['session']['attributes']
  shouldRun = True
  if event['request']['type']=='IntentRequest':
    iName = event['request']['intent']['name']
    if iName == 'InputIntent': fw.logs.setdefault(__name__+'.input',[]).append(re.sub('^[aA]nswer ','',event['request']['intent']['slots'].get('UserInput', {}).get('value','')))
    elif iName == 'AMAZON.HelpIntent': fw.outBuf.append("Speak the input to your program.")
    elif iName == 'AMAZON.StopIntent' or iName == 'AMAZON.CancelIntent': shouldRun = False
  if shouldRun:
    fw.wrapM(time),fw.wrapM(random,True),wrapPrintInput()
    try: exec(user_code,{})
    except SystemExit: pass
    except Exception as e: fw.outBuf += [f"Unhandled {type(e)} {e}"]
    fw.unwrapM(time),fw.unwrapM(random)
  if fw.inputWait:
    if not fw.outBuf: fw.outBuf=["Waiting"]
  else: fw.outBuf += ["Program terminated"]
  r={'version': '1.0','response':{'outputSpeech': {
       'type':'PlainText','text':'\n'.join(fw.outBuf)},
      "reprompt":{"outputSpeech":{"type":"PlainText",
        "text":'\n'.join([i for i in fw.outBuf if i.strip()][-1:])}},
      'shouldEndSession': not fw.inputWait}}
  if fw.inputWait: r['response']['directives'],r['sessionAttributes']=[{"type":"Dialog.ElicitSlot","slotToElicit":"UserInput"}],fw.logs
  return r

user_code = r'''

# Delete this example and paste the child's code here:
import random, sys
print("Do you want to play Guess my number or House adventure?")
i = input()
if "guess" in i:
  answer = random.randint(1,10)
  while True:
    i = int(input("Guess my number: "))
    if i < answer: print("That's too low")
    elif i > answer: print("That's too high")
    else: print("Correct"), sys.exit()
print("Welcome to House adventure.") # see https://ssb22.user.srcf.net/game/
class Room:
    def __init__(new_room, description):
        new_room.description = description
        new_room.doors = {}
        new_room.things = []
    def connect(this_room, direction, other_room):
        assert not direction in this_room.doors
        assert not opposite(direction) in other_room.doors
        this_room.doors[direction] = other_room
        other_room.doors[opposite(direction)] = this_room
    def __str__(this_room):
        things = " and ".join(this_room.things)
        if things: things = ".  Things here: " + things
        return this_room.description + "\n" + \
            "You can go " + \
            " or ".join(this_room.doors) + things+"."
    def special_action(this_room, player, action):
        return False
class Landing(Room):
    def __init__(new_landing):
        Room.__init__(
            new_landing,
            "You are on a landing. The north door has a lock.")
    def special_action(this_landing, player, action):
        if action=="unlock door":
            if 'north' in this_landing.doors:
                print ("The door is already unlocked.")
            elif not "key" in player.things:
                print ("You do not have the key.")
            else:
                this_landing.connect('north', secret_room)
                print ("The door is now unlocked.")
            return True
def opposite(direction):
    return {"north":"south", "south":"north",
            "east":"west", "west":"east"} [direction]
def init():
    bathroom = Room("You are in a bathroom.")
    bathroom.things.append("towel")
    bedroom1 = Room("You are in a bedroom.")
    bedroom1.things.append("key")
    landing = Landing()
    landing.connect('south', bathroom)
    landing.connect('east', bedroom1)
    landing.connect('west', Room("You are in a bedroom."))
    global secret_room
    secret_room = Room("You are in the secret room.")
    return landing
class Player:
    def __init__(new_player, first_room):
        new_player.in_room = first_room
        new_player.things = []
    def have_a_turn(this_player):
        print (this_player.in_room)
        what = input("What now? ") ; print()
        if this_player.in_room.special_action(this_player, what):
            return
        what = what.split(None,1)
        if not what: print("You didn't say anything!")
        elif what[0]=="get":
            if len(what)==1:
                print ("You have to tell me what to get.")
            elif what[1] in this_player.in_room.things:
                this_player.in_room.things.remove(what[1])
                this_player.things.append(what[1])
                print ("Got it.")
            elif what[1] in this_player.things:
                print ("You already had that.")
            else: print (what[1]+" is not here.")
        elif what[0]=="drop":
            if len(what)==1:
                print ("You have to tell me what to drop.")
            elif what[1] in this_player.things:
                this_player.things.remove(what[1])
                this_player.in_room.things.append(what[1])
                print ("Dropped it.")
            else: print (f"You are not carrying {what[1]}.")
        elif what[0] in this_player.in_room.doors:
            this_player.in_room = this_player.in_room.doors[what[0]]
        else: print ("You can't do that now.")
start_room = init()
player1 = Player (start_room)
while True: player1.have_a_turn()

# End of example.  Please do NOT delete the apostrophes below.

'''
