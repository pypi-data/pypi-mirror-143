
# Museum_API_conversions

Converts Museum_API objectIDs into pdf, html, csv and xml files.

## usage

Make sure you have python installed in your system

Run following command in command prompt

pip install Museum_API_conversions 

## Example

import ArtCollection

var = ArtColection.MuseumAPI(Museum_API_url)

df = var.api_to_dataframe(1, 5)

The above step is must in order to convert dataframe into html, csv and xml

csv_file = 'Museum_API_5to8.csv'

html_file = 'Museum_API_5to8.html'

xml_file = 'Museum_API_5to8.xml'

pdf_file = 'Museum_API_5to8.pdf'

api.dataframe_to_csv(df, csv_file)


var.dataframe_to_html(df, html_file)


var.html_to_pdf(html_file, pdf_file)


var.dataframe_to_xml(df, xml_file)

## parameters

Museum_API(url=Museum_API_url)

url contains the url of Museum_API objectIDs

var.api_to_dataframe(st=None, sp=None)

default st and sp will be 0 to 50

if st parameter is None then by default it will be 0

if sp parameter is None then by default it will be st+50

## Note

objectIDs are between 0 and 830985