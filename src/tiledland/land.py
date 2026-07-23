
class Avatar():
    def __init__(self, index, body, agent):
        self._body= body
        self._agent= agent
    
    # accessor: 
    def agent(self):
        return self._agent

    def body(self):
        return self._body

class Land():
    def __init__(self, aMap):
        self._map= aMap
        self._avatars= []
    