import re
key_words = {
                "operator":["+","-","*","/",">","<","(",")"],
                "operator_2":[">=","<=","!=","=="],
                "key_word":["if","elif","else","input","print","while",'True','False',"for",'range','in'],
                "symbol":{":":"colon","\t":"tab",'\n':"newline"}
            }

class DATA:
    def __init__(self,data):
        self.__data=data
        self.__len=len(data)
        self.__index=-1
    
    def next_char(self):
        if self.__index+1<self.__len:
            return self.__data[self.__index+1]
        return None

    def getNextChar(self):
        self.__index+=1
        if self.__index>=self.__len:
            return None
        return self.__data[self.__index]
     

def _scan_string(start_char,data):
    t=f"{start_char}"
    while data.next_char() not in ["'",'"',None]:
        t+=data.getNextChar()
    t+=data.getNextChar()
    return t

def _scan(first_char,data, allowed):
    ret = f"{first_char}"
    p=data.next_char()
    while  p!= None and re.match(allowed, p):
        p=data.getNextChar()
        ret += p
        p=data.next_char()
    t="".join(list(filter(lambda x: x!="",ret.split("."))))
    if t.isnumeric():
        return ("num",ret)
    if ret in key_words["key_word"]:
        return tuple([ret])
    return ("var",ret)

def _lex(data):
    d=DATA(data)
    while d.next_char() is not None:
        c=d.getNextChar()
        if c==" ":
            pass
        elif c in key_words["operator"] or c in ["!","="]:
            if d.next_char() !=None and c+d.next_char() in key_words["operator_2"]:
                name=c
                c=d.getNextChar()
                name+=c
                yield(tuple([name]))
            else:
                yield(tuple(c))
        elif c in key_words["symbol"].keys():
            yield((key_words["symbol"][c],c))
        elif c in ["'",'"']:
            yield(("string",_scan_string(c,d)))
        elif re.match("[.0-9]", c): 
            yield(_scan(c,d, "[.0-9]"))
        elif re.match("[_a-zA-Z]", c):
            yield(_scan(c,d, "[_a-zA-Z0-9]"))
        else:
            raise Exception("Unrecognised character: '" + c + "'.")


def _read_data(url):
    data=None
    with open(url,"r") as f:
        data=f.readlines()
    data=list(map(lambda x: x.replace("    ","\t",),data))
    s=""
    for i in data:
        s += i.rstrip('\n')+" "
    return "".join(data)

def lexer(string):
    return [i for i in _lex(string)]
    
def lex(url):
    data=_read_data(url)
    tokens= [ i[0] for i in lexer(data)]
    tokens.insert(0,"EMP")
    tokens.insert(0,"START")
    tokens.append("EMP")
    tokens.append("END")
    return tokens

#print(lex(r"input.py"))