from .map import Map

class Avatar():
    def __init__(self, index, body, agent):
        self._id= index
        self._body= body
        self._agent= agent
    
    # accessor: 
    def agent(self):
        return self._agent

    def body(self):
        return self._body

class Land():
    def __init__(self, aMap= None):
        self._map= aMap
        if self._map is None :
            self._map= Map()
        self._avatars= [ Avatar(0, None, None) ]
    
    # Accessor:
    def map(self):
        return self._map

    def agent(self, identifier):
        return self._avatars[identifier].agent()

    def body(self, identifier):
        return self._avatars[identifier].body()
    
    # Construction:
    def tileAppendAvatar(self, iTile, body, agent ):
        newId= len(self._avatars)
        self._map.tileAppendEntity( iTile, body )
        self._avatars.append( Avatar(newId, body, agent) )
        return newId

