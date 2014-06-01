import codecs
import re
import sys

dependents_func="""
def get_child(token,idx,state):
    if token is None: return None
    childs=sorted(state.tree.childs[token], key=lambda x:x.index)
    if len(childs)>0:
        if idx==u"ld": # leftmost
            return childs[0]
        elif idx==u"rd": # rightmost
            return childs[-1]
        else:
            index=int(idx[1])
            if idx>len(childs)-1: return None
            return childs[index]
    else:
        return None
"""

stack_func="""
def get_from_stack(stack):
    if len(stack)>2:
        return stack[-1],stack[-2],stack[-3]
    elif len(stack)>1:
        return stack[-1],stack[-2],None
    elif len(stack)>0:
        return stack[-1],None,None
    else:
        return None,None,None

"""

follow_func="""
def get_following(token,idx,state):
    if token is None: return None
    if idx[0]==u"+":
        index=token.index+int(idx[1])
    elif idx[0]==u"-":
        index=token.index-int(idx[1])
    else: return None
    if index<0 or index>len(state.tree.tokens)-1: return None
    return state.tree.tokens[index]
"""

token_dictionary={u"S0":u"state.stack(-1)",u"S1":u"state.stack(-2)"}
ending_dictionary={u"p":u".pos",u"l":u".lemma",u"w":u".text",u"d":u".dtype",u"m":u".feat"}

mainregex=re.compile(ur"([a-z]{1,2})\(([A-Za-z0-9-+]+|[a-z0-9]{2}\([S0-9]{2}\))\)",re.U)

regex=re.compile(ur"([a-z0-9]{2})\(([A-Za-z0-9-+]+)\)",re.U)

def process_one_feature(feature):
    if u"A" in feature or u"h" in feature: return []
    parts=mainregex.findall(feature) # returns list of (ftype,token) tuples
    return parts

def give_token(token):
    if token==u"S0" or token==u"S1":
        return token
    if u"+" in token or u"-" in token: # tokens from input string
        base_tok=token[0]+token[-1] # first and last char encode the base token
        index=token[1:3] # two middle characters encode the index in
        return "get_following("+base_tok+",'"+index+"',state)"
    if u"d" in token: # ld, rd or di, use regex
        parts=regex.findall(token)
        if len(parts)!=1:
            print >> sys.stderr, "returning none"
            return None
        else:
            idx,tok=parts[0]
            return "get_child("+tok+",'"+idx+"',state)"
    return None


print dependents_func
print
print stack_func
print
print follow_func
print

print u"def create_all_features(state):" # start function
print u"    S0,S1,S2=get_from_stack(state.stack)" # these are the basic tokens I need to get everything else, can be None
print u"    features={}"

# read feature template
f=codecs.open(u"baseline_feature_template.txt",u"rt",u"utf-8")
for line in f:
    line=line.strip()
    if not line or line.startswith(u"#"): continue
    line=line.replace(u" ",u"") # remove extra whitespaces
    tuples=process_one_feature(line)
    if not tuples:
        print >> sys.stderr, "Skipping", line
        continue
    if_string=u"if"
    for i in xrange(0,len(tuples)):
        print "    v"+str(i)+"="+str(give_token(tuples[i][1]))
        if_string+=" (v"+str(i)+" is not None) and"
    if_string=if_string[:-3]+":"
    print "    "+if_string # if any of tokens is not None
    string=u"+".join("v"+str(i)+str(ending_dictionary.get(tuples[i][0])) for i in xrange(0,len(tuples)))
    print ("        features['"+line+"='+"+string+"]=1.0").encode(u"utf-8")
f.close()
print "    return features"

