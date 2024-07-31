import datetime

def filters(miles, location, title, price, date):
    
    #max filters 
    miles_filter = 150000 #miles
    location_filter = 300 #range from me in miles
    price_filter = 5000 #dollar amount
    name_filter = ["", ""] #includes this in title
    date_filter = 5000 #posted less than x days ago
    

    miles_num = int(miles.split()[0].replace(',', '')) #turns html string into number for for loop

    price_num = int(price.replace('$', '').replace(',', ''))
    #checks if its in x days ago format vs mon day format -- figure out how to change date into days ago later 
    if 'ago' in date:
        date_num = int(date.split()[0])
    elif 'Yesterday' in date:
        date_num = 1
    elif 'Today' in date:
        date_num = 0
    else:
        #formats month day into x days ago
        date_num = date.replace('nd', '').replace('st', '').replace('th', '').replace('rd', '') #ignore that its still named num even though string
        current_year = datetime.datetime.now().year
        
        #check if year is in date
        if ',' in date_num:
            format_data = "%b %d, %Y"
        else:
            date_num += f" {current_year}"
            format_data = "%b %d %Y"
        
        current_date = datetime.datetime.now()
        
        car_date = datetime.datetime.strptime(date_num, format_data)
        date_num = (current_date - car_date).days
                        

    location_num = int(location.replace('(','').split()[0]) #in miles as int

    conditions = []

    truefalse = bool(0)
    
    for index, n in enumerate(name_filter):
        if n.lower() in title.lower():
            truefalse = bool(1)

    conditions.append(truefalse)
    conditions.append(miles_num < miles_filter)
    conditions.append(location_num < location_filter)
    conditions.append(price_num < price_filter)
    conditions.append(date_num < date_filter)

    return all(conditions)