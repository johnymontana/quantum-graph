# Import the Neo4j Python driver
from neo4j import GraphDatabase

# Connection credentials for our Neo4j database
NEO4J_URI = "neo4j://localhost"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "letmein"
NEO4J_DATABASE = "newsgraph"

# Create connection to Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Create a new QGIS vector layer
vlayer = QgsVectorLayer('LineString?crs=EPSG:4326', 'lines', 'memory')
provider = vlayer.dataProvider()
provider.addAttributes([QgsField('score', QVariant.Int)])
vlayer.updateFields()

# Set up graduated symbol renderer for proportional line widths
rangeList = []
#color = QtGui.QColor('#ffee00')

symbol1 = QgsSymbol.defaultSymbol(vlayer.geometryType())
symbol1.setWidth(0.5)
#symbol1.setColor(color)
range1 = QgsRendererRange(0, 7, symbol1, 'Group 1')
rangeList.append(range1)

symbol2 = QgsSymbol.defaultSymbol(vlayer.geometryType())
symbol2.setWidth(0.75)
#symbol2.setColor(color)
range2 = QgsRendererRange(8, 12, symbol2, 'Group 2')
rangeList.append(range2)

symbol3 = QgsSymbol.defaultSymbol(vlayer.geometryType())
symbol3.setWidth(1.25)
#symbol3.setColor(color)
range3 = QgsRendererRange(12, 1000, symbol3, 'Group 3')
rangeList.append(range3)

renderer = QgsGraduatedSymbolRenderer('', rangeList)
classificationMethod = QgsApplication.classificationMethodRegistry().method("EqualInterval")
renderer.setClassificationMethod(classificationMethod)
renderer.setClassAttribute('score')
vlayer.setRenderer(renderer)

# Cypher query to fetch geographic area co-occurances
LINE_GEOMETRY_QUERY = """
MATCH (g1:Geo)<-[:ABOUT_GEO]-(:Article)-[:ABOUT_GEO]->(g2:Geo) 
WHERE g1.location IS NOT NULL AND g2.location IS NOT NULL
WITH g1, g2, COUNT(*) AS score 
WHERE g1.location.longitude < g2.location.longitude
RETURN g1.location.latitude AS g1lat, 
       g1.location.longitude AS g1lon, 
       g2.location.latitude AS g2lat, 
       g2.location.longitude AS g2lon, 
       score ORDER BY score DESC LIMIT 100
"""

# Function to run Cypher query and process results
def get_lines(tx):
    lines = []
    result = tx.run(LINE_GEOMETRY_QUERY)
    for record in result:
        lines.append({"score": record["score"], "g1lat": record["g1lat"], "g1lon": record["g1lon"], "g2lat": record["g2lat"], "g2lon": record["g2lon"]})
    return lines
    

d = QgsDistanceArea()
d.setEllipsoid('WGS84')

# Execute Cypher query and create features
with driver.session(database=NEO4J_DATABASE) as session:
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

# Add vector layer
vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)
         
        
    