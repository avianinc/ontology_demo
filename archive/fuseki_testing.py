from pyfuseki import FusekiUpdate, FusekiQuery

fuseki_update = FusekiUpdate('localhost:3030', 'test_db')
fuseki_query = FusekiQuery('localhost:3030', 'test_db')


from pyfuseki.rdf import rdf_prefix, NameSpace as ns
from pyfuseki.rdf import NameSpace

@rdf_prefix('http://expample.com/')
class RdfPrefix():
    Person: ns
    Dog: ns
    neA = NameSpace('http://expample.com/1A/')

rp = RdfPrefix()

from pyfuseki.rdf import rdf_property
from rdflib import URIRef as uri

@rdf_property('http://example.org/')
class ObjectProperty:
    own: uri 

@rdf_property('http://example.org/')
class DataProperty:
    hasName: uri

# example instances
person = rp.Person['12345']  #
dog = rp.Dog['56789']  # 

print(person)

# Lets build the graph
from rdflib import Graph
g = Graph()

from rdflib import RDF

person = rp.Person['12345'] 
stmt = (person, RDF.type, rp.Person.to_uri())

g.add((person, RDF.type, rp.Person.to_uri()))  # 声明 person 的类型是 Person
g.add((dog, RDF.type, rp.Dog.to_uri()))

fuseki = FusekiUpdate('http://localhost:3030', 'test_db')
fuseki.insert_graph(g)
