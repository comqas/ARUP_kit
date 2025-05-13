from json import dumps, loads
from datetime import datetime
from random import randint

def Adj(a, sigma):      # a: proposed reputation level; sigma: current context
    """This function:
    uses the current context of a user and the RS server proposal to adjust reputation level to 'a'
    to actually adjust the user's reputation and update the user context.
    The type of sigma is dictionary"""

    if sigma:
        context = loads(sigma.decode('utf-8'))
    else:
        context = {}
    if 'updates' not in context: context['updates'] = []
    # example
    context['updates'].append(           # append (a, timestamp) to the list tagged "updates" in the context
        (a,str(datetime.now()))
         )
    return a, dumps(context).encode('utf-8')            # accept recommendation


def Upd(a,R):       # a: correct current reputation, R: situation report
    "This function evaluates report R and returns a proposed new reputation"
    # Below is a plug-up for Report analysis code with reputation update
    if randint(0,9) == 0: return 0     # 10% probability of 0 reputation to return
    return randint(max(a-1,0), min(a+1,3))  # equal probability to keep, upgrade and downgrade
