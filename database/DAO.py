from database.DB_connect import DBConnect
from model.Arco import Arco
from model.artObject import ArtObject


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNodes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        res = []

        query = """SELECT *
                    FROM objects o """

        cursor.execute(query)

        for row in cursor:
            res.append(ArtObject(**row))

        cursor.close()
        cnx.close()

        return res

    @staticmethod
    def getPeso(u1, u2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        res = []

        query = """SELECT eo.object_id, eo2.object_id, count(*) AS peso
                    FROM exhibition_objects eo, exhibition_objects eo2 
                    WHERE eo.exhibition_id = eo2.exhibition_id and eo.object_id < eo2.object_id
                    and eo.object_id = %s and eo2.object_id = %s
                    GROUP BY eo.object_id, eo2.object_id"""

        cursor.execute(query, (u1.object_id, u2.object_id))

        for row in cursor:
            res.append(row["peso"])
        cursor.close()
        cnx.close()

        if len(res) == 0:
            return None
        return res


    @staticmethod
    def getAllArchi(idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        res = []

        query = """SELECT eo.object_id as o1, eo2.object_id as o2, count(*) AS peso
                        FROM exhibition_objects eo, exhibition_objects eo2 
                        WHERE eo.exhibition_id = eo2.exhibition_id and eo.object_id < eo2.object_id
                        GROUP BY eo.object_id, eo2.object_id
                        order by peso desc"""

        cursor.execute(query)

        for row in cursor:
            res.append(Arco(idMap[row["o1"]], idMap[row["o2"]], row["peso"]))
        cursor.close()
        cnx.close()


        return res


