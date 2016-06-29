
#########
# script to:
# 1. access records in fulcrum form 
# 2. put specified fields into a list
# 3. check if the fulcrum_id already exist in a PostGIS query, send sql insert statement if not
# 4. SQL insert statement includes where not exists clause to check if fulcrum_id already exists and if not inserts them


from fulcrum import Fulcrum
import psycopg2

# create a fulcrum client with my API key
fulcrum = Fulcrum(key='my_api_key')

# search for a fulcrum_id, returns all relating to the url_params
records = fulcrum.records.search(url_params={'form_id': '485688d9-aca6-4586-a624-260b0ca71c6a'})

# find number of records in form
record_count = len(records['records']) # returns int

# set multiple fields of records in range of record_count
# to work out which form values to use look at a single record from records variable
info = []
for i in range(record_count):
	# append required fields
	info.append(
		[
		records['records'][i]['id'],
		records['records'][i]['created_by'],
		records['records'][i]['created_at'],
		records['records'][i]['latitude'],
		records['records'][i]['longitude'],
		records['records'][i]['status'],
		records['records'][i]['form_values']['72e8']['choice_values'][0] # feature type
		]
	)
	# append non-required fields, fields will not be present if non-required and empty
	# if key exists append it, if not then append ''
	key = '170f' # comments
	if key in records['records'][i]['form_values']:
		info[i].append(records['records'][i]['form_values'][key])
	else:
		info[i].append('')
		
# connect to db		
conn = psycopg2.connect(dbname="dbname", port=0000, user="user", password="password", host="host")
# cur = conn.cursor()

# select current fulcum_id in the table
query_fulcrum_id = """
	SELECT
		fulcrum_id
	FROM
		schema.feature_survey
	"""

cur = conn.cursor()
cur.execute(query_fulcrum_id)
# fetch result as tuples
result = cur.fetchall()
# close the transaction, we just did a select query so no need to commit
conn.rollback()
# convert tuples to list
result_list = [i for sub in result for i in sub]

# create a query string to insert selected records if their fulcrum_id does not already exist
query = """
	INSERT INTO schema.feature_survey (
		fulcrum_id, 
		created_by,
		created_at,
		latitude,
		longitude,
		status,
		feature_type,
		comments
	)
	SELECT 
	%s,
	%s,
	%s,
	%s,
	%s,
	%s,
	%s,
	%s
	WHERE NOT EXISTS (
			SELECT fulcrum_id 
			FROM schema.feature_survey
			WHERE feature_survey.fulcrum_id = %s
		)
	"""

# check if downloaded fulcrum_id are already within the database, do nothing if they are, insert them if they are not
for f in info:
	if f[0] in result_list:
		print(str(f[0]) + '...is present')
		# tell us if present
	else:
		print(str(f[0]) + '...is not present')
		# insert if not present
		q = "{0}".format(query)
		cur = conn.cursor()
		print(str(f[0]) + '...executing query for record')
		cur.execute(q, (
			f[0], # fulcrum_id
			f[1], # created_by
			f[2], # created_at
			f[3], # latitude
			f[4], # longitude
			f[5], # status
			f[6], # feature_type
			f[7], # comments
			f[0] # fulcrum_id
			)
		)
		print(str(f[0]) + '...commiting query for record')
		conn.commit() # commit or rollback() every query to end the transaction
		cur.close()
		
conn.close()
