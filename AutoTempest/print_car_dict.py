
def print_dict(car_dict):
    if car_dict:
        headers = car_dict[0].keys() #gets headers from list
        for index, car in enumerate(car_dict):
            print(f"Car #{index + 1}")
            for header in headers:
                print(f"{header}: {car[header]}")
            print("\n")
    else:
        print("empty")