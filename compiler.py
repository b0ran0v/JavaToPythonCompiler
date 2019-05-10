import os
import re

from classes import Token, Assign, If, Operation, Condition, While


javaFile = ""
filePath = 'javaFile.txt'

data_types = ['int','String']

syntax_tree = []
tokens = []
current = 0
ids = []
token = ''

tab_value = 0


def readFile(path):
    with open(path, 'r') as file:
        myFile = file.read()
    return myFile


def tokenizer(input):
    input = input+''
    current = 0
    tokens = []

    while(current<len(input)):
        char = input[current]
        #Left paranthesis
        if(char=='('):
            tokens.append(Token('lparen', char))
            current+=1
            continue
        #Right paranthesis
        elif(char==')'):
            tokens.append(Token('rparen', char))
            current+=1
            continue
        #Left brace
        elif(char=='{'):
            tokens.append(Token('lbrace', char))
            current+=1
            continue
        #Right brace
        elif(char=='}'):
            tokens.append(Token('rbrace', char))
            current+=1
            continue
        #Is id
        elif(re.match(r'[A-Za-z]+',char)):
            value = ''
            while(re.match(r'[A-Za-z]+',char)):
                value+=char
                current+=1
                char = input[current]
            if(value in data_types):
                continue
            elif(value=='if'):
                tokens.append(Token('if',value))
            elif(value=='while'):
                tokens.append(Token('while',value))
            else:
                tokens.append(Token('var_name',value))
            continue
        #Is number
        elif(re.match(r'[0-9]+',char)):
            value = ''
            while(re.match(r'[0-9]+',char)):
                value+=char
                current+=1
                char = input[current]
            tokens.append(Token('number',value))
            continue
        #Is string
        elif(char=='\"'):
            value = ''
            current+=1
            char = input[current]
            while(char!='\"'):
                value+=char
                current+=1
                char = input[current]
            tokens.append(Token('string',value))
            current+=1
            continue
        #Is signing
        elif(char=='='):
            if(input[current+1]=='='):
                tokens.append(Token('conditional', '=='))
                current+=1
            else:
                tokens.append(Token('assign', char))
            current+=1
            continue
        #Is arithmetical operator
        elif(char=='+' or char=='-' or char=='*' or char=='/' or char=='%'):
            tokens.append(Token('arithmetic', char))
            current+=1
            continue
        #Is conditional operator
        elif(char=='>' or char=='<'):
            tokens.append(Token('conditional', char))
            current+=1
            continue
        #Is whitespace
        elif(re.match(r'\s',char)):
            current+=1
            continue
        #Is semicolon
        elif(char==';'):
            tokens.append(Token('semi', char))
            current+=1
            continue
    return tokens
    

def parser():
    global syntax_tree
    global ids
    global tokens
    global current
    global token

    if(current>=len(tokens)):
        return
    token = tokens[current]
    if(token.type=='var_name'):
        ids.append(token.value)
        current+=1
        return
    elif(token.type=='assign'):
        assign = Assign(ids[len(ids)-1])
        del ids[:]
        current+=1
        token = tokens[current]
        while(token.type!='semi'):
            assign.nodes.append(token)
            current+=1
            token = tokens[current]
        if(len(assign.nodes)==1):
            assign.assign_value(assign.nodes[0].value, assign.nodes[0].type)
        else:
            operation = Operation(assign.nodes[0].value,assign.nodes[2].value,assign.nodes[1].value)
            assign.assign_value(operation, 'operation')
        current+=1
        return assign
    elif(token.type=='if'):
        current+=2
        left = []
        cond = ''
        right = []
        token = tokens[current]
        #Building left side of condition
        while(token.type!='conditional'):
            left.append(token)
            current+=1
            token = tokens[current]
        if(len(left)==1):
            left = left[0].value
        else:
            left = Operation(left[0].value, left[2].value, left[1].value)

        #Condition track
        cond = token.value

        #Building right side of condition
        current+=1
        token = tokens[current]
        while(token.type!='rparen'):
            right.append(token)
            current+=1
            token = tokens[current]

        if(len(right)==1):
            right = right[0].value
        else:
            right = Operation(right[0].value, right[2].value, right[1].value)
        #Building condition and if statement
        condition = Condition(left, cond, right)
        iff = If(condition)

        current+=2
        token = tokens[current]
        while(token.type!='rbrace'):
            statement = parser()
            if(statement!=None):
                iff.body.append(statement)
        current+=1
        return iff
    elif(token.type=='while'):
        current+=2
        left = []
        cond = ''
        right = []
        token = tokens[current]
        #Building left side of condition
        while(token.type!='conditional'):
            left.append(token)
            current+=1
            token = tokens[current]
        if(len(left)==1):
            left = left[0].value
        else:
            left = Operation(left[0].value, left[2].value, left[1].value)

        #Condition track
        cond = token.value

        #Building right side of condition
        current+=1
        token = tokens[current]
        while(token.type!='rparen'):
            right.append(token)
            current+=1
            token = tokens[current]

        if(len(right)==1):
            right = right[0].value
        else:
            right = Operation(right[0].value, right[2].value, right[1].value)
        #Building condition and while statement
        condition = Condition(left, cond, right)
        whilee = While(condition)

        current+=2
        token = tokens[current]
        while(token.type!='rbrace'):
            statement = parser()
            if(statement!=None):
                whilee.body.append(statement)
        current+=1
        return whilee

def generate_code(statement):
    global current
    global tab_value

    if(isinstance(statement, Assign)):
        if(statement.type=='string'):
            print('  '*tab_value+statement.id+' = \''+str(statement.value)+'\'')
        elif(statement.type=='operation'):
            print('  '*tab_value+statement.id+' = '+str(statement.value.id1)+' '+str(statement.value.op+' '+str(statement.value.id2)))
        else:
            print('  '*tab_value+statement.id+' = '+str(statement.value))
    elif(isinstance(statement, If)):
        left = statement.condition.left
        right = statement.condition.right
        if(isinstance(statement.condition.left, Operation)):
            left = str(left.id1)+str(left.op)+str(left.id2)
        if(isinstance(statement.condition.right, Operation)):
            right = str(right.id1)+str(right.op)+str(right.id2)
        print('  '*tab_value+'if('+str(left)+str(statement.condition.condition)+str(right)+'):')
        tab_value+=1
        for element in statement.body:
            generate_code(element)
        tab_value-=1     
    elif(isinstance(statement, While)):
        left = statement.condition.left
        right = statement.condition.right
        if(isinstance(statement.condition.left, Operation)):
            left = str(left.id1)+str(left.op)+str(left.id2)
        if(isinstance(statement.condition.right, Operation)):
            right = str(right.id1)+str(right.op)+str(right.id2)
        print('  '*tab_value+'while('+str(left)+str(statement.condition.condition)+str(right)+'):')
        tab_value+=1
        for element in statement.body:
            generate_code(element)
        tab_value-=1   
            

javaFile = readFile(filePath)
tokens = tokenizer(javaFile)

while(current<len(tokens)):
    statement = parser()
    if(statement!=None):
        syntax_tree.append(statement)
  
  
current = 0
while(current<len(syntax_tree)):
    statement = syntax_tree[current]
    generate_code(statement)
    current+=1