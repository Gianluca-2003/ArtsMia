from model.model import Model

myModel = Model()
myModel.buildGraph()

print("Numero nodi:",myModel.getNumNodes())
print("Numero archi:",myModel.getNumEdges())


myModel.getInfoConnessa(1234)