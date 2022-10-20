# Import the Neo4j Python driver
from neo4j import GraphDatabase
from qgis.PyQt import QtGui

# Connection credentials for our Neo4j database
NEO4J_URI = "neo4j://localhost"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "letmein"
NEO4J_DATABASE = "newsgraph"

# Create connection to Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Create a new QGIS vector layer
vlayer = QgsVectorLayer('Point?crs=EPSG:4326', 'points', 'memory')
provider = vlayer.dataProvider()
provider.addAttributes([QgsField('name', QVariant.String), QgsField('degree', QVariant.Int)])
vlayer.updateFields()


# Set up graduated symbol renderer for proportional symbol size
rangeList = []
color = QtGui.QColor('#ffee00')

symbol1 = QgsSymbol.defaultSymbol(vlayer.geometryType())
symbol1.setSize(2)
#symbol1.setColor(color)
range1 = QgsRendererRange(0, 15, symbol1, 'Group 1')
rangeList.append(range1)

symbol2 = QgsSymbol.defaultSymbol(vlayer.geometryType())
symbol2.setSize(4)
#symbol2.setColor(color)
range2 = QgsRendererRange(16, 200, symbol2, 'Group 2')
rangeList.append(range2)

symbol3 = QgsSymbol.defaultSymbol(vlayer.geometryType())
symbol3.setSize(6)
#symbol3.setColor(color)
range3 = QgsRendererRange(201, 1000, symbol3, 'Group 3')
rangeList.append(range3)

renderer = QgsGraduatedSymbolRenderer('', rangeList)
classificationMethod = QgsApplication.classificationMethodRegistry().method("EqualInterval")
renderer.setClassificationMethod(classificationMethod)
renderer.setClassAttribute('degree')
vlayer.setRenderer(renderer)



# Cypher query to fetch point geometries
POINT_GEOMETRY_QUERY = """
MATCH (g:Geo) WHERE g.location IS NOT NULL
RETURN SIZE( (g)<-[:ABOUT_GEO]-(:Article) ) AS degree, 
g.name AS name, g.location.latitude AS lat, 
g.location.longitude AS lon ORDER BY degree DESC"""

# Function to run Cypher query and process results
def get_points(tx):
    points = []
    result = tx.run(POINT_GEOMETRY_QUERY)
    for record in result:
        points.append({"name": record["name"], "lat": record["lat"], "lon": record["lon"], "degree": record["degree"]})
    return points

# Execute Cypher query and create features
with driver.session(database=NEO4J_DATABASE) as session:
    points = session.execute_read(get_points)
    for p in points:
        f  = QgsFeature()
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(p['lon'], p['lat'])))
        f.setAttributes([p['name'], p['degree']])
        provider.addFeature(f)

# Add vector layer
vlayer.updateExtents()
QgsProject.instance().addMapLayer(vlayer)
    