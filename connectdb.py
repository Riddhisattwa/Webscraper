from pymongo import MongoClient
from bson.code import Code
class Dbfunction:

    def __init__(self,host,port,dbname,collection,username=None,password=None):

        self.host=host
        self.port=port
        self.dbname=dbname
        self.username=username
        self.password=password
        self.collection=collection


    def connectMongo(self):

        if(self.username!=None):
            connectionString='mongodb://'+self.username+':'+self.password+'@'+self.host+':'+self.port
        else:
            connectionString = 'mongodb://' + self.host + ':' + self.port

        client=MongoClient(connectionString)
        db=client.get_database(self.dbname)
        return db

    def upsert(self,payload,oldpayload=None):

        db=self.connectMongo()
        col=db.get_collection(self.collection)
        post_id=col.update(oldpayload,payload,upsert=True)
        db.logout()
        return post_id

    def deleteData(self,payload):

        db=self.connectMongo()
        col=db.get_collection(self.collection)
        post_id=col.delete_one(payload)
        db.logout()
        return post_id.acknowledged

    def mapReduce(self,map_file,reduce_file):

        db=self.connectMongo()
        col=db.get_collection(self.collection)

        #load map and reduce files

        map=Code(open(map_file).read())
        reduce=Code(open(reduce_file).read())

        #perform mapreduce
        results=col.map_reduce(map,reduce,out="map_reduce_example")
        return results






