import json,requests
import MySQLdb as mysql
#get request for all the cuisine categories in Kolkata (city_id = 2)
h = {'user-key':'8dcbce9bb51cc0ac55982b69981c7dc3','Accept': 'application/json'}
r = requests.get('https://developers.zomato.com/api/v2.1/cuisines?city_id=2',headers=h)
cuisine = {}
for dicts in r.json()['cuisines']:
    cuisine[dicts['cuisine']['cuisine_id']] = dicts['cuisine']['cuisine_name']
part = 'https://developers.zomato.com/api/v2.1/search?entity_id=2&entity_type=city&cuisines='
restaurants = []
for cid,val in cuisine.iteritems():
    url = part + str(cid)
    r = requests.get(url,headers=h)
    data = r.json()
    if data['results_found'] > 500:
        for i in range(data['results_shown']):
            temp = data['restaurants'][i]['restaurant']
            tdict = {}
            tdict['res_id'] = temp['R']['res_id']
            tdict['cuisine_id'] = cid
            tdict['rating'] = float(temp['user_rating']['aggregate_rating'])
            try:
                tdict['name'] = str(temp['name'])
                tdict['image'] = str(temp['featured_image'])
                tdict['address'] = str(temp['location']['address'])
            except UnicodeEncodeError:
                tdict['name'] = temp['name']
                tdict['image'] = temp['featured_image']
                tdict['address'] = temp['location']['address']
            restaurants.append(tdict)
#Now,connect to the database and create the tables
db = mysql.connect("127.0.18.102","14CS30008","dual14","OFDS")
cursor = db.cursor()
#check for existing table named 'categories',drop them and create a new one as per our requirements
test1 = """drop table if exists `categories`;"""
cursor.execute(test1)
table1 = """CREATE TABLE categories (
         cuisine_id INT NOT NULL,
         cname  CHAR(30),
         PRIMARY KEY (cuisine_id))"""
cursor.execute(table1)
#add popular entries to 'categories' table
popular = []
for res in restaurants:
    popular.append(res['cuisine_id'])
popular = set(popular)
sql = "INSERT INTO categories(cuisine_id,cname) VALUES ('%d', '%s')"
for id,name in cuisine.iteritems():
    try:
        if id in popular:
            cursor.execute(sql%(id,name))
            db.commit()
    except:
        db.rollback()
    
test2 = """drop table if exists `restaurants`;"""
cursor.execute(test2)
table2 = """CREATE TABLE restaurants (
         res_id INT NOT NULL AUTO_INCREMENT,
         cuisine_id INT NOT NULL,
         name CHAR(100),
         address TEXT,
         image_url TEXT,
         rating FLOAT,
         PRIMARY KEY (res_id))"""
cursor.execute(table2)
#add entries to 'restaurant' table
sql = """INSERT INTO restaurants(cuisine_id,res_id,
        name,address,image_url,rating) VALUES ( 
        '%d', '%s', '%s', '%s', '%f')"""
for res in restaurants:
    try:
        cursor.execute(sql%(res['cuisine_id'],res['name'],res['address'],res['image'],res['rating']))
        db.commit()
    except:
        db.rollback()

#create a table for storing the menu items of every restaurant
test3 = """drop table if exists `menu`;"""
cursor.execute(test3)
table3 = """CREATE TABLE menu (
         menu_id INT NOT NULL AUTO_INCREMENT,
         res_id INT NOT NULL,
         name CHAR(100),
         price FLOAT,
         type CHAR(20),
         category CHAR(20),
         PRIMARY KEY (menu_id))"""
cursor.execute(table3)
#Now,add random menu entries to every restaurant from the table
ids = []
for res in restaurants:
    ids.append(res['res_id'])
ids = set(ids)
sql = """INSERT INTO menu(res_id,name,price,type,category) values
({0},"Vegetable Pakora","3.00","Veg","Starters"),
({0},"Vegetable Samosa","3.00","Veg","Starters"),
({0},"Onion Bhaji ","3.00","Veg","Starters"),
({0},"Potato and Mushroom Chaat","3.00","Veg","Starters"),
({0},"Mushroom Garlic Fry","3.00","Veg","Starters"),
({0},"Chicken Tikka","4.00","Non-Veg","Starters"),
({0},"Tandoori Chicken","4.00","Non-Veg","Starters"),
({0},"Chicken Garlic Fry","4.00","Non-Veg","Starters"),
({0},"Chicken Tikka on Puree","4.00","Non-Veg","Starters"),
({0},"Lamb Tikka","4.00","Non-Veg","Starters"),
({0},"Tandoori King Prawn","6.95","Non-Veg","SeaFood"),
({0},"King Prawn Rosun","5.95","Non-Veg","SeaFood"),
({0},"King Prawn on Puree","5.95","Non-Veg","SeaFood"),
({0},"Prawn Bhuna on Puree","3.95","Non-Veg","SeaFood"),
({0},"Prawn Cocktail","3.95","Non-Veg","SeaFood"),
({0},"Chi/Lam Sashlik Chi","9.95","Non-Veg","Tandoori Specials"),
({0},"Tandoori Deluxe","12.95","Non-Veg","Tandoori Specials"),
({0},"Tandoori Chicken Main","9.95","Non-Veg","Tandoori Specials"),
({0},"Chicken Tikka","7.95","Non-Veg","Tandoori Specials"),
({0},"Lamb Tikka","9.95","Non-Veg","Tandoori Specials"),
({0},"Bombay Aloo ","6.50","Veg","Vegetable Dishes"),
({0},"Mushroom Bhaji ","6.50","Veg","Vegetable Dishes"),
({0},"Saag Dall","6.50","Veg","Vegetable Dishes"),
({0},"Mattor Paneer","6.50","Veg","Vegetable Dishes"),
({0},"Vegetable Roshun","6.50","Veg","Vegetable Dishes"),
({0},"Boiled Rice","2.50","Veg","Side Orders - Rice"),
({0},"Keema Pilau Rice","3.50","Non-Veg","Side Orders - Rice"),
({0},"Mushroom Rice","3.20","Veg","Side Orders - Rice"),
({0},"Garlic Naan","3.00","Veg","Side Orders - Bread"),
({0},"Stuffed Naan","3.50","Veg","Side Orders - Bread"),
({0},"Chapati","1.00","Veg","Side Orders - Bread"),
({0},"Green Salad","2.00","Veg","Side Orders - Sundries"),
({0},"Spice Popadum","0.80","Veg","Side Orders - Sundries"),
({0},"Chutney","0.70","Veg","Side Orders - Sundries"),
({0},"Ras Malai","2.95","Veg","Dessert"),
({0},"Ice Cream","2.95","Veg","Dessert"),
({0},"Gulab Jamun","2.95","Veg","Dessert"),
({0},"Kulfi","2.95","Veg","Dessert"),
({0},"Kheer","2.95","Veg","Dessert");"""
for id in ids:
    try:
        cursor.execute(sql.format(id))
        db.commit()
    except:
        db.rollback()
    
    

