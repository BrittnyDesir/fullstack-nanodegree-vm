from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_db_setup import Base, OutdoorActivity, Items, User

engine = create_engine('sqlite:///catalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(email="bberry.336@gmail.com")
session.add(User1)
session.commit()

# Items for Camping
activity1 = OutdoorActivity(user_id=1, name="Camping")

session.add(activity1)
session.commit()

item1 = Items(user_id=1, name="Day Pack", description="Backpack suitable for a day hike. Plenty of pockets with an adjustable hip belt. Made with a lightweight waterproof material.", price="$50.00", activity=activity1)

session.add(item1)
session.commit()

item2 = Items(user_id=1, name="Camp Stove", description="Camping stove with fuel included", price="$35.00", activity=activity1)

session.add(item2)
session.commit()

item3 = Items(user_id=1, name="Sleeping Bag", description="One person 800 fill synthetic down sleeping bag. Can be used down to 20 degrees", price="$180.00", activity=activity1)

session.add(item3)
session.commit()

item4 = Items(user_id=1, name="Tent", description="3-season two person tent. Lightweight, poles and roof cover included.", price="$220.00", activity=activity1)

session.add(item4)
session.commit()

item5 = Items(user_id=1, name="Water Bottle", description="24oz. BPA free plastic water bottle. Keeps cold drinks cold and hot drinks hot for up to 12 hours.", price="$25.00", activity=activity1)

session.add(item5)
session.commit()

# Items for Climbing
activity2 = OutdoorActivity(user_id=1, name="Climbing")

session.add(activity2)
session.commit()

item1 = Items(user_id=1, name="Harness", description="Women\'s harness comes in sizes XS-XL.", price="$150.00", activity=activity2)

session.add(item1)
session.commit()

item2 = Items(user_id=1, name="Chalk", description="Climber\'s chalk. Keeps your hands dry for a better grip", price="$10.00", activity=activity2)

session.add(item2)
session.commit()

item3 = Items(user_id=1, name="Rope", description="Durable rope in multiple colors. For indoor climbing only.", price="$200.00", activity=activity2)

session.add(item3)
session.commit()

item4 = Items(user_id=1, name="Belay Device", description="Device used for belaying. Easy to use and comes with easy to read instructions", price="$99.00", activity=activity2)

session.add(item4)
session.commit()

item5 = Items(user_id=1, name="Climbing Shoes", description="Women\'s climbing shoes. Great for bouldering and beginners.", price="$65.00", activity=activity2)

session.add(item5)
session.commit()

# Items for Cycling
activity3 = OutdoorActivity(user_id=1, name="Cycling")

session.add(activity3)
session.commit()

item1 = Items(user_id=1, name="Mountain Bike", description="Bike with larger tires and deeper tread for muddy trails. Can customize handle bars, frame and wheels.", price="$800.00", activity=activity3)

session.add(item1)
session.commit()

item2 = Items(user_id=1, name="Road Bike", description="A lighter carbon frame bike with skinnier tires for flat roadways. Excellent for commuters.", price="$750.00", activity=activity3)

session.add(item2)
session.commit()

item3 = Items(user_id=1, name="Lights", description="Front and rear lights. Can be used on a mountain or road bike. Comes with 3 different light settings. Batteries not included.", price="$30.00", activity=activity3)

session.add(item3)
session.commit()

item4 = Items(user_id=1, name="Bike Tool", description="16 piece multi-tool for fixing a bike in a pinch. Carrying case included.", price="$25.00", activity=activity3)

session.add(item4)
session.commit()

item5 = Items(user_id=1, name="Portable Pump", description="Portable hand-held bike pump. Great for multi-day trips", price="$15.00", activity=activity3)

session.add(item5)
session.commit()

# Items for Paddling
activity4 = OutdoorActivity(user_id=1, name="Paddling")

session.add(activity4)
session.commit()

item1 = Items(user_id=1, name="Kayak", description="One person kayak suitable for lakes and rivers. Paddle not included.", price="$500.00", activity=activity4)

session.add(item1)
session.commit()

item2 = Items(user_id=1, name="Life Vest", description="Adult life vest, one size fits all. Suitable for any water activity.", price="$40.00", activity=activity4)

session.add(item2)
session.commit()

item3 = Items(user_id=1, name="Paddle", description="Adult size adjustable paddle for kayaking only.", price="$60.00", activity=activity4)

session.add(item3)
session.commit()

item4 = Items(user_id=1, name="Paddle Board", description="Adult size paddle board. Suitable for lakes or calm ocean water. Paddle not included.", price="$750.00", activity=activity4)

session.add(item4)
session.commit()

item5 = Items(user_id=1, name="Car Rack", description="Car rack for economy size cars. Can be used to carry a kayak or paddle board. Straps and blocks included.", price="$75.00", activity=activity4)

session.add(item5)
session.commit()

# Items for Running
activity5 = OutdoorActivity(user_id=1, name="Running")

session.add(activity5)
session.commit()

item1 = Items(user_id=1, name="Shoes", description="Women\'s running shoes. Meant for long distances on roadways.", price="$120.00", activity=activity5)

session.add(item1)
session.commit()

item2 = Items(user_id=1, name="Hydration Pack", description="Lightweight hydration pack for long runs. Includes pockets for small items.", price="$40.00", activity=activity5)

session.add(item2)
session.commit()

item3 = Items(user_id=1, name="GPS Watch", description="Women\'s black GPS watch. Records distance, pace and time. Heart rate monitor not included.", price="$300.00", activity=activity5)

session.add(item3)
session.commit()

item4 = Items(user_id=1, name="Compression Socks", description="Women\'s compression socks can be worn during or after a hard run to decrease recovery time.", price="$30.00", activity=activity5)

session.add(item4)
session.commit()

item5 = Items(user_id=1, name="Foam Roller", description="Used for muscle recovery when stretching isn\'t enough.", price="$25.00", activity=activity5)

session.add(item5)
session.commit()

# I tems for Winter Sports
activity6 = OutdoorActivity(user_id=1, name="Winter Sports")

session.add(activity6)
session.commit()

item1 = Items(user_id=1, name="Snow Shoes", description="Women\'s snow shoes one size fits all. Perfect for hiking in the winter.", price="$150.00", activity=activity6)

session.add(item1)
session.commit()

item2 = Items(user_id=1, name="Winter Boots", description="Women\'s winter hiking boots. Waterproof with warm inner lining.", price="$180.00", activity=activity6)

session.add(item2)
session.commit()

item3 = Items(user_id=1, name="Winter Coat", description="800 fill goose down winter coat.", price="$300.00", activity=activity6)

session.add(item3)
session.commit()

item4 = Items(user_id=1, name="Winter Hat", description="Keeps your head and ears warm on cold days. Multiple colors available.",price="$10.00", activity=activity6)

session.add(item4)
session.commit()

item5 = Items(user_id=1, name="Winter Gloves", description="Thick gloves with fleece lining.", price="$25.00", activity=activity6)

session.add(item5)
session.commit()

print "Added items to database!"
