from string import Template

# >>> Info log templates ======================================================
info_log_values_template = Template("$ip,$a,$b,$c,$d")
info_log_template = Template(
    "INFO: $time PARAMS [ip, a, b, c, d]:\t$values_1\t$values_2\t$values_3\n")

# >>> Timed coordinates templates =============================================
timed_coordinate_kml_template = Template(
    """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
     xmlns:gx="http://www.google.com/kml/ext/2.2">
    <Folder>
        <Placemark>
            <gx:Track>
	        <extrude>1</extrude>
            <altitudeMode>absolute</altitudeMode>
$points
			</gx:Track>
        </Placemark>
    </Folder>
</kml>""")

point_template = Template(
    "           <when>$datetimez</when><gx:coord>$longitude $latitude $height</gx:coord>\n")

# >>> Styled coordinates templates ============================================
styled_coordinate_kml_template = Template(
    """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"
     xmlns:gx="http://www.google.com/kml/ext/2.2">
	<Document id="1">
		<Style id="bad">
			<IconStyle id="bad_1">
				<color>E63E31FF</color>
				<colorMode>normal</colorMode>
				<scale>1</scale>
				<heading>0</heading>
				<Icon id="bad_2">
					<href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
				</Icon>
			</IconStyle>
		</Style>
		<Style id="normal">
			<IconStyle id="normal_1">
				<color>E793FFFF</color>
				<colorMode>normal</colorMode>
				<scale>1</scale>
				<heading>0</heading>
				<Icon id="normal_2">
					<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
				</Icon>
			</IconStyle>
		</Style>
		<Style id="good">
			<IconStyle id="good_1">
				<color>FF499C54</color>
				<colorMode>normal</colorMode>
				<scale>1</scale>
				<heading>0</heading>
				<Icon id="good_2">
					<href>https://maps.google.com/mapfiles/kml/pushpin/grn-pushpin.png</href>
				</Icon>
			</IconStyle>
		</Style>
$placemarks
	</Document>
</kml>
""")

placemark_template = Template("""		<Placemark id="$id">
			<styleUrl>#$color</styleUrl>
			<Point id="$id">
				<coordinates>$longitude,$latitude,$height</coordinates>
			</Point>
		</Placemark>
""")
