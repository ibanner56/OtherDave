from otherdave.util.madlib import Prompter

prompter = Prompter()

def prompt(args):
    if(len(args) == 0):
        return prompter.make()
    elif(args[0] == "-forget" and args[1]):
        prompter.remNoun(args[1])
        prompter.remAdjective(args[1])
        return "forgotten" + args[1]
    elif(args[0] == "-add" and args[1] and args[2]):
        if(args[1].lower() == "noun"):
            prompter.addNoun(args[2])
        elif(args[1].lower() == "adjective"):
            prompter.addAdjective(args[2])
        else:
            return "invalid article"
    else:
        return "stupid command"