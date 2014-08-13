import codecs
import re
import sys



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



exp_dictionary={u"p":u"%s.pos",u"l":u"%s.lemma",u"w":u"%s.text",u"d":u"str(state.tree.dtypes.get(%s))",u"m":u"%s.feat",u"pi":u"%s.pos"}

mainregex=re.compile(ur"([a-z]{1,2})\(([A-Za-z0-9-+]+|[a-z0-9]{2}\([S0-9]{2}\))\)",re.U)

regex=re.compile(ur"([a-z0-9]{2})\(([A-Za-z0-9-+]+)\)",re.U)

def process_one_feature(feature):
    if u"A" in feature or u"h" in feature: return []
    parts=mainregex.findall(feature) # returns list of (ftype,token) tuples
    return parts

def give_token(token):
    base,direc,length=token[0],token[1],token[2]
    index=direc+length
    return "get_following("+base+",'"+index+"',state)"
    
def encode_token(token):
    """ Token is a string from baseline_feature_template.txt file, encode it so that we can use it as a python variable (replace + and - etc)."""
    token=token.replace(u"+",u"right")
    token=token.replace(u"-",u"left")
    return token

if __name__==u"__main__":

    gen=codecs.open(u"auto_graph_features.py",u"wt",u"utf-8")

    print >> gen, follow_func
    print >> gen

    print >> gen, u"def create_first_order(p,d,order,state):" # start function
    print >> gen, u"    features={}"

    # read feature template and gather individual features into a list to print later + needed tokens into a set
    tokens=set() # all tokens we will ever need
    ind_features=[] # list of lists of tuples :)

    f=codecs.open(u"first_order_template.txt",u"rt",u"utf-8")
    for line in f:
        line=line.strip()
        if not line or line.startswith(u"#"): continue
        line=line.replace(u" ",u"") # remove extra whitespaces
        tuples=process_one_feature(line)
        # now tuples is a list of (expression,token) pairs, where both are represented as strings, like ('p','d')
        if not tuples:
            print >> sys.stderr, "Skipping", line # features we are not able to process
            continue
        ind_features.append(tuples)
    f.close()    

    tokens=set()
    for feat in ind_features:
        for func,token in feat:
            if (token not in tokens) and ((u"+" in token) or (u"-" in token)):
                tokens.add(token)
                print >> gen, u"    "+encode_token(token),u"=",give_token(token)

    for feat in ind_features: # iterate through all features
        extra=set()
        for func,token in feat:
            if (u"+" in token) or (u"-" in token):
                extra.add(token)
        if extra:
            if_string=u"if" # to check that none of the tokens is None
            for t in extra:
                if_string+=" ("+encode_token(t)+" is not None) and"
            if_string=if_string[:-3]+":" # replace the last 'and' with ':'
            print >> gen, "    "+if_string
            str_repr=u"".join(end+"("+token+")" for end,token in feat)+u"o(d,p)"
            value=u"+".join(str(exp_dictionary.get(end))%(encode_token(token)) for end,token in feat)+u'+"_"+str(order)'

            print >> gen, ("        features['"+str_repr+"='+"+value+"]=1.0").encode(u"utf-8")
        else:
            str_repr=u"".join(end+"("+token+")" for end,token in feat)+u"o(d,p)"
            value=u"+".join(str(exp_dictionary.get(end))%(encode_token(token)) for end,token in feat)+u'+"_"+str(order)'

            print >> gen, ("    features['"+str_repr+"='+"+value+"]=1.0").encode(u"utf-8")

    print >> gen, "    return features"
    print >> gen
    print >> gen

    ### sec order ###
    
    print >> gen, u"def create_second_order(p,d,z,role,order,state):" # start function
    print >> gen, u"    features={}"

    # read feature template and gather individual features into a list to print later + needed tokens into a set
    tokens=set() # all tokens we will ever need
    ind_features=[] # list of lists of tuples :)

    f=codecs.open(u"second_order_template.txt",u"rt",u"utf-8")
    for line in f:
        line=line.strip()
        if not line or line.startswith(u"#"): continue
        line=line.replace(u" ",u"") # remove extra whitespaces
        tuples=process_one_feature(line)
        # now tuples is a list of (expression,token) pairs, where both are represented as strings, like ('p','d')
        if not tuples:
            print >> sys.stderr, "Skipping", line # features we are not able to process
            continue
        ind_features.append(tuples)
    f.close()    

    tokens=set()
    for feat in ind_features:
        for func,token in feat:
            if (token not in tokens) and ((u"+" in token) or (u"-" in token)):
                tokens.add(token)
                print >> gen, u"    "+encode_token(token),u"=",give_token(token)

    for feat in ind_features: # iterate through all features
        extra=set()
        for func,token in feat:
            if (u"+" in token) or (u"-" in token):
                extra.add(token)
        if extra:
            if_string=u"if" # to check that none of the tokens is None
            for t in extra:
                if_string+=" ("+encode_token(t)+" is not None) and"
            if_string=if_string[:-3]+":" # replace the last 'and' with ':'
            print >> gen, "    "+if_string
            str_repr=u"".join(end+"("+token+")" for end,token in feat)+u"o(d,p,z)_'+role"
            value=u"+".join(str(exp_dictionary.get(end))%(encode_token(token)) for end,token in feat)+u'+"_"+str(order)'

            print >> gen, ("        features['"+str_repr+"+'='+"+value+"]=1.0").encode(u"utf-8")
        else:
            str_repr=u"".join(end+"("+token+")" for end,token in feat)+u"o(d,p,z)_'+role"
            value=u"+".join(str(exp_dictionary.get(end))%(encode_token(token)) for end,token in feat)+u'+"_"+str(order)'
            if u"d(y)" in str_repr: continue
            print >> gen, ("    features['"+str_repr+"+'='+"+value+"]=1.0").encode(u"utf-8")

    print >> gen, "    return features"

    print >> gen
    print >> gen


    ### third order ###
    
    print >> gen, u"def create_third_order(p,d,y,z,role1,role2,order,state):" # start function
    print >> gen, u"    features={}"

    # read feature template and gather individual features into a list to print later + needed tokens into a set
    tokens=set() # all tokens we will ever need
    ind_features=[] # list of lists of tuples :)

    f=codecs.open(u"third_order_template.txt",u"rt",u"utf-8")
    for line in f:
        line=line.strip()
        if not line or line.startswith(u"#"): continue
        line=line.replace(u" ",u"") # remove extra whitespaces
        tuples=process_one_feature(line)
        # now tuples is a list of (expression,token) pairs, where both are represented as strings, like ('p','d')
        if not tuples:
            print >> sys.stderr, "Skipping", line # features we are not able to process
            continue
        ind_features.append(tuples)
    f.close()    

    tokens=set()
    for feat in ind_features:
        for func,token in feat:
            if (token not in tokens) and ((u"+" in token) or (u"-" in token)):
                tokens.add(token)
                print >> gen, u"    "+encode_token(token),u"=",give_token(token)

    for feat in ind_features: # iterate through all features
        extra=set()
        for func,token in feat:
            if (u"+" in token) or (u"-" in token):
                extra.add(token)
        if extra:
            if_string=u"if" # to check that none of the tokens is None
            for t in extra:
                if_string+=" ("+encode_token(t)+" is not None) and"
            if_string=if_string[:-3]+":" # replace the last 'and' with ':'
            print >> gen, "    "+if_string
            str_repr=u"".join(end+"("+token+")" for end,token in feat)+u"o(d,p,y,z)_'+role1+'_'+role2"
            value=u"+".join(str(exp_dictionary.get(end))%(encode_token(token)) for end,token in feat)+u'+"_"+str(order)'

            print >> gen, ("        features['"+str_repr+"+'='+"+value+"]=1.0").encode(u"utf-8")
        else:
            str_repr=u"".join(end+"("+token+")" for end,token in feat)+u"o(d,p,y,z)_'+role1+'_'+role2"
            value=u"+".join(str(exp_dictionary.get(end))%(encode_token(token)) for end,token in feat)+u'+"_"+str(order)'
            print >> gen, ("    features['"+str_repr+"+'='+"+value+"]=1.0").encode(u"utf-8")

    print >> gen, "    return features"


    gen.close()

