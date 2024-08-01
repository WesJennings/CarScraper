import datetime

def filters(miles, location, title, price, date):
    
    #max filters 
    miles_filter = 60000 #miles
    location_filter = 300 #range from me in miles
    price_filter = 25000 #dollar amount
    name_filter = "2020" #includes this in title
    date_filter = 50 #posted less than x days ago


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

    conditions.append(miles_num < miles_filter)
    conditions.append(location_num < location_filter)
    #conditions.append(name_filter in title.lower())
    conditions.append(price_num < price_filter)
    conditions.append(date_num < date_filter)

    return all(conditions)