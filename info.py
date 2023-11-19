import csv

def initializeinfo(id):
    filename = f"{id}.csv"
    
    with open(filename, "x", newline='') as file:
        csv_writer = csv.writer(file)
        info = {'liras': 0, 'donair_type1': 0, 'donair_type2': 0}
        csv_writer.writerow(info.keys())  # Write the header row
        csv_writer.writerow(info.values())  # Write the data row


def update_entry(id, datatype, data):
    filename = f"{id}.csv"

    # Read the existing data from the CSV file into a dictionary
    with open(filename, "r", newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        data = next(csv_reader)    # Read the data row

    # Convert the header and data into a dictionary
    info = dict(zip(header, data))

    # Update the specified entry with the new value
    info[datatype] = data

    # Write the updated dictionary back to the CSV file
    with open(filename, "w", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(info.keys())    # Write the header row
        csv_writer.writerow(info.values())  # Write the data row

def readinfo(id):
    with open(filename, "r", newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        data = next(csv_reader)    # Read the data row
        info = dict(zip(header, data))
    return info['liras'], info['donair_type1'], info['donair_type2']
