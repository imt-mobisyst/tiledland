class AbsObj():

    # Object abstrac accessor:
    def wordAttributes(self):
        # Should return the list of word attributes
        assert "Should be implemented" is None
    
    def intAttributes(self):
        # Should return the list of integer attributes
        assert "Should be implemented" is None
    
    def floatAttributes(self):
        # Should return the list of floating point attributes
        assert "Should be implemented" is None

    def children(self):
        # Should return the list of AbsObj children
        assert "Should be implemented" is None

    # Object abstrac construction:
    def initializeFrom( self, anAbsObj ):
        # Should initialize self with anAbsObj
        assert "Should be implemented" is None
        return self
    
    # Object accessor:
    def numberOfWords(self):
        return len( self.wordAttributes() )
    
    def wordAttribute(self, i=1):
        return self.wordAttributes()[i-1]
    
    def numberOfInts(self):
        return len( self.intAttributes() )
    
    def intAttribute(self, i=1):
        return self.intAttributes()[i-1]
    
    def numberOfFloats(self):
        return len( self.floatAttributes() )
    
    def floatAttribute(self, i=1):
        return self.floatAttributes()[i-1]
    
    def numberOfChildren(self):
        return len( self.children() )

    def child(self, i=1):
        return self.children()[i-1]

    # Object construction:
    def copy( self ):
        return type(self)().initializeFrom(self)
    

