"""
Gets a copy of the AGOL layer for parking inventory.
Creates a lookup table between parking kioks and parkATX zones
"""
import urllib.request
import json
import csv

# specify the URL of the JSON file
QUERY = "https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/Parking_Inventory/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&relationParam=&returnGeodetic=false&outFields=STATION_NUMBER%2C+ZONE_DESCRIPTION&returnGeometry=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&defaultSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="

# download the JSON file
response = urllib.request.urlopen(QUERY)
data = json.loads(response.read())

# specify the output CSV filename
output_filename = "kisoks_to_zones.csv"

# open the output CSV file for writing
with open(output_filename, "w", newline="") as csvfile:
    # create a CSV writer object
    writer = csv.writer(csvfile)

    # write the header row
    writer.writerow(data["features"][0]["attributes"].keys())

    # write the data rows
    for row in data["features"]:
        writer.writerow(row["attributes"].values())
