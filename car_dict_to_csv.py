import csv

def to_csv_file(car_dict):
    headers = car_dict[0].keys()

    file = open("scraped_cars.csv", "w")
    
    fields = []
    for header in headers:
        fields.append(header)
    
    #create writer object
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(car_dict)

    file.close()