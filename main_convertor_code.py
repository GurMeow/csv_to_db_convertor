import mysql.connector
import csv


def make_columns(data):
    columns = ""

    for j in range(len(data)):
        columns += data[j]

        columns += " VARCHAR(200)"

        if j != len(data)-1:
            columns += ", "

    return columns


def values_to_str(values):
    str_row = '"'
    str_row_str = [str(value) for value in values]
    str_row_str = '", "'.join(str_row_str)
    str_row += str_row_str
    str_row += '"'

    return str_row


my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ha@blablabla123",
    port="3306",
    database="csv_to_db"
)

my_cursor = my_db.cursor()

csv_file_rows_amount = 0

data_list = []

while True:
    while True:
        csv_file_path = input("Enter the file path: ")
        if csv_file_path[-4:] == ".csv" and csv_file_path[:45] == "C:\\Users\\Gur\\Documents\\csv_files_for_project\\":
            break
        else:
            print("file is not a csv type")
    try:
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)

            # Get the header
            header = next(csv_reader, None)

            # Add the header to the data list if it exists
            if header:
                data_list.append(header)

            # Add the remaining rows
            for row in csv_reader:
                data_list.append(row)
            csv_file_rows_amount = len(data_list) - 1
            break
    except FileNotFoundError as error:
        print(error)

print(data_list)

i = 0
columns_to_add = make_columns(data_list[0])

table_name = ""

for i in range(len(csv_file_path)-5, 0, -1):
    if csv_file_path[i] == "\\":
        break
    else:
        table_name += csv_file_path[i]

table_name = table_name[-1::-1]

my_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'csv_to_db'")
table_names = my_cursor.fetchall()

for table in table_names:
    if table[0] == table_name:
        my_cursor.execute(f"DROP TABLE {table_name}")
        my_cursor.execute("COMMIT")
        print("Table exists, dropping table")

my_cursor.execute(f"CREATE TABLE {table_name} ({columns_to_add})")
for j2 in range(1, len(data_list)):
    my_cursor.execute(f"INSERT INTO {table_name} VALUES ({values_to_str(data_list[j2])})")
my_cursor.execute("COMMIT")

print(f"Table {table_name} was created")
print(f"{csv_file_rows_amount} rows were created")
