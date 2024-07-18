class LoadBatch:
    def __init__(self, name):
        self.name = name
        self.loads=[]

    def add_load(self, load):
        self.loads.append(load)

    def delete_loads(self):
        self.loads=[]

    def total_loads(self):
        return len(self.loads)