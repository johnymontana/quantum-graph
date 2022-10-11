from neo4j import GraphDatabase

# Fetch points from Neo4j and create layer


NEO4J_URI = "neo4j://news.graph.zone:7687"
NEO4J_USER = "newsgraph"
NEO4J_PASSWORD = "newsgraph"
NEO4J_DATABASE = "neo4j"


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

vlayer = QgsVectorLayer('Point?crs=EPSG:4326', 'points', 'memory')
provider = vlayer.dataProvider()
provider.addAttributes([QgsField('name', QVariant.String)])
vlayer.updateFields()

# TODO: add degree value
POINT_GEOMETRY_QUERY = """
MATCH (g:Geo) WHERE g.location IS NOT NULL
RETURN g.name AS name, g.location.latitude AS lat, g.location.longitude AS lon
"""

def get_points(tx):
    points = []
    result = tx.run(POINT_GEOMETRY_QUERY)
    for record in result:
        points.append({"name": record["name"], "lat": record["lat"], "lon": record["lon"]})
    return points

# TODO: style point size based on degree value    
with driver.session() as session:
    points = session.execute_read(get_points)
    for p in points:
        f  = QgsFeature()
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(p['lon'], p['lat'])))
        f.setAttributes([p['name']])
        provider.addFeature(f)

vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)
    