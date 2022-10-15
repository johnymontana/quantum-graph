from neo4j import GraphDatabase

# Fetch points from Neo4j and create layer


NEO4J_URI = "neo4j://news.graph.zone:7687"
NEO4J_USER = "newsgraph"
NEO4J_PASSWORD = "newsgraph"
NEO4J_DATABASE = "neo4j"


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

vlayer = QgsVectorLayer('LineString?crs=EPSG:4326', 'lines', 'memory')
provider = vlayer.dataProvider()

provider.addAttributes([QgsField('score', QVariant.Int)])
vlayer.updateFields()

# TODO: add names to return
LINE_GEOMETRY_QUERY = """
MATCH (g1:Geo)<-[:ABOUT_GEO]-(:Article)-[:ABOUT_GEO]->(g2:Geo) 
WHERE g1.location IS NOT NULL AND g2.location IS NOT NULL
WITH g1, g2, COUNT(*) AS score WHERE g1.location.longitude < g2.location.longitude
RETURN g1.location.latitude AS g1lat, 
       g1.location.longitude AS g1lon, 
       g2.location.latitude AS g2lat, 
       g2.location.longitude AS g2lon, 
       score ORDER BY score DESC LIMIT 100
"""

def get_lines(tx):
    lines = []
    result = tx.run(LINE_GEOMETRY_QUERY)
    for record in result:
        lines.append({"score": record["score"], "g1lat": record["g1lat"], "g1lon": record["g1lon"], "g2lat": record["g2lat"], "g2lon": record["g2lon"]})
    return lines
    

d = QgsDistanceArea()
d.setEllipsoid('WGS84')

# TODO: add name pairs to attribut table
# TODO: style thickness of line based on score value
with driver.session() as session:
    lines = session.execute_read(get_lines)
    for l in lines:
        point1 = QgsPointXY(l['g1lon'], l['g1lat'])
        point2 = QgsPointXY(l['g2lon'], l['g2lat'])
        vertices = d.geodesicLine(point1, point2, 10000)
        geodesic_line = QgsGeometry.fromPolylineXY(vertices[0])
        f = QgsFeature()
        f.setGeometry(geodesic_line)
        f.setAttributes([l['score']])
        provider.addFeature(f)

vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)
         
        
    