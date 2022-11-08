from otherdave.util.madlib import Prompter

prompter = Prompter()

def prompt(addParams, forgetParams):
    # Only one argument at a time
    args = [x for x in [addParams, forgetParams] if x is not None]

    if(args == 0):
        return prompter.make()
    if (args > 1):
        return "stupid command"

    addArgs = addParams.split() if addParams else None
    forgetArgs = forgetParams.split() if forgetParams else None
    
    if (forgetParams and len(forgetArgs) == 1):
        prompter.remNoun(forgetArgs[0])
        prompter.remAdjective(forgetArgs[0])
        return "forgotten" + forgetArgs[0]
    elif(addParams and len(addArgs) == 2):
        if(addArgs[0].lower() == "noun"):
            prompter.addNoun(addArgs[1])
            return "added " + addArgs[1]
        elif(addArgs[0].lower() == "adjective"):
            prompter.addAdjective(addArgs[1])
            return addArgs[1] + " addition"
        else:
            return "invalid article"
    else:
        return "stupid command"
