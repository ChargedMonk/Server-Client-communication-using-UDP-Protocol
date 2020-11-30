# there should only be unique keys in the nested dict in db
def resolveQuery(orgDict,query):
    for k,v in orgDict.items():
        if query in k.lower() and isinstance(v,dict):
            result[k] = v
        elif isinstance(v,dict):
            resolveQuery(v,query)

def delConfInfo(infodict):
    for k,v in infodict.items():
        if isinstance(v,dict):
            if 'Phone no' in v:
                v.pop('Phone no')
            delConfInfo(v)
    return infodict


def serverReply(query,flag=1):
    organizationHeirarchy = eval(dbTxt)
    result.clear()
    if flag == 2:
        resolveQuery(organizationHeirarchy,query.lower())
        # print("sending infodict\n ### result =",result,"\n\n-----\n\n")
        # print("sending infodict\n ### organizationHeirarchy =",organizationHeirarchy,"\n\n-----\n\n")
        return str(delConfInfo(result))
    else:
        resolveQuery(organizationHeirarchy,query.lower())
        # print("result with phone no\n ***result =",result,"\n\n-----\n\n")
        # print("sending infodict\n ### organizationHeirarchy =",organizationHeirarchy,"\n\n-----\n\n")
        return str(result)


result = dict()
with open('db.json','r') as f:
    dbTxt = f.read()
