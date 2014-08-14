import string

s=set()

templates=[]
f=open("feature_template_template.txt","rt")
for line in f:
    line=line.strip()
    templates.append(string.Template(line))

for S1 in range(0,3):
    for S2 in range(0,3):
        for S3 in range(0,3):
            for B1 in range(0,5):
                for B2 in range(0,5):
                    for C1 in range(1,5):
                        for C2 in range(1,5):
                            for t in templates:
                                s.add(t.substitute(S1=S1,S2=S2,S3=S3,B1=B1,B2=B2,C1=C1,C2=C2))

for f in sorted(s):
    print f


