#Basic OOP is needed to work with Data Structures

class Node:
    def __init__(self,value=None,next=None) -> None:
        self.value = value
        self.next = next

class LinkedList:
    def __init__(self) -> None:
        self.head = None

    def insert():
        pass

    def delete():
        pass

n1 = Node(3)
n2 = Node(7)
n3 = Node(2)
n4 = Node(9) 

LL = LinkedList()
LL.head = n1 #head

n1.next = n2 #connect 3 to 7
n2.next = n3 #connect 7 to 2
n3.next = n4 #connect 2 to 9