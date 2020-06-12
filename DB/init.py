from neo4j import GraphDatabase 
db = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "MPB1324"))

# search node with propertes
session = db.session()
q1="MATCH (x) where x.from='LK' return (x)"
nodes=session.run(q1)
for node in nodes:
	print(node)

# create node with label
session = db.session()
q1="CREATE (N:TEAM)"
nodes=session.run(q1)
q2="MATCH (x:TEAM) return (x)"
nodes=session.run(q2)
for node in nodes:
	print(node)

# create node with label, propertes
session = db.session()
q1="CREATE (N:TEAM{name:'Mark'})"
nodes=session.run(q1)
q2="MATCH (x:TEAM) return (x)"
nodes=session.run(q2)
for node in nodes:
	print(node)