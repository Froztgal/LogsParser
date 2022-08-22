from string import Template

kml_template = Template("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
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

placemark = Template("""		<Placemark id="$id">
			<styleUrl>#$color</styleUrl>
			<Point id="$id">
				<coordinates>$longitude,$latitude,$height</coordinates>
			</Point>
		</Placemark>
""")
