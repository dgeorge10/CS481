#------------------------------------------------------------------------------
import sys
# Text correction using Hidden Markov model and Viterbi algorithm
# JL Popyack, May 2020
#
# Uses Viterbi algorithm code, modified from
#   https://en.wikipedia.org/wiki/Viterbi_algorithm
#
# The user provides the following arguments:
#
# obs     : a list of periodic state observations (evidence)
# states  : a list of all possible states for the actual system
# start_p : a list of probabilities of occurrence for each state
# trans_p : transition probabilities for system states
# emit_p  : conditional probabilities of evidence values produced
#           by each state
#
# The algorithm determines the most likely states that explain the
#  
#
# An example given at
#   https://en.wikipedia.org/wiki/Viterbi_algorithm
# concerns a village doctor whose patients are either in Healthy or Fever state,
# but is able only to observe a whether a patient is normal, cold, or dizzy.
# After a few observations, the doctor is able to determine the most likely 
# state sequence that explains the evidence.
# The example uses the following values:
#
# obs = ('normal', 'cold', 'dizzy')
# states = ('Healthy', 'Fever')
# start_p = {'Healthy': 0.6, 'Fever': 0.4}
# trans_p = {
#    'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
#    'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
#    }
# emit_p = {
#    'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
#    'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
#    }
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Viterbi algorithm from https://en.wikipedia.org/wiki/Viterbi_algorithm
# This has been modified so that instead of printing the table of 
# probabilities and the result (commented out), it returns the concatenated 
# results.
# For this program, the algorithm is used on strings of lowercase letters
# which represent words that have been garbled during Optical Character 
# Recognition (OCR). Expected occurrences of letters a..z are given in start_p,
# determined through analysis of a book written in English.  Transition 
# probabilities reflect the probability that the next character in sequence
# is a given letter, based on the previous k characters in the sequence, also
# determined through analysis of the same book.
#------------------------------------------------------------------------------

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}

    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t-1][states[0]]["prob"]*trans_p[states[0]][st]
            prev_st_selected = states[0]
            for prev_st in states[1:]:
                tr_prob = V[t-1][prev_st]["prob"]*trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st
                    
            max_prob = max_tr_prob * emit_p[st][obs[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}
                    
# commented out code from original:
#     for line in dptable(V):
#         print (line)
    
    opt = []
    max_prob = -1.0
    previous = None

    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st
    
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]
        
# inserted code - joins the optimized list to form a string:
    return(''.join(opt))

# commented out code from original:
#     print ('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)

def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)

#------------------------------------------------------------------------------
# Used for comparing actual text with corrected text
#------------------------------------------------------------------------------
def countDifferences(str1,str2):
    print str(len(str1))+" - "+str(len(str2))
    numDiffs = 0
    for ch1,ch2 in zip(str1.strip().split(),str2.strip().split()):
        if ch1 != ch2:
            numDiffs = numDiffs + 1
    return numDiffs
		
		
#------------------------------------------------------------------------------
# Emission probabilities for this example state explain the probabilities that 
# certain letters are mistaken in the OCR process.  For instance, b and d are 
# often confused for each other, as are {c,e,o}, {h,l}, {i,j}, {m,n} and {v,w}.  
# In all cases, the probability that the actual letter is recognized correctly 
# is 60%, and the probability that it is recognized as one of the other letters # in its grouping is 40%, evenly divided among the alternatives. 
# The emission probabilities shown below contain only nonzero values, e.g.,
# 	  'e' : {'c':0.2, 'e':0.6 ,'o':0.2}
# Zero probabilities for remaining emissions are filled in later.
#------------------------------------------------------------------------------
emit_nonzero = {
  'b' : {'b':0.6, 'd':0.4}, 
  'd' : {'b':0.4, 'd':0.6}, 
  'c' : {'c':0.6, 'e':0.2 ,'o':0.2}, 
  'e' : {'c':0.2, 'e':0.6 ,'o':0.2}, 
  'o' : {'c':0.2, 'e':0.2 ,'o':0.6}, 
  'h' : {'h':0.6, 'l':0.4}, 
  'l' : {'h':0.4, 'l':0.6}, 
  'i' : {'i':0.6, 'j':0.4}, 
  'j' : {'i':0.4, 'j':0.6}, 
  'm' : {'m':0.6, 'n':0.4}, 
  'n' : {'m':0.4, 'n':0.6}, 
  'v' : {'v':0.6, 'w':0.4},
  'w' : {'v':0.4, 'w':0.6},

  ' ': {' ':1.0},
  'a': {'a':1.0},
  'f': {'f':1.0},
  'g': {'g':1.0},
  'k': {'k':1.0},
  'p': {'p':1.0},
  'q': {'q':1.0},
  'r': {'r':1.0},
  's': {'s':1.0},
  't': {'t':1.0},
  'u': {'u':1.0},
  'x': {'x':1.0},
  'y': {'y':1.0},
  'z': {'z':1.0}
}
   

# input validation
n = 0
try:
    n = int(sys.argv[1])
except:
    print "no value for n passed: using 0"

if n > 2 or n < 1:
    print "invalid value of n. must be either 1 or 2"
    sys.exit(0)


bookfile = file('gatsby.txt','r')
booktext = bookfile.read()
bookfile.close()
booktext.strip()

valid_chars = (' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z') 
states = []
graph = {}

# algorithm to build n-graph
def buildGraph(n):
    index = 0
    for char in booktext:
        #lower = char.lower()
        # get chunk that we are inserting into states
        chunk = booktext[index:index+n].lower()
        valid = all([char in valid_chars for char in chunk])
        if not valid: 
            index += 1
            continue
        
        if valid and chunk not in states: states.append(chunk)

        if chunk not in graph: graph[chunk] = {}

        next_char = booktext[index+n].lower()
        if next_char in valid_chars:
            if next_char in graph[chunk]:
                graph[chunk][next_char] += 1
            else:
                graph[chunk][next_char] = 1
        index += 1

for i in range(1,n+1):
    buildGraph(i)

for char in graph:
    count = 0
    for value in graph[char]:
        count += graph[char][value]
    for value in graph[char]:
        graph[char][value] /= float(count)

# set new trans_nonzero
trans_nonzero = graph

# update emit_nonzero to have the digraph-states
for state in states:
    if state not in emit_nonzero:
        new = { state: 0.6 }
        good_replacements=[]
        for char in state:
            if char in emit_nonzero and emit_nonzero[char][char] != 1.0:
                replacements = emit_nonzero[char]
                for replacement in replacements:
                    if replacement != char:
                        new_emit = state.replace(char, replacement)
                        good_replacements.append(new_emit)

        if len(good_replacements) == 0:
            new.update({state: 1.0})
        else:
            for replacement in good_replacements:
                new.update({replacement: 0.4/len(good_replacements)})

        emit_nonzero[state] = new

counts = {}
total = 0
for i in range(1,n+1):
    index = 0
    for char in booktext:
        chunk = booktext[index:index+i].lower()
        if chunk in states:
            if chunk in counts:
                counts[chunk] += 1
            else:
                counts[chunk] = 1
            total += 1
        index += 1

for state in counts:
    counts[state] /= float(total)

# set new start_p
start_p = counts

#------------------------------------------------------------------------------
# Create trans_p and emit_p from trans_nonzero and emit_nonzero by filling in 
# zero probabilities for unlisted transitions.
#------------------------------------------------------------------------------
trans_p = {}
emit_p = {}
from collections import defaultdict
for st in states:
    trans_p[st] = {s: 0 for s in states}
    trans_p[st].update(trans_nonzero[st])
    emit_p[st] = {s: 0 for s in states}
    emit_p[st].update(emit_nonzero[st])

#------------------------------------------------------------------------------
# Read actual text and text resulting from (simulated) poor OCR.
#------------------------------------------------------------------------------
actualfile = file('actual_text.txt','r')
actualtext = actualfile.read()
actualfile.close()
actualtext.strip()  #remove leading and trailing whitespace

infile = file('poor_ocr1b.txt','r') 
text = infile.read() 
infile.close() 
text = text.strip()  #remove leading and trailing whitespace

numDiffs = countDifferences(actualtext,text)
print "Differences between actual, poor OCR text: "+str(numDiffs)

print "\nCorrected text: "


word=""
newtext = ""
for word in text.split():
    obs = list(word)
    mostLikely = viterbi(obs,states,start_p,trans_p,emit_p)
    newtext += mostLikely + " "
    print mostLikely,
    
newtext = newtext.strip()
numDiffs = countDifferences(actualtext,newtext)
print "\n\nDifferences between actual, corrected text: "+str(numDiffs)
