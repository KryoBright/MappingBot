from neo4j import GraphDatabase 

db = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "MPB1324"))
session = db.session()