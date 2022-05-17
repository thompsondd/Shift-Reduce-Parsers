from nltk.grammar import Nonterminal
from nltk.tree import Tree
import nltk
from lexer_analysis import *
import pandas as pd

grammar1 = nltk.CFG.fromstring("""
program -> 'START' statements 'END'

statements -> branch_stmt | 'EMP' assign | 'EMP' block| statements block 'EMP'| statements statements | statements assign | statements assign 'EMP' | 'EMP' print_stmt 'newline' | 'EMP' input_stmt 'newline' | statements block 'newline' | statements assign 'newline' | statements 'EMP' | stmt| statements 'newline' | end_branch_stmt | statements exp 'EMP' |statements exp 'newline' |'EMP' exp 

branch_stmt -> 'EMP' if_stmt | 'EMP' while_stmt | 'EMP' for_stmt

stmt -> for_stmt 'newline' | while_stmt 'newline' | if_stmt 'newline'

end_branch_stmt -> statements for_stmt 'EMP' | statements while_stmt 'EMP' | statements if_stmt 'EMP'

block_ ->  'tab' if_stmt | 'tab' for_stmt | 'tab' while_stmt | 'tab' print_stmt | 'tab'assign | 'tab' input_stmt | 'tab' exp_stmt | 'tab' block | 'tab' block_ | 'tab' else_block | 'tab' elif_block

block -> 'tab' block_ | block_

exp_stmt1 ->  number '-' identifier | number '+' identifier |  identifier '-' number | identifier '+' number 

exp_stmt2 -> number '+' exp_stmt |number '-' exp_stmt |  exp_stmt '-' number | exp_stmt '+' number | identifier '+' exp_stmt | identifier '-' exp_stmt | exp_stmt '+' identifier | exp_stmt '-' identifier

exp_stmt ->  number '-' number | number '+' number | identifier '-' identifier | identifier '+' identifier |  exp_stmt1 | exp_stmt2 | factor_id |factor_atom | factor_num | sp_exp | exp_sub_stmt | sp_sub_exp_stmt

sp_sub_exp_stmt -> special_exp_stmt '+' exp_stmt | special_exp_stmt '-' exp_stmt | special_exp_stmt '*' exp_stmt | special_exp_stmt '/' exp_stmt | exp_stmt '*' special_exp_stmt | exp_stmt '/' special_exp_stmt | exp_stmt '-' special_exp_stmt | exp_stmt '+' special_exp_stmt

exp_sub_stmt -> exp_stmt '*' exp_stmt | exp_stmt '+' exp_stmt | exp_stmt '/' exp_stmt | exp_stmt '-' exp_stmt

special_exp_stmt -> '(' exp_stmt ')'

sp_exp -> special_exp_stmt '*' special_exp_stmt | special_exp_stmt '-' special_exp_stmt | special_exp_stmt '/' special_exp_stmt | special_exp_stmt '+' special_exp_stmt | sp_exp_1 | sp_exp_2

sp_exp_1 -> special_exp_stmt '*' number | special_exp_stmt '/' number | special_exp_stmt '-' number | special_exp_stmt '+' number | number '+' special_exp_stmt | number '-' special_exp_stmt | number '/' special_exp_stmt | number '*' special_exp_stmt

sp_exp_2 -> special_exp_stmt '*' identifier | special_exp_stmt '/' identifier | special_exp_stmt '-' identifier | special_exp_stmt '+' identifier | identifier '+' special_exp_stmt | identifier '-' special_exp_stmt | identifier '/' special_exp_stmt | identifier '*' special_exp_stmt

assign -> identifier '=' exp_stmt 'newline'| identifier '=' 'string' 'newline'| identifier '=' number 'newline' | identifier '=' bool_value 'newline' | identifier '=' exp 'newline' | identifier '=' special_exp_stmt 'newline' | assign_sub

assign_sub -> identifier '=' number 'EMP' | identifier '=' bool_value 'EMP' | identifier '=' exp 'EMP' | identifier '=' special_exp_stmt 'EMP' | assign assign | i_r | identifier '=' identifier 'EMP' | identifier '=' identifier 'EMP' | identifier '=' exp_stmt 'EMP'| identifier '=' 'string' 'EMP'| identifier '=' number 'EMP'

i_r -> identifier '+' '=' number | identifier '-' '=' number | identifier '*' '=' number | identifier '/' '=' number | i_r_1

i_r_1 -> identifier '+' '=' special_exp_stmt | identifier '-' '=' special_exp_stmt | identifier '*' '=' special_exp_stmt | identifier '/' '=' special_exp_stmt

print_stmt -> 'print' special_exp_stmt | 'print' '(' input_stmt ')' | 'print' '(' identifier ')' | 'print' '(' exp ')' | 'print' '(' number ')' | 'print' '(' 'string' ')' |'print' '(' ')'

exp -> identifier compare identifier | identifier compare number | number compare number | bool_value | identifier compare special_exp_stmt | special_exp_stmt compare special_exp_stmt | special_exp_stmt compare identifier| '(' exp ')'

for_stmt -> 'for' identifier 'in' 'range' '(' number ')' 'colon' 'newline' block | 'for' identifier 'in' 'range' '(' identifier ')' 'colon' 'newline' block | 'for' identifier 'in' 'range' special_exp_stmt 'colon' 'newline' block

if_stmt -> 'if' exp 'colon' 'newline' block | 'if' exp 'colon' 'newline' block 'newline' elif_block|'if' exp 'colon' 'newline' block 'newline' else_block

else_block -> 'else' 'colon' 'newline' block | 'newline' if_stmt

elif_block -> 'elif' exp 'colon' 'newline' block 'newline' elif_block|'newline' if_stmt

while_stmt -> 'while' exp 'colon' 'newline' block

factor_atom -> number '*' identifier | number '/' identifier | identifier '*' number | identifier '/' number | number '*' number | number '/' number | identifier '*' identifier | identifier '/' identifier 

factor_num -> number '*' exp_stmt |  number '/' exp_stmt | exp_stmt '*' number | exp_stmt '/' number

factor_id -> identifier '*' exp_stmt | identifier '/' exp_stmt | exp_stmt '*' identifier | exp_stmt '/' identifier

input_stmt -> identifier '=' 'input' '(' ')'

identifier -> 'var' | '(' 'var' ')'

number -> '(' number ')' | 'num'

compare -> '<'|'>'|'>='|'<='|'=='|"!="

bool_value -> 'True' | 'False'
  
""")

def convert_to_sym(list_sym):
    data=[]
    for i in list_sym:
        try:
            data.append(i.label())
        except:
            data.append(i)
    return data

def convert_to_action(data):
    try:
        action=f"reduce: {data.productions()[0]}"
    except:
        action="shift"
    return action

def shift_reduce_table(history,list_reduce,syntax):
    table={
        "stack":[],
        "curr_sym":[],
        "rest_of_input":[],
        "action":[]
    }
    limit=len(history)
    for i in range(limit):
        table["stack"].append(convert_to_sym(history[i][0]))
        table["curr_sym"].append(history[i][1][0] if len(history[i][1])>1 else "")
        table["rest_of_input"].append(history[i][1][1:])
        if i+1<limit:
            value=convert_to_action(history[i+1][0][-1])
            table["action"].append(value)
        else:
            table["action"].append("accept" if syntax else "deny")
    return table

class SteppingShiftReduceParser(nltk.SteppingShiftReduceParser):
    def __init__(self,grammar1,trace=2):
        super().__init__(grammar1,trace)
        self.table= {
                        "stack":[[]],
                        "curr_sym":[],
                        "rest_of_input":[],
                        "action":[]
                    }
    def _trace_stack(self, stack, remaining_text, marker=" "):
        s = "  " + marker + " [ "
        if marker=="S":
            self.table["action"].append("shift")
        elif marker=="R":
            if isinstance(stack[-1], Tree):
                self.table["action"].append("reduce: "+repr(Nonterminal(stack[-1].productions()[0])))
        curr_sym=None
        curr_stack=[]
        rest_of_input=remaining_text[-1::-1]
        for elt in stack:
            if isinstance(elt, Tree):
                curr_sym_=str(Nonterminal(elt.label()))
                s += repr(curr_sym_) + " "
                curr_stack.append(str(curr_sym_))
            else:
                curr_sym=str(elt)
                s += repr(curr_sym) + " "
                curr_stack.append(str(curr_sym))
        if marker =="S":
            self.table["curr_sym"].append(curr_sym)
        else:
            self.table["curr_sym"].append(rest_of_input.pop() if len(remaining_text)>0 else "")
        self.table["rest_of_input"].append(rest_of_input[-1::-1])
        self.table["stack"].append(curr_stack.copy())
        s += "* " + " ".join(remaining_text) + "]"
        print(s)

def print_table(table):
    if table["stack"][-1]==["program"]:
        table["curr_sym"].append("")
        table["rest_of_input"].append([])
        table["action"].append("accept")
    else:
      table["curr_sym"].append("")
      table["rest_of_input"].append([])
      table["action"].append("deny")
    new_data={}
    for i in table.keys():
        if i in ["action","curr_sym"]:
            new_data.update({i.upper():table[i]})
            continue
        new_data.update({i.upper():[]})
        for j in table[i]:
            new_data[i.upper()].append(" ".join(j))
    df=pd.DataFrame(new_data)
    
    return df


def checkSyntax(c):
    sent = c
    syntax = False
    rd_parser = SteppingShiftReduceParser(grammar1)
    tree=list(rd_parser.parse(sent))
    history=rd_parser.table
    try:
        tree=tree[0]
        if tree.label()=="program":
            syntax = True
    except:
        #print(tree)
        pass
    return (syntax,print_table(history))

