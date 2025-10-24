#!/usr/bin/env python3

kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Path from Pico</name>
    <Style id="pointStyle">
      <IconStyle>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>
        <scale>1.0</scale>
      </IconStyle>
    </Style>
    <Style id="lineStyle">
      <LineStyle><color>ff0000ff</color><width>3</width></LineStyle>
    </Style>
    <Placemark>
      <styleUrl>#pointStyle</styleUrl>
      <MultiGeometry>
"""

kml_points = ""
coordinates_line = ""
cvs_file = "ultimateGPStracker.log.OnPC.log"

with open(cvs_file, 'r', encoding='utf-8') as filePChandle:
    for line in filePChandle:
        # remove       all        leading       and       trailing
        # whitespace(spaces,tabs,and newlines)
        line = line.strip()
        if not line:
            # skip over blank lines
            continue

        # splits the stirng in two parts at the , delimiter
        latitude, longitude = line.split(',')
        kml_points += f"<Point><coordinates>\n{longitude},{latitude}\n</coordinates></Point>\n"
        coordinates_line += f"{longitude},{latitude} \n"

kml_footer = f"""</MultiGeometry>
    </Placemark>
    <Placemark>
      <name>Path</name>
      <styleUrl>#lineStyle</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <altitudeMode>clampToGround</altitudeMode>
        <coordinates>
        {coordinates_line}
        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
"""

kml_content = kml_header + kml_points + kml_footer
kml_file = "ultimateGPStracker.log.OnPC.log.kml"

with open(kml_file, 'w',
          encoding='utf-8') as filePChandle:
    filePChandle.write(kml_content)

print(f"KML file {kml_file} created successfully.")
