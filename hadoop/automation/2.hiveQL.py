from pyhive import hive
import pandas as pd

conn = hive.Connection(
    host='localhost',
    port=10000,
    username='ubunto',
)

cursor = conn.cursor()

query = '''
SELECT * FROM logs LIMIT 10
'''

# query = '''
# SELECT 
#     ip_address,
#     COUNT(*)
# FROM
#     logs
# GROUP BY
#     ip_address
# ORDER BY
#     COUNT(*) DESC
# LIMIT 10
# '''

# query = '''
# SELECT
#     SPLIT(request_path, '/')[2] AS product_id,
#     COUNT(*) AS request_count
# FROM
#     logs
# WHERE
#     request_path LIKE '/product/%'
# GROUP BY
#     SPLIT(request_path, '/')[2]
# ORDER BY
#     request_count DESC
# LIMIT 10
# '''

cursor.execute(query)

result = cursor.fetchall()

df = pd.DataFrame(result)

output_path = '/home/ubunto/dmf/automation/logs-result/'
output_file = 'request_result.csv'

df.to_csv(output_path + output_file)