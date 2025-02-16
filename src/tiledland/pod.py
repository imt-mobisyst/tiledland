class Podable():
    def asPod(self):
        # Should return self as a Pod instance
        assert "Should be implemented" == None
        
    def fromPod(self):
        # Should rebuild self from a Pod instance
        assert "Should be implemented" == None
      
    # Object construction:
    def podCopy( self ):
        return type(self)().fromPod( self.asPod() )
  
class Pod(Podable):
    def __init__( self ):
        self._words= []
        self._integers= []
        self._values= []
        self._children= []
        
    def fromLists(self, words, integers, values, children):
        self._words= words
        self._integers= integers
        self._values= values
        self._children= children
        return self
    
    # Object abstrac accessor:
    def words(self):
        return self._words
    
    def integers(self):
        return self._integers
    
    def values(self):
        return self._values
    
    def children(self):
        return self._children
    
    # Podable:
    def asPod( self ):
        return Pod().fromLists(
            self.words(),
            self.integers(),
            self.values(),
            [ child.asPod() for child in self.children() ]
        )
    
    def fromPod( self, aPod ):
        self._words= aPod.words(),
        self._integers= aPod.integers(),
        self._values= aPod.values(),
        self._children= [ Pod().fromPod(child) for child in aPod.children() ]
        return self
    
    # Accessor:
    def numberOfWords(self):
        return len( self.words() )
    
    def word(self, i=1):
        return self.words()[i-1]
    
    def numberOfIntegers(self):
        return len( self.integers() )
    
    def integer(self, i=1):
        return self.integers()[i-1]
    
    def numberOfValues(self):
        return len( self.values() )
    
    def value(self, i=1):
        return self.values()[i-1]
    
    def numberOfChildren(self):
        return len( self.children() )

    def child(self, i=1):
        return self.children()[i-1]

    # Comparison:
    def __eq__(self, another):
        return (
            self._words == another.words()
            and self._integers == another.integers()
            and self._values == another.values()
            and self._children == another.children()
        )
    

