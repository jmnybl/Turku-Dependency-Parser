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

#token_dictionary={u"S0":u"state.stack(-1)",u"S1":u"state.stack(-2)"}
exp_dictionary={u"p":u"%s.pos",u"l":u"%s.lemma",u"w":u"%s.text",u"d":u"str(state.tree.dtypes.get(%s))",u"m":u"%s.feat"}

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

def encode_token(token):
    """ Token is a string from baseline_feature_template.txt file, encode it so that we can use it as a python variable (replace + and - etc)."""
    token=token.replace(u"(",u"_")
    token=token.replace(u")",u"_")
    token=token.replace(u"+",u"right")
    token=token.replace(u"-",u"left")
    return token

if __name__==u"__main__":

    # now we need two separate file, one for general features and one for deptype related features
    gen=codecs.open(u"xxx.py",u"wt",u"utf-8")
    dep=codecs.open(u"auto_features_deptype.py",u"wt",u"utf-8")


    print >> gen, dependents_func
    print >> dep, dependents_func
    print >> gen
    print >> dep
    print >> gen, stack_func
    print >> dep, stack_func
    print >> gen
    print >> dep
    print >> gen, follow_func
    print >> gen

    print >> gen, u"def create_auto_features(state):" # start function
    print >> dep, u"def create_auto_dep_features(state):"
    print >> gen, u"    S0,S1,S2=get_from_stack(state.stack)" # these are the basic tokens I need to get everything else, can be None
    print >> dep, u"    S0,S1,S2=get_from_stack(state.stack)"
    print >> gen, u"    features={}"
    print >> dep, u"    features={}"

    # read feature template and gather individual features into a list to print later + needed tokens into a set
    tokens=set() # all tokens we will ever need
    ind_features=[] # list of lists of tuples :)

    f=codecs.open(u"baseline_feature_template.txt",u"rt",u"utf-8")
    for line in f:
        line=line.strip()
        if not line or line.startswith(u"#"): continue
        line=line.replace(u" ",u"") # remove extra whitespaces
        tuples=process_one_feature(line)
        # now tuples is a list of (expression,token) pairs, where both are represented as strings, like ('p','S1')    
        if not tuples:
            print >> sys.stderr, "Skipping", line # features we are not able to process
            continue
        for end,token in tuples:
            if token==u"S0" or token==u"S1" or token==u"S2": continue # we already have these, do not take twice
            tokens.add(token)
        ind_features.append(tuples)
    f.close()    
    # now we know all tokens needed, print a function to gather those only once per state
    for token in tokens:
        print >> gen, "    "+encode_token(token)+"="+str(give_token(token))
        if u"right" in encode_token(token) or u"left" in encode_token(token): # won't need these tokens in deptype features
            continue
        print >> dep, "    "+encode_token(token)+"="+str(give_token(token))
    # now we have all the tokens and can refer to those with basic strings (use encode_token to remove illegal chars)
    for feat in ind_features: # iterate through all features

        dtype=False
        if_string=u"if" # to check that none of the tokens is None
        for end,token in feat:
            if_string+=" ("+encode_token(token)+" is not None) and"
            if end==u"d": # this feature involves deptype, write to a separate file
                dtype=True
        if_string=if_string[:-3]+":" # replace the last 'and' with ':'
        if not dtype:
            print >> gen, "    "+if_string
        else:
            print >> dep, "    "+if_string

        str_repr=u"".join(end+"("+token+")" for end,token in feat)
        value=u"+".join(str(exp_dictionary.get(end))%(encode_token(token)) for end,token in feat)
        if not dtype:
            print >> gen, ("        features['"+str_repr+"='+"+value+"]=1.0").encode(u"utf-8")
        else:
            print >> dep, ("        features['"+str_repr+"='+"+value+"]=1.0").encode(u"utf-8")

    print >> gen, "    return features"
    print >> dep, "    return features"

    gen.close()
    dep.close()
