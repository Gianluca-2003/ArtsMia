from database.DAO import DAO
from model.model import Model

listObject = DAO.getAllNodes()
my_model = Model()
my_model.buildGraph()

edges = DAO.getAllArchi(my_model.getIdMap())





print(len(listObject), len(edges))