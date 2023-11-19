import csv

def initializeinfo(id):
    filename = f"{id}.csv"
    
    with open(filename, "x", newline='') as file:
        csv_writer = csv.writer(file)
        info = {'liras': 0, 'Veggie': 0, 'Falafel': 0, 'Chicken': 0, 'Beef': 0}
        csv_writer.writerow(info.keys())  # Write the header row
        csv_writer.writerow(info.values())  # Write the data row


def update_entry(id, datatype, data):
    filename = f"{id}.csv"

    # Read the existing data from the CSV file into a dictionary
    with open(filename, "r", newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        data_row = next(csv_reader)    # Read the data row

    # Convert the header and data into a dictionary
    info = dict(zip(header, map(int, data_row)))

    # Update the specified entry with the new value
    data_row = info[datatype]

    info[datatype] = int(data)

    # Write the updated dictionary back to the CSV file
    with open(filename, "w", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(info.keys())    # Write the header row
        csv_writer.writerow(info.values())  # Write the data row

def readinfo(id):
    filename = f'{id}.csv'
    with open(filename, "r", newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        data_row = next(csv_reader)    # Read the data row
        info = dict(zip(header, map(int, data_row)))
    return info['liras'], info['Veggie'], info['Falafel'], info['Chicken'], info['Beef']
