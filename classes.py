class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Condition:
    def __init__(self, left, condition, right):
        self.left = left
        self.condition = condition
        self.right = right
    def __str__(self):
        return 'Condition(left:'+str(self.left)+', right:'+str(self.right)+', condition:'+str(self.condition)+')'

class If:
    def __init__(self, condition):
        self.condition = condition
        self.body = []

    def __str__(self):
        body = ''
        for element in self.body:
            body+=str(element)+'\n'
        return str(self.condition)+', Body:'+body

class While:
    def __init__(self, condition):
        self.condition = condition
        self.body = []

class Assign:
    def __init__(self, id):
        self.id = id
        self.nodes = []
        self.value = None
        self.type = None

    def assign_value(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return 'Assign(id:'+str(self.id)+', value:'+str(self.value)+', type:'+str(self.type)+')'

class Operation:
    def __init__(self, id1, id2, op):
        self.id1 = id1
        self.id2 = id2
        self.op = op

    def __str__(self):
        return 'Operation(id1:'+str(self.id1)+', id2:'+str(self.id2)+', op:'+str(self.op)+')'