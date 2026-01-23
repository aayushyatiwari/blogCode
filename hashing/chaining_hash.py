
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class HashChaining:
    '''
    assumption:

    hash function will return an integer from 0 to 19
    '''

    def __init__(self, size = 20):
        self.size = size
        self.table = [None] * size


    def hash(self, key):
        if isinstance(key, str):
            return ord(key) % self.size
        return key % self.size

## i made a lot of mistakes implementing this func !! :(
    def insert(self, s):
        index = self.hash(s)
        if self.table[index] is None:
            head = Node(s)
            self.table[index] = head
        else:
            new = Node(s) 
            new.next = self.table[index] 
            self.table[index]= new

    def search(self, s):
        index = self.hash(s)
        if self.table[index] is None:
            return "not hashed"
        l = self.table[index] 
        curr = l
        while curr:
            if curr.val == s:
                return "found the value"
            curr = curr.next
        return "THE VALUE ISNT PRESENT"

def main():
    ht = HashChaining(size=5)
    
    # Insert with collisions
    ht.insert('a')  # hash = 2
    ht.insert('f')  # hash = 2 (collision!)
    ht.insert('b')  # hash = 3
    
    # Search
    print(ht.search('a'))  # Should find
    print(ht.search('f'))  # Should find
    print(ht.search('z'))  # Should NOT find
    
    # Visualize
    for i in range(5):
        curr = ht.table[i]
        chain = []
        while curr:
            chain.append(curr.val)
            curr = curr.next
        print(f"{i}: {chain if chain else None}")
