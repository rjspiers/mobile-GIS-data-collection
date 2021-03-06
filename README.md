# Mobile data collection

## Flow chart

![flow chart image](https://raw.githubusercontent.com/rjspiers/mobile-GIS-data-collection/master/gis%20flowchart%20for%20github.png)


## Recording data in Fulcrum

Example form to report faults with assets on the Android/iOS Fulcrum app:

<img src="https://raw.githubusercontent.com/rjspiers/mobile-GIS-data-collection/master/fulcrum_form_example.png" width=30%>

## Importing data from Fulcrum

This python script [fulcrum_access_data.py](fulcrum_access_data.py) connects to a Fulcrum form, stores the form records in a variable, checks if fulcrum_id already exists in a PostGIS table and if not inserts the new records.

## Running the script
Change the variables for 

1. Fulcrum API Key: 
	```python
	Fulcrum(key='my_api_key')
	```

1. Form ID: 
	
	```python
	records = fulcrum.records.search(url_params={'form_id': '485688d9-aca6-4586-a624-260b0ca71c6a'})
	```

1. Fields to select from the Fulcrum form: 
	
	```python
	records['records'][i]['id']
	```

1. PostGIS db connection: 
	
	```python
	conn = psycopg2.connect(dbname="dbname", port=0000, user="user", password="password", host="host")
	```

1. The fields in query variable 
	
	```python
	query = """INSERT..."""
	```

1. And the corresponding list items in the cur.execute (line 106-115): 
	
	```python
	f[0], # fulcrum_id
	```



### Run the script in python using:

`
C:\Python27\python.exe fulcrum_access_data.py
`

## iShare Studio workflow
Schedule the script as a job in iShare Studio by using a .bat file to issue python commands.

Batch file content:

```bat
C:\Python27\python.exe fulcrum_access_data.py
```

iShare Studio workflow job:

![workflow job image](https://raw.githubusercontent.com/rjspiers/mobile-GIS-data-collection/master/iShare_studio_job.PNG)

## Links
- [Astun - iShare](https://astuntechnology.com/)
- [Fulcrum](http://www.fulcrumapp.com/)
- [GIS Cloud](http://www.giscloud.com/)
