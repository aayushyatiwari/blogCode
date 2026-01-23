class SimpleFreqHashTable:
    '''
    Docstring for SimpleFreqHashTable
    
    simple hashtable to store frequency of lower case
    alphabets in an array of size 26.
    
    '''
    def __init__(self, size = 26):
        self.size = size
        self.hashTable = [0] * size

    def hash(self, key):
        '''
        Docstring for hash
        index using a - 0, b - 1 
        '''
        return ord(key) - ord('a')

    def insert(self, key):
        index = self.hash(key)
        if 0 <= index <= 26:
            self.hashTable[index]+=1
    
    def search(self, key):
        ind = self.hash(key) 
        return self.hashTable[ind]
    
def main():
    s = 'hashing'

    table = SimpleFreqHashTable()
    for ch in s:
        table.insert(ch)

    freq = table.search('h')
    print(f"Frequency of 'h': {freq}")  # Output: 2
    
    freq = table.search('g')
    print(f"Frequency of 'g': {freq}")  # Output: 2
    
    # Print the whole table
    print(f"\nHash table: {table.hashTable}")