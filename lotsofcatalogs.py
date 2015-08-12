from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem, User

engine = create_engine('sqlite:///catalogmenuwithusers.db')
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

# Create a dummy user and add it to database
User1 = User(
    name="Y.H Zhou",
    email="ziyanrufeng@gmail.com",
    picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
    )
session.add(User1)
session.commit()

catalog1 = Catalog(
    user_id=1,
    name="Soccer",
    description="Soccer is a fun and exciting sport passionately followed "
                "by millions, if not billions of fans around the globe. It "
                "most popular sport, played by tons of people in more than 140 "
                "is the countries. Soccer is a great workout, and it is "
                "entertaining and easy to learn. Competitive soccer is "
                "played at all levels from school to international games."
    )
session.add(catalog1)
session.commit()

soccerItem1 = CatalogItem(
    user_id=1,
    name="Socks",
    description="Soccer socks are typically made out of heavy cotton or "
                "a thick, durable synthetic fabric that reaches the knee. "
                "They should protect your feet from too much friction "
                "with your cleats and cover your shinguards. If you find "
                "they are sliding down your leg too much, many manufacturers "
                "produce stocking ties that fit just below the knee and "
                "are concealed when you fold the sock down.",
    catalog=catalog1
    )
session.add(soccerItem1)
session.commit()

soccerItem2 = CatalogItem(
    user_id=1,
    name="Shinguards",
    description="Shinguards fit on the front of your leg with Velcro "
                "straps and may or may not include a section designed "
                "to support your ankle. Strikers tend to wear smaller, "
                "lighter models, while defenders, midfielders, and "
                "goalkeepers tend to opt for designs that offer more "
                "coverage. Shinguards are also required to play in "
                "many recreational leagues.",
    catalog=catalog1
    )
session.add(soccerItem2)
session.commit()

soccerItem3 = CatalogItem(
    user_id=1,
    name="Gloves",
    description="Goalkeepers are the only players who wear gloves all "
                "the time. Again, there are countless models out "
                "there so it is important to find a design that "
                "offers maximum mobility to your fingers and support "
                "to your wrists. Players in the field sometimes wear "
                "gloves in cold conditions and there are no rules for "
                "these as long as they are light.",
    catalog=catalog1
    )
session.add(soccerItem3)
session.commit()

soccerItem4 = CatalogItem(
    user_id=1,
    name="Soccer Cleats",
    description="Cleats seem to come in dozens of shapes, sizes, "
                "and prices. The most important things are comfort "
                "and a close fit so that they offer full support "
                "through all the sudden starts, stops, and turns of "
                "soccer. It is also critical to make sure that your "
                "studs are suited to the type of surface you are "
                "playing on. Longer metal studs are for softer grass "
                "fields while shorter plastic studs are better for "
                "harder ground. Special shoes with rubber soles are "
                "also made for artificial turf and indoor settings.",
    catalog=catalog1
    )
session.add(soccerItem4)
session.commit()

soccerItem5 = CatalogItem(
    user_id=1,
    name="Soccer Shorts",
    description="There are very few rules for shorts since over "
                "the years players have worn everything from wide "
                "baggy ones to things that resemble small running "
                "shorts. Again, the rule of thumb should be comfort "
                "and freedom of movement. Only basketball-style "
                "shorts that fall below the knee are not recommended.",
    catalog=catalog1
    )
session.add(soccerItem5)
session.commit()

soccerItem6 = CatalogItem(
    user_id=1,
    name="HeadGear",
    description="Headgear is becoming more and more popular in soccer, "
                "particularly among youth players in the United States. "
                "Light and shaped like a headband, it is designed to "
                "soften the impact of heading the ball. It has also "
                "been shown to reduce the likelihood of injury in "
                "the event of two heads clashing.",
    catalog=catalog1
    )
session.add(soccerItem6)
session.commit()

catalog2 = Catalog(
    user_id=1,
    name="Basketball",
    description="Basketball is a game played by two teams, of five "
                "players each, on a rectangular floor.  The purpose "
                "of each team is to throw an inflated spherical ball "
                "into its own basket or goal located at one end of "
                "the playing floor, and to prevent the other team "
                "from scoring at its basket located at the other end."
    )
session.add(catalog2)
session.commit()

basketballItem1 = CatalogItem(
    user_id=1,
    name="basket ball",
    description="The most important thing for training is a ball. "
                "Without a ball, one cannot possibly practice "
                "basketball. There are certain guidelines which "
                "one needs to follow when buying a basketball. "
                "For practicing, one can play with a rubber ball. "
                "For professional competitions, one needs to use "
                "an inflated ball made of leather. Official size "
                "of a basketball is 29.5 to 30 inches in circumference "
                "for men's game and 28.5 inches in circumference "
                "for women's game. It should weigh 18 to 22 ounces. "
                "When bounced off 6 feet from the floor, a well "
                "inflated ball should bounce 49 to 54 inches in height.",
    catalog=catalog2
    )
session.add(basketballItem1)
session.commit()

basketballItem2 = CatalogItem(
    user_id=1,
    name="Hoop",
    description="The hoop or basket is a horizontal metallic rim, "
                "circular in shape. This rim is attached to a net "
                "and helps one score a point. The rim is mounted "
                "about 4 feet inside the baseline and 10 feet "
                "above the court.",
    catalog=catalog2
    )
session.add(basketballItem2)
session.commit()

basketballItem3 = CatalogItem(
    user_id=1,
    name="Basketball Court",
    description="The basketball court is the next important thing "
                "for shooting balls in this game. The court is "
                "usually made of wooden floorboard. The court "
                "size is about 28m x 17m according to the "
                "International standards. The National Basketball "
                "Association (NBA) regulation states the floor "
                "dimension as 29m x 15m. The standard court is "
                "rectangular in shape and has baskets placed on "
                "opposite ends.",
    catalog=catalog2
    )
session.add(basketballItem3)
session.commit()

basketballItem4 = CatalogItem(
    user_id=1,
    name="Backboard",
    description="The backboard is the rectangular board that is "
                "placed behind the rim. It helps give better "
                "rebound to the ball. The backboard is about "
                "1800mm in size horizontally and 1050mm vertically. "
                "Many times, backboards are made of acrylic, "
                "aluminum, steel or glass.",
    catalog=catalog2
    )
session.add(basketballItem4)
session.commit()

catalog3 = Catalog(
    user_id=1,
    name="Baseball",
    description="A game played with a bat and ball by two "
                "opposing teams of nine players, each team playing "
                "alternately in the field and at bat, the players "
                "at bat having to run a course of four bases laid "
                "out in a diamond pattern in order to score."
    )
session.add(catalog3)
session.commit()

baseballItem1 = CatalogItem(
    user_id=1,
    name="Base Ball",
    description="An official baseball is manufactured through a "
                "process of wrapping yarn around a cork or rubber "
                "center and then tightly stitching a cowhide or "
                "horsehide cover over the yarn. A baseball is a "
                "sphere that is approximately 9 inches (23 cm) in "
                "circumference and weighs 5 1/4 ounces (149 g).",
    catalog=catalog3
    )
session.add(baseballItem1)
session.commit()

baseballItem2 = CatalogItem(
    user_id=1,
    name="Bat",
    description="A bat is a solid piece of wood, usually ash, "
                "that is 2.75 inches (7 cm) in diameter at the "
                "thickest part, which is called the barrel, and "
                "not more than 42 inches (107 cm) in length.",
    catalog=catalog3
    )
session.add(baseballItem2)
session.commit()

baseballItem3 = CatalogItem(
    user_id=1,
    name="Batting Helmet",
    description="A helmet protects a baseball player if a ball "
                "accidentally hits him in the head. Some "
                "pitcher's can throw a baseball as fast as "
                "100 miles per hour (161 kph), so a player "
                "needs to wear a helmet to prevent severe "
                "head injuries.",
    catalog=catalog3
    )
session.add(baseballItem3)
session.commit()

baseballItem4 = CatalogItem(
    user_id=1,
    name="Batting Glove",
    description="Although not a required piece of equipment, "
                "many batters wear gloves to protect their "
                "hands while batting. Blisters may be caused "
                "by not wearing batting gloves. Some players "
                "wear these gloves while running bases to "
                "protect their hands while sliding into bases.",
    catalog=catalog3
    )
session.add(baseballItem4)
session.commit()

baseballItem5 = CatalogItem(
    user_id=1,
    name="Catcher's equipment",
    description="A catcher is the target for the pitcher, "
                "so the catcher must wear protective gear "
                "that covers the majority of his body. "
                "Catcher's gear includes a helmet with a "
                "faceguard that is similar to a hockey "
                "goalie's mask, a chest protector, shin "
                "guards, and a special padded glove. Some "
                "catcher's also wear devices called knee "
                "savers, which are triangular pads that "
                "attach to the players calves and rest his "
                "knees even while squatting behind the plate.",
    catalog=catalog3
    )
session.add(baseballItem5)
session.commit()

catalog4 = Catalog(
    user_id=1,
    name="Frisbee",
    description="A game between two teams whose players try to "
                "toss a Frisbee to one another until they cross "
                "the opponents goal; possession changes hands "
                "when the Frisbee is intercepted or touches the "
                "ground or goes out of bounds."
    )
session.add(catalog4)
session.commit()

frisbeeItem1 = CatalogItem(
    user_id=1,
    name="Frisbee",
    description="There are many different types of frisbee molds "
                "that companies sell. The two biggest ones, in my "
                "opinion, are Wham-o and Discraft. The main "
                "difference between these molds are the feel "
                "and the stiffness of the plastic.",
    catalog=catalog4
    )
session.add(frisbeeItem1)
session.commit()

frisbeeItem2 = CatalogItem(
    user_id=1,
    name="Frisbee Gloves",
    description="Gloves perform two important functions, "
                "especially during intense games: 1) They "
                "protect your hands and fingers from fast-moving "
                "discs; and 2) They can actually help grip "
                "the disc better!",
    catalog=catalog4
    )
session.add(frisbeeItem2)
session.commit()

catalog5 = Catalog(
    user_id=1,
    name="Snowboarding",
    description="Snowboarding is a winter sport that involves "
                "descending a slope that is covered with snow "
                "while standing on a board attached to a riders "
                "feet, using a special boot set onto a "
                "mounted binding."
    )
session.add(catalog5)
session.commit()

snowItem1 = CatalogItem(
    user_id=1,
    name="Goggles",
    description="Goggles have all kinds of functions like anti "
                "fogging, uv protection, venting, etc. While "
                "all these features are great and probably "
                "worth the money, the most important option "
                "is the tint. Yellow or amber lenses filter "
                "out blue light and add contrast. Since most "
                "snow and ice has bluish tints these help you "
                "make out shapes like bumps and dips. Rose "
                "lenses help you see detail on overcast days. "
                "Clear lenses are for when there is little "
                "light. like night riding or really grey days "
                "where you can still see the terrain.",
    catalog=catalog5
    )
session.add(snowItem1)
session.commit()

snowItem2 = CatalogItem(
    user_id=1,
    name="Snowboard",
    description="There are Three Different Types of Snowboards "
                "available on the market today: Freestyle, "
                "Freeride (All Mountain), and Alpine (Carving) "
                "Boards. Each board has a unique construction "
                "technique and materials, shape, flex pattern, "
                "and size. The type of Snowboard you ride "
                "should correspond to your particular style "
                "of riding.",
    catalog=catalog5
    )
session.add(snowItem2)
session.commit()

snowItem3 = CatalogItem(
    user_id=1,
    name="Snowboard Boots",
    description="Snowboard boots are mostly considered soft "
                "boots, though alpine snowboarding uses a "
                "harder boot similar to a ski boot. A boot's "
                "primary function is to transfer the rider's "
                "energy into the board, protect the rider with "
                "support, and keep the rider's feet warm. A "
                "snowboarder shopping for boots is usually "
                "looking for a good fit, flex, and looks. "
                "Boots can have different features such as "
                "lacing styles, heat molding liners, and gel "
                "padding that the snowboarder also might be "
                "looking for. Tradeoffs include rigidity versus "
                "comfort, and built in forward lean, versus comfort.",
    catalog=catalog5
    )
session.add(snowItem3)
session.commit()

snowItem4 = CatalogItem(
    user_id=1,
    name="Bindings",
    description="Bindings are separate components from the "
                "snowboard deck and are very important parts "
                "of the total snowboard interface. The bindings' "
                "main function is to hold the rider's boot in "
                "place tightly to transfer their energy to the "
                "board. Most bindings are attached to the board "
                "with three or four screws that are placed in "
                "the center of the binding. Although a rather "
                "new technology from Burton called Infinite "
                "channel system[12] uses two screws, both on "
                "the outsides of the binding.",
    catalog=catalog5
    )
session.add(snowItem4)

catalog6 = Catalog(
    user_id=1,
    name="Rock Climbing",
    description="Rock climbing is an activity in which "
                "participants climb up, down or across natural "
                "rock formations or artificial rock walls. "
                "The goal is to reach the summit of a formation "
                "or the endpoint of a usually pre-defined "
                "route without falling."
    )
session.add(catalog6)
session.commit()

rockClimbItem1 = CatalogItem(
    user_id=1,
    name="Climbing Shoes",
    description="The most useful piece of climbing equipment is "
                "a pair of climbing shoes. Improvements in shoe "
                "design alone have allowed climbers to climb "
                "many things previously unclimbable. The modern "
                "climbing shoe has a stiff, smooth rubber sole "
                "that protects the foot from sharp, rough rock, "
                "and provides more friction than a bare foot. A "
                "pair costs between $100 and $150. Climbing shoes "
                "fit tightly to prevent the foot from sliding "
                "around within. This makes them uncomfortable, "
                "but the improved friction and control they "
                "afford far outweigh the discomfort.",
    catalog=catalog6
    )
session.add(rockClimbItem1)
session.commit()

rockClimbItem2 = CatalogItem(
    user_id=1,
    name="Rope",
    description="A modern climbing rope, a key piece of safety "
                "equipment, is of kernmantle construction, "
                "consisting of continuous braided nylon fibers, "
                "the kern, surrounded by a continuous braided "
                "nylon outer sheath, the mantle. Such construction "
                "is superior to the more traditional laid rope "
                "(three large strands twisted together) because "
                "the outer sheath protects the inner core, where "
                "most of the strength lies, from the elements. "
                "Climbing rope is dynamic: able to stretch a bit "
                "under tension. This is because the rope must stop "
                "falling climbers. If the rope did not stretch, a "
                "falling climber would be jerked suddenly as the "
                "rope stops him. Instead, the rope slows his fall "
                "more gently.",
    catalog=catalog6
    )
session.add(rockClimbItem2)
session.commit()

rockClimbItem3 = CatalogItem(
    user_id=1,
    name="Carabiners",
    description="Carabiners, used constantly in climbing, are rings "
                "of solid aluminum with a spring-loaded gate that "
                "allows them to be opened. Normally, the spring "
                "holds the gate closed, but the gate can be opened "
                "to admit a rope. Carabiners are inexpensive "
                "(between $5 and $20), strong (most are rated "
                "to hold at least 20 kN, about 2.2 tons), and "
                "versatile. Virtually every climbing technique "
                "uses carabiners.",
    catalog=catalog6
    )
session.add(rockClimbItem3)
session.commit()

catalog7 = Catalog(
    user_id=1,
    name="Football",
    description="A game played by two teams of 11 players each "
                "on a rectangular, 100-yard-long field with goal "
                "lines and goalposts at either end, the object "
                "being to gain possession of a ball and advance "
                "it in running or passing plays across the "
                "opponent's goal line or kick it through the "
                "air between the opponent's goalposts."
    )
session.add(catalog7)
session.commit()

footballItem1 = CatalogItem(
    user_id=1,
    name="Football Helmet",
    description="One of the most important pieces of equipment "
                "is the helmet. The helmet is composed of a "
                "facemask and the helmet itself. With growing "
                "awareness of concussions associated with "
                "football, wearing a helmet properly is extremely "
                "important. According to USA Football, the helmet "
                "will be placed so the front edge will rest 1 inch "
                "above your eyebrows and will fastened to your "
                "head via the chinstrap.",
    catalog=catalog7
    )
session.add(footballItem1)
session.commit()

footballItem2 = CatalogItem(
    user_id=1,
    name="Shoulder Pads",
    description="Shoulder pads must be worn when playing football. "
                "They absorb shock when being hit, and allow you "
                "to tackle with reduced risk of injury. Shoulder "
                "pads come in various sizes, depending on the "
                "position you play. Quarterbacks tend to have "
                "smaller and lighter shoulder pads so that their "
                "natural throwing motion is not affected, while "
                "players such as linebackers and defensive ends "
                "have larger shoulder pads to protect their "
                "bodies from constant impact.",
    catalog=catalog7
    )
session.add(footballItem2)
session.commit()

footballItem3 = CatalogItem(
    user_id=1,
    name="Waist And Leg Pads",
    description="Your lower body needs protection too. From "
                "youth- to college-level football, you are "
                "required to wear leg and hip pads, which "
                "include hip, tailbone, knee and thigh pads. "
                "These are inserted in the football pants "
                "themselves or a sports girdle worn under "
                "the football pants. The hip and tailbone "
                "pads may also be tied around the waist with "
                "a sports belt. In addition, although it is "
                "not always required, male players should always "
                "wear a cup to protect the sensitive groin "
                "area from impact during the play.",
    catalog=catalog7
    )
session.add(footballItem3)
session.commit()

catalog8 = Catalog(
    user_id=1,
    name="Skating",
    description="The recreation and sport of gliding across an "
                "ice surface on blades fixed to the bottoms of "
                "shoes (skates). The activity of ice skating "
                "has given rise to two distinctive sports: "
                "figure skating and short-track speed skating, "
                "both of which are forms of racing on ice skates."
    )
session.add(catalog8)
session.commit()

skatingItem1 = CatalogItem(
    user_id=1,
    name="Skating Boots",
    description="Ice skating boots are constructed from stiff "
                "leather to provide support to the ankle and "
                "foot. The most important thing to consider "
                "when buying ice skating boots is the fit. "
                "The boot should be snug and your foot should "
                "not be able to move around much. The boots "
                "will become more comfortable once they are "
                "broken in, but if a boot pinches or causes "
                "numbness, it is not the right size. Many boots "
                "sold in sports equipment outlets come with "
                "the blades already attached, which is fine "
                "for a beginner or recreational skater. But "
                "competitive skaters should buy their boots "
                "and then have the blades fitted and attached.",
    catalog=catalog8
    )
session.add(skatingItem1)
session.commit()

skatingItem2 = CatalogItem(
    user_id=1,
    name="Blades",
    description="Ice skating blades are not completely flat "
                "from one tip to the other; instead, they "
                "have a small curve referred to as the rocker. "
                "The width of the blade is not completely "
                "flat either---it is concave, which creates "
                "two sharp edges. In turn, there are four "
                "points on the blade that can be used in "
                "executing various moves, spins and jumps. "
                "The front of the blade is serrated and "
                "referred to as the toe pick. The length of "
                "the blade and the size of the toe pick will "
                "vary depending on specialized style and skill "
                "level. It is important to regularly sharpen "
                "your skate blades and to protect them when "
                "you're not on the ice.",
    catalog=catalog8
    )
session.add(skatingItem2)
session.commit()

catalog9 = Catalog(
    user_id=1,
    name="Hockey",
    description="A game played on a field by two opposing teams "
                "of 11 players each, who try to hit a ball into "
                "their opponents' goal using long sticks curved "
                "at the end."
    )
session.add(catalog9)
session.commit()

hockeyItem1 = CatalogItem(
    user_id=1,
    name="Stick",
    description="The hockey stick is the most important piece of "
                "equipment for a player. The top of the stick is "
                "known as the 'butt', which leads down into the "
                "shaft (the long stem of the stick). Shafts are "
                "typically made of carbon graphite, aluminum, or "
                "wood. The curvature at the bottom of the shaft is "
                "known as the blade. Sticks need to be fitted for "
                "players. Remember the 'rule of chin': While wearing "
                "skates and placing the stick on the end of its "
                "blade, the butt of the stick should lie 3 inches "
                "under your chin (see photo). Sticks are made for "
                "either left- or right-handed players, depending "
                "on the curve of the blade. Restrictions regarding "
                "the size of your hockey stick vary depending upon "
                "the level of competition.",
    catalog=catalog9
    )
session.add(hockeyItem1)
session.commit()

hockeyItem2 = CatalogItem(
    user_id=1,
    name="Hockey Skates",
    description="Skates are composed of three parts: a boot, a "
                "blade holder, and a steel blade. The boot is "
                "made of leather, nylon, or molded plastic. The "
                "surface of the steel blade is not flat, but "
                "curved inward. The sharpening process carves "
                "out the center of the blade, leaving two sharp "
                "surfaces. Keeping your skates sharp helps "
                "maneuverability and prevents you from catching "
                "your blade on the ice, which can lead to leg and "
                "knee injuries. Brand-name skates are your best "
                "bet. Make sure the skate has a well-constructed "
                "heel and ankle support. Wear only one pair of "
                "socks; bulky socks can hinder the snug fit of "
                "a boot.",
    catalog=catalog9
    )
session.add(hockeyItem2)
session.commit()

hockeyItem3 = CatalogItem(
    user_id=1,
    name="Hockey Jersey",
    description="Covers the shoulder and elbow pads. Jerseys "
                "are color-coded and numbered for team and "
                "player identification, and teams, especially "
                "at upper skill levels, may have multiple "
                "jersey styles for home and away games. "
                "Traditional hockey jerseys are oversized, "
                "roughly square, and made using fabrics with "
                "limited elasticity. A 'fight strap' is required "
                "to be used in most professional leagues; this "
                "connects the jersey to the inside of the pants "
                "and prevents an opponent in a fight pulling the "
                "player's jersey over their head. Newer jerseys "
                "are more form-fitting due to the use of elastic "
                "fabrics, and resemble NFL jerseys in their overall fit.",
    catalog=catalog9
    )
session.add(hockeyItem3)
session.commit()

print "added catalog items!"
