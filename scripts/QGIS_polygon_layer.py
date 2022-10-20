# Import the Neo4j Python driver
from neo4j import GraphDatabase

# Connection credentials for our Neo4j database
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "letmein"
NEO4J_DATABASE = "landgraph"

# Create connection to Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Create a new QGIS vector layer
vlayer = QgsVectorLayer('Polygon?crs=EPSG:4326', 'polygons', 'memory')
provider = vlayer.dataProvider()
provider.addAttributes([QgsField('name', QVariant.String)])
vlayer.updateFields()

# Cypher query to fetch polygon geometries from Neo4j
POLYGON_GEOMETRY_QUERY = """
MATCH (p:Parcel)-[r:HAS_GEOMETRY]->(g:Geometry)
WHERE p.GIS_Acres > 100
RETURN p.name AS name, [c IN g.coordinates | {lat:c.latitude, lon: c.longitude }] AS coords
"""

def get_polygons(tx):
    polygons = []
    result = tx.run(POLYGON_GEOMETRY_QUERY)
    for record in result:
        polygons.append({"name": record["name"], "coords": record["coords"]})
    return polygons
    

d = QgsDistanceArea()
d.setEllipsoid('WGS84')

# Execute Cypher query and create features
with driver.session(database=NEO4J_DATABASE) as session:
    polys = session.execute_read(get_polygons)
    for p in polys:
        f  = QgsFeature()
        f.setGeometry(QgsGeometry.fromPolygonXY([[QgsPointXY(pair['lon'], pair['lat']) for pair in p['coords']]]  ))
        f.setAttributes([p['name']])
        provider.addFeature(f)

# Add vector layer
vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)
         
        
    