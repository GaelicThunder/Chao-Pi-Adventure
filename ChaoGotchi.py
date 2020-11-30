import time
import os.path
from demo_opts import get_device
from PIL import Image, ImageDraw
from PIL import ImageFont
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import random
from timeloop import Timeloop
from datetime import timedelta
from luma.core.virtual import terminal
from luma.core.render import canvas
import luma.core.render
import logging
import sys
import pickle


button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP
 
button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP
 
button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP
 
button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP
 
button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP

button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

Name="Violation"

random.seed() 

tl = Timeloop()
NameList=["Hydro","Raevix","Melon","Apple-B","Lunar","Lunesc","Mintum","Adamant","Tweef","Twigs","Razz","Alshi","Zod","Eradic","Google","Yumyum","Galaxus","Galax","Solar","Pickle","Foamy","Tickles","Alfalfa","Boc","Napoli","Sunni","Lemon","Medrac","Alndar","Lemartz","Zidao","Vivi","Kefka","Geo","Aero","Pyro","Chiraz","Juice","Element","Allo","Alto","Soprano","Tenor","Bass","Base","Trombo","Trumpy","Sax","Clari","Fluti","Barito","Tuba","Drumum","Cresc","Piano","Bugle","Chuck","Navi","Gator","Jethro","Rappy","Tippy","Nippy","Sippy","Katamar","IChao","Nomnom","Hiro","Neutro","Dhark","Poker","Blakjak","BoBo","Whiny","Sniffy","Squirmy","John","Paul","Ringo","George","Vamp","Chaolin","Chaosko","Chaozy","Chaochi","Chow","Eatum","Pen","Gwen","May","Spring","Summer","Autumn","Winter","Ima","Winner","Wacko","Jacko","Dot","Flick","Olimar","Pikmao","Bio","Aqua","Terra","Pie","Richter","Benvoli","Mercuti","Romeo","Tybalt","Chapu","Chappa","Choppa","Ace","Salt","Pepper","Lock","Shock","Barrel","Nobeard","Ice","Egzist","Namin","Admin","Kahn","Veggie","Chat","Chap","Tart","Nickel","Soup","Peasoup","Meat","Spuggy","Saucy","Bigfoot","Bunni","NIGHTS","Reala","NoCTuRNe","Mozilla","Firefox","Shade","Haze","Angel","Grip","Dash","Phrozen","Krimzon","Demon","Blitz","Melissa","Buzzy","Melody","BriBri","Zippy","ChaChao","Abbey","Emmy","Cheng","Pebbles","Bingo","Dingo","Shmooples","Muffins","Chaos 0.5","Curly","Mr. Grizzle","Sparkles","Cole","The Maw","Phoenix","Deathly","Shadow","Chaky","Happy","Dark","Jester","Blinky","Rocky","Pinky","Roxy","Troopy","Vader","Kirby","Vult","Sony","Muffy","Snipe","Speedy","Bubbles","Fafu","Chaoly","Bucket","Brandin","Zaphod","Snoozy","Pillow","Boxy","Boxer","Bounty","Hunty","Hunter","Gunther","Killer","Angel","Fluffer","Mr. Foo","Cappy","Bottin","Silver","ChsAngl","ChsDvl","Chacron","Snowflk","Aeolus","Zues","Dew","Sain","Zai","Spark","Tethys","Zonic","Sonic","Ares","Nike","Ayrus","Zoragon","Rutie","Zora","Goron","Cookie","Muffin","Waffle","Pancake","Sugar","Berry","Candy","Popcorn","Cake","Cupcake","House","Rice","Sky","Jamie","Lione","Rein","Kitty","Milky","Boom","Sticky","Name","Chaos","Lune","Gold","Emerald","Ruby","Midnight","Flash","Greem Foot","Csillag","Alkali","Slinky","SA2B","Maya","Ethine","Seldash","Rord","Breeze","Fuoco","Aquila","Spada","Corallo","Almed","Manzo","Nuvola","Diavolo","Baci","Illica","Sunny","Chumm","Alvil","Tuna","Sleepy","Crimson","Stiz","Blue","Cyber","Atom","Charon","Rouel","Ultra","Storm","Super","Lordice","Stormy","Darcy","Jane","Glitchy","Shen","Bleu","Violet","Nero","Shelk","Scarlet","Aurora","Nova","Arrow","Lotus","Vibrant","Tamara","Eclipse","Azura","Votrexia","Voltex","BB&Chao","SA2/B","aMAZing","Johnson","Johnny","Lamar","Shoney","Bearber","Penguin","Supalol","Jakki","Pie","Darkly","Sonix Super","Ami","Night","Misty","Anaklusmos","Riptide","Skully","Sonikuu","Violeta","CUTE ^_^","Lilly","Banana","Mint","Money","Monolie","Chaoz","Blue$","Camz","Chaz","Kron","Kobe","Cole","Da$h","Hayde$","Po$iden","Jak","Jack$","Mori","Shady","Shadey","Zigzag","Luna","Coal","Iris","Nora","Crystal","Red","JoJo","Ninja","Sensei","Jello","Dyno","Dino","Titian","Flipper","Naomi","Echo","Melony","Tazz","Jess","Leah","Donte","Link","Don Arr","Hera","Rouge","Princess","Artemis","Maleike","Hades","Dede","Mimi","Sammy","Pinda","Marcus","Star","M&M","Edge","Reid","Jarrod","Reese","Lint","Chad","Meow","Chaosky","Skye","Skyler","Tiko","Rolly","Ray","Leed","Zuka","Pucky","Sprat","Fluff","Tiny","Twilight","Clover","Wind","Chapon","Presto","Lo Mein","Lolli","Monsoon","Blu-blu","Nopahc","Fui","Golorok","REX","Grape","Chaolina","Chaoplis","Chaoro","Steak","Apple","Galaxy","Max","Shiny","Mr.Shiny","Twinkle","Swimmey","Swimmy","Mermaid","Fishy","Blooper","Gollum","Titan","Punchy","Jak","Hotshoot","Ridley","Chance","Mystic","Benny","Smile","Devil","Knuckles","Pippy","Fudge","Cream","Tilly","Cheese","Denim","Rox","Kayla","Shin","Jada","Jade","Amaya","Sam","Sakura","Saskue","Iruka","Tobi","Sodapop","Charlie","Pipy","Jet","Moonlight","Skylar","Chil","Sora","Leon","Cloud","Axel","Roxas","Hayner","Pence","Rai","Seifer","Mush","Demyx","Bob","Chewbucka","Stitch","Wesly","Elliet","Colt","Copperhead","Copper","Kazune","Jin","Michi","Kyo","Yuki","Shigure","Hatori","Akito","Momiji","Hatsuharu","Kairi","Fuu","Olette","Amber","Baby","Flora","Megs","Zoey","Kiky","Rika","Karin","Kick","Leila","Risa","Kagura","Hanajima","Arisa","Bluma","Lucky","Winky","Poky","Pokey","Riku","Tohru","Spirit","Ripley","Clubber","Gema","Kiwi","Margarine","Boba","Sapphire","Topez","Amethist","Bandit","Mischief","Bear","Bubby","Shortie","Russel","Wiggle","Mimzy","Aerith","Dove","Jemiah","Gloria","Summer","Ellen","Ina","Ibuki","Ribbon","Smiley","Smiles","Miley","Sumon Butt","Rosey","Rose","Boo","Snow","Ayaka","Hikari","Junko","Kaori","Kazumi","Kimiko","Michiko","Natsumi","Sayuri","Yumi","Chi","Chikako","Chiyo","Dai","Sumiko","Arashi","Daichi","Mephiles","Diablo","Goldy","Buddy","Mr. Uie","Carrot","Chowder","Big","Ben","Flop","Fling","Streak","Slider","Evil","Claws","G","Candy","Hezues","Twigs","Crunchy","Slimy","Lawlz","Lolz","Yosho","Lady","T-Bone","Chaokumo","Chaozuki","Chaoming","Heather","Gangsta","Gangster","Peanut","Donuts","Jelly","Shocker","Phsyco","Mirage","Chocho","Mashed Potatoes (MP)","Lays","Dorito","Eli","Juicy","Spike","Cosmo","Spikey","Flappin","Joe","Beefy","Stuffed","Eggo","Grapes","Berries","Tingle","Jerry","Tom","Pocket","Pizza","Blaze","Ember","Scorch","Scorcher","Scourge","Scorcher","Scourge","Sonia","Mercury","Tails","Shark","Rain","Tyranno","Terminos","Pelican","Vulcan","Thunder","Lightning"]

ChaoList=["Normal.jpg","Chaos.jpg","Run.jpg","Fly.jpg","Power.jpg","Swim.jpg","Devil.jpg","DevilChaos.jpg","DevilRun.jpg","DevilFly.jpg","DevilPower.jpg","DevilSwim.jpg","Hero.jpg","HeroChaos.jpg","HeroRun.jpg","HeroFly.jpg","HeroPower.jpg","HeroSwim.jpg"]
#riga 0
walk=[1,0,1,2]
sit=[3,4,5,4]
confused=[6,7,6,7]
#riga 1
drawing=[6,7,6,7]
punchcharge=[0,1,2,3]
#riga 2
punch=[0,1,0,1]
ballkick=[4,5,2,3] #Start a riga 6 #YAni=[6,6,2,2]
fall=[4,5,6,7]
#riga 3
cry=[0,1,2,1]
crycicle=[2,1,2,1]
thinking=[3,4,3,4]
sleep=[5,6,5,6]
#cantswim1=[7]  continua riga 4
#riga 4
cantswim=[7,0,7,0] #YAni=[3,4,3,4]
swimming=[2,3,4,3]
punchmiss=[5,6,7,7]
#riga 5
eat=[0,1,2,3]
eat2=[2,3,2,3]
fly=[5,6,7,6]
#riga 6
smh=[0,1,0,1]
lateralwait=[4,4,6,6]
#jump=[7] continua riga 7
#riga 7
jump=[7,0,1,0] #YAni=[6,7,7,7]
hellothere=[2,3,2,3]

YAni=[0,0,0,0]

MaxFrame=4
w = 25
h = 25
### Small Back     
bw = 13
bh = 26
###
frame = 0
frameblx= 0
framebsx= 1
Ani=walk
Chao="Normal.jpg"#random.choice(ChaoList)
Back='18.jpg'

Hero=0
Dark=0
menu=False
inventory=False
shop=False
games=False
stat=False
race=False
racing=False
racegui=False
BackMove=True
Counter=0
Age=0
Fly=random.randint(0,5)
Run=random.randint(0,5)
Swim=random.randint(0,5)
Power=random.randint(0,5)
Stamina=random.randint(0,5)
Int=random.randint(0,1)
Luck=random.randint(0,1)
VelocityDec=random.randint(15,25)
Mood=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
Choice=["Walk","Walk","Walk","Walk","Walk","Walk","Swim","Fly","Sleep","Sad","Tired","Think","Hello","Draw"]
ObjList=["Run Fruit","Fly Fruit","Swim Fruit","Power Fruit","Stamina Fruit","Hero Fruit","Chao Fruit","Dark Fruit"]
Inv=[]
Text=' '
Evolve=False
Dec=""
meters=0
OnOff='On'
Happiness=100
InvList=[]
Money=0
Stamina=100
StatList=[str(''),int(0),int(0),int(0),int(0),int(0),int(0)]
ListRacer=[[Chao,Fly,Run,Swim,Power,Int,Luck,""]]
ChaoPoint=Fly+Run+Swim+Power+Int+Luck
CurrentChao=0
racelevel=0
RunMedal=1
FlyMedal=1
SwimMedal=1
PowerMedal=1
RaceLenght=0
RaceType='Run'
Positions=[]
Selection=''
Trip=False
boost=False
i=0
background=''

def Load():
    global Name
    global Chao
    global i
    global Inv
    global Fly
    global Run
    global Swim
    global Power
    global Int
    global Luck
    global meters
    global Age
    global Evolve
    global Dec
    global Ani
    global YAni
    global Mood
    global Stamina
    global RunMedal
    global FlyMedal
    global SwimMedal
    global PowerMedal
    global BackMove
    global Dark
    global Hero
    
    
    if os.path.getsize("/home/pi/Chao.save") == 0:
        logging.info("Save Corrupted, restoring backup")
        if os.path.isfile("/home/pi/Chao.bak"):
            if os.path.getsize("/home/pi/Chao.bak") != 0:
                logging.info("Backup found, proceding with restore")
                os.remove("/home/pi/Chao.save")
                os.rename("/home/pi/Chao.bak","/home/pi/Chao.save")
            else:
                logging.info("Backup also corrupted, goodbye friend...")
                while (j<30):
                    Mood[j]=random.choice(Choice)
                    logging.info(Mood[j])
                    j+=1
                i=random.choice([0,1,2])
                return
        else:
            logging.info("Backup not found, proceding with restore")
        
    logging.info("Loading")
    with open("/home/pi/Chao.save", 'rb') as f:
        Name=pickle.load(f)
        Chao=pickle.load(f)
        i=pickle.load(f)
        Inv=pickle.load(f)
        Fly=pickle.load(f)
        Run=pickle.load(f)
        Swim=pickle.load(f)
        Power=pickle.load(f)
        Int=pickle.load(f)
        Luck=pickle.load(f)
        meters=pickle.load(f)
        Age=pickle.load(f)
        Evolve=pickle.load(f)
        Dec=pickle.load(f)
        Ani=pickle.load(f)
        YAni=pickle.load(f)
        Mood=pickle.load(f)
        Stamina=pickle.load(f)
        RunMedal=pickle.load(f)
        FlyMedal=pickle.load(f)
        SwimMedal=pickle.load(f)
        PowerMedal=pickle.load(f)
        BackMove=pickle.load(f)
        Hero=pickle.load(f)
        Dark=pickle.load(f)
    f.close()

@tl.job(interval=timedelta(seconds=300))
def Save():
    global Name
    global Chao
    global i
    global Inv
    global Fly
    global Run
    global Swim
    global Power
    global Int
    global Luck
    global meters
    global Age
    global Evolve
    global Dec
    global Ani
    global YAni
    global Mood
    global Stamina
    global RunMedal
    global FlyMedal
    global SwimMedal
    global PowerMedal
    global BackMove
    global Dark
    global Hero
    global background
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'SpritesJpeg', 'save.jpg'))
    spritemap = Image.open(img_path).convert("1")
    background.paste(spritemap, (110, 49))
    device.display(background.convert(device.mode))
    logging.info("Saving... ")
    
    
    
    
    logging.info(Name)
    logging.info(Chao)
    logging.info(i)
    logging.info(Inv)
    logging.info(Fly)
    logging.info(Run)
    logging.info(Swim)
    logging.info(Power)
    logging.info(Int)
    logging.info(Luck)
    logging.info(meters)
    logging.info(Age)
    logging.info(Evolve)
    logging.info(Dec)
    logging.info(Ani)
    logging.info(YAni)
    logging.info(Mood)
    logging.info(Stamina)
    logging.info(RunMedal)
    logging.info(FlyMedal)
    logging.info(SwimMedal)
    logging.info(PowerMedal)
    logging.info(BackMove)
    logging.info(Dark)
    logging.info(Hero)
    
    
    if os.path.isfile("/home/pi/Chao.save"):
        os.rename("/home/pi/Chao.save","/home/pi/Chao.bak")
    with open("/home/pi/Chao.save", 'wb') as f:
        pickle.dump(Name,f)
        pickle.dump(Chao,f)
        pickle.dump(i,f)
        pickle.dump(Inv,f)
        pickle.dump(Fly,f)
        pickle.dump(Run,f)
        pickle.dump(Swim,f)
        pickle.dump(Power,f)
        pickle.dump(Int,f)
        pickle.dump(Luck,f)
        pickle.dump(meters,f)
        pickle.dump(round(Age,1),f)
        pickle.dump(Evolve,f)
        pickle.dump(Dec,f)
        pickle.dump(Ani,f)
        pickle.dump(YAni,f)
        pickle.dump(Mood,f)
        pickle.dump(Stamina,f)
        pickle.dump(RunMedal,f)
        pickle.dump(FlyMedal,f)
        pickle.dump(SwimMedal,f)
        pickle.dump(PowerMedal,f)
        pickle.dump(BackMove,f)
        pickle.dump(Hero,f)
        pickle.dump(Dark,f)
    f.close()
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
    'SpritesJpeg', 'save.jpg'))
    spritemap = Image.open(img_path).convert("1")
    background.paste(spritemap, (110, 49))
    device.display(background.convert(device.mode))

def Evolution():
    global Fly
    global Run
    global Swim
    global Power
    global Dark
    global Hero
    global Chao
    
    logging.info("EVO START")
    logging.info("Fly "+str(Fly))
    logging.info("Run "+str(Run))
    logging.info("Swim "+str(Swim))
    logging.info("Power "+str(Power))
    
    if Fly>=Run and Fly>=Swim and Fly>=Power:
        if Hero>Dark and Hero>50:
            Chao="HeroFly.jpg"
            
        if Dark>Hero and Dark>50:
            Chao="DevilFly.jpg"
            
        if Dark==Hero or (Dark<50 and Hero<50):
            Chao="Fly.jpg"
        
        logging.info("EVO FLY")
    
    elif Run>=Fly and Run>=Swim and Run>=Power:
        if Hero>Dark and Hero>50:
            Chao="HeroRun.jpg"
            
        if Dark>Hero and Dark>50:
            Chao="DevilRun.jpg"
            
        if Dark==Hero or (Dark<50 and Hero<50):
            Chao="Run.jpg"
            
        logging.info("EVO RUN")
            
    elif Swim>=Run and Swim>=Fly and Fly>=Power:
        if Hero>Dark and Hero>50:
            Chao="HeroSwim.jpg"
            
        if Dark>Hero and Dark>50:
            Chao="DevilSwim.jpg"
            
        if Dark==Hero or (Dark<50 and Hero<50):
            Chao="Swim.jpg"
            
        logging.info("EVO SWIM")
        
    elif Power>=Run and Power>=Swim and Power>=Fly:
        if Hero>Dark and Hero>50:
            Chao="HeroPower.jpg"
            
        if Dark>Hero and Dark>50:
            Chao="DevilPower.jpg"
            
        if Dark==Hero or (Dark<50 and Hero<50):
            Chao="Power.jpg"
        
        logging.info("EVO POWER")
        
    elif Dark>200:
        Chao="DevilChaos.jpg"
        logging.info("EVO DEVILCHAOS")
        
    elif Hero>200:
        Chao="HeroChaos.jpg"
        logging.info("EVO HEROCHAOS")
    
    elif Hero>200 and Dark>200:
        Chao="Chaos.jpg"
        logging.info("EVO CHAOS")
    
    else:
        if Hero>Dark and Hero>50:
            Chao="Hero.jpg"
            logging.info("EVO HERO")
            
        if Dark>Hero and Dark>50:
            Chao="Devil.jpg"
            logging.info("EVO DEVIL")
            
        if Dark==Hero or (Dark<50 and Hero<50):
            Chao="Normal.jpg"
            logging.info("EVO NORMAL")

@tl.job(interval=timedelta(seconds=0.05))
def ButtonPressd():
    global Chao
    global menu
    global inventory
    global shop
    global games
    global stat
    global OnOff
    global i
    
    
    if not button_C.value:
        if OnOff=='On':
            OnOff='Off'
            device.hide()
            Save()
            time.sleep(0.2)
        else:
            OnOff='On'
            device.show()
            time.sleep(0.2)
#    if not button_A.value and OnOff=='On':
        #if menu==False:
            #Chao=random.choice(ChaoList)
            #i+=1
            #time.sleep(0.2)
    if not button_B.value:
         if menu==False and OnOff=='On' and games==False and shop==False and racegui==False and stat==False and racing==False and inventory==False:
            menu=True
            Menu()

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)
            
def Menu():
    global i
    global MaxFrame   
    global frame
    global frameblx
    global framebsx
    global Chao
    global menu
    global inventory
    global shop
    global games
    global stat
    global Text
    global Inv
    
    w=0
    h=0
    selected=1
    Text='Shop'
    font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
    
    background = Image.new("1", device.size, "black")
    time.sleep(0.2)
    
   
    #games stat shop
    while menu==True:
        if not button_L.value :
            if selected==3:
                selected=2
                Text='Stat'
                time.sleep(0.2)
            else:    
                if selected==2:
                    selected=1
                    Text='Shop'
                    time.sleep(0.2)
                else:     
                    if selected==1:
                        selected=0
                        Text='Games'
                        time.sleep(0.2)
                    else:     
                        if selected==0:
                            selected=3
                            Text='Inventory'
                            time.sleep(0.2)
                
        if not button_R.value :
            if selected==0:
                selected=1
                Text='Shop'
                time.sleep(0.2)
            else:     
                if selected==1:
                    selected=2
                    Text='Stat'
                    time.sleep(0.2)
                else:     
                    if selected==2:
                        selected=3
                        Text='Inventory'
                        time.sleep(0.2)
                    else:     
                        if selected==3:
                            selected=0
                            Text='Games'
                            time.sleep(0.2)
                
                
        if not button_B.value:
            if selected==0:
                games=True
                menu=False
                GamesMenu()
            if selected==1:
                shop=True
                menu=False
                ShopMenu()
            if selected==2:
                stat=True
                menu=False
                StatMenu()
            if selected==3 and len(Inv)!=0:
                inventory=True
                menu=False
                InventoryMenu()
        if not button_A.value:
            menu=False
            return
        
        background = Image.new("1", device.size, "black")       
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize("< "+ Text + " >", font=font)            
        TextOffset=((device.width-w) / 2,(device.height-30) / 2)
        draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")  
        if selected==3:
            w, h = draw.textsize(str(len(Inv)), font=font)            
            TextOffset=((device.width-w) / 2,(device.height-30))
            draw.text(TextOffset,str(len(Inv)),font=font, fill="white")    
        device.display(background.convert(device.mode))
        


        
def ShopMenu():
    pass
    
def StatMenu():
    global menu
    global stat
    global Swim
    global Fly
    global Run
    global Power
    global Stamina
    global Dark
    global Hero
    
    while stat:
        Text='Swim'
        font = make_font("C&C Red Alert [INET].ttf", device.height - 50)
    
        background = Image.new("1", device.size, "black")
    
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Swim', font=font)            
        TextOffset=(0,5)
        draw.text(TextOffset,'Swim',font=font, fill="white")    
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Lv '+str(Swim), font=font)            
        TextOffset=(device.width-35,5)
        draw.text(TextOffset,'Lv '+str(Swim),font=font, fill="white")   
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Fly', font=font)            
        TextOffset=(0,15)
        draw.text(TextOffset,'Fly',font=font, fill="white")    
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Lv '+str(Fly), font=font)            
        TextOffset=(device.width-35,15)
        draw.text(TextOffset,'Lv '+str(Fly),font=font, fill="white")   
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Run', font=font)            
        TextOffset=(0,25)
        draw.text(TextOffset,'Run',font=font, fill="white")    
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Lv '+str(Run), font=font)            
        TextOffset=(device.width-35,25)
        draw.text(TextOffset,'Lv '+str(Run),font=font, fill="white")   
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Power', font=font)            
        TextOffset=(0,35)
        draw.text(TextOffset,'Power',font=font, fill="white")    
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Lv '+str(Power), font=font)            
        TextOffset=(device.width-35,35)
        draw.text(TextOffset,'Lv '+str(Power),font=font, fill="white")   
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize('Dark/Hero ', font=font)            
        TextOffset=(0,45)
        draw.text(TextOffset,'Dark/Hero ',font=font, fill="white")  
        
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize(str(Dark)+'/'+str(Hero), font=font)            
        TextOffset=(device.width-40,45)
        draw.text(TextOffset,str(Dark)+'/'+str(Hero),font=font, fill="white")  
        
        #font = make_font("C&C Red Alert [INET].ttf", device.height - 54)
        #draw = ImageDraw.Draw(background)
        #w, h = draw.textsize('< >', font=font)            
        #TextOffset=((int(device.width/2),54))
        #draw.text(TextOffset,'< >',font=font, fill="white")  
        
        
        device.display(background.convert(device.mode))
                    
        
        if not button_A.value:
            stat=False
            menu=True
            Menu()

def InventoryMenu():
    global i
    global MaxFrame
    global frame
    global frameblx
    global framebsx
    global Chao
    global menu
    global inventory
    global shop
    global games
    global stat
    global Text
    global InvList
    global Hero
    global Dark
    global Fly
    global Run
    global Swim
    global Power
    global Stamina
    global Inv
    global Dec
    global Ani
    global YAni
    global BackMove
    w=0
    h=0   
    time.sleep(0.2)
    Text=''
    font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
    
    background = Image.new("1", device.size, "black")
    time.sleep(0.2)
    
    index=0
    
    while inventory==True:
        if not button_L.value :
            if index!=0:
                index-=1
            else:
                index=len(Inv)-1
            time.sleep(0.2)
            
        if not button_R.value :
            if index!=len(Inv)-1:
                index+=1
            else:
                index=0
            time.sleep(0.2)
                
        Text=Inv[index]
        if not button_B.value:
            if Text=="Run Fruit":
                Run+=1
                del Inv[index]
                
            if Text=="Fly Fruit":
                Fly+=1
                del Inv[index]
                
            if Text=="Swim Fruit":
                Swim+=1
                del Inv[index]
                
            if Text=="Power Fruit":
                Power+=1
                del Inv[index]
                
            if Text=="Stamina Fruit":
                Stamina+=5
                del Inv[index]
            
            if Text=="Hero Fruit":
                Hero+=5
                del Inv[index]
                
            if Text=="Dark Fruit":
                Dark+=5
                del Inv[index]
                
            if Text=="Chao Fruit":
                Run+=1
                Fly+=1
                Power+=1
                Swim+=1
                del Inv[index]
            Dec='Eat'   
            Ani=eat
            YAni=[5,5,5,5]
            BackMove=False
            inventory=False
            menu=False
            
        
        if not button_A.value:
            inventory=False
            menu=True
            Menu()
            return
        if inventory==True:
            background = Image.new("1", device.size, "black")       
            draw = ImageDraw.Draw(background)
            w, h = draw.textsize("< "+ Text + " >", font=font)            
            TextOffset=((device.width-w) / 2,(device.height-30) / 2)
            draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
            w, h = draw.textsize(str(index+1), font=font)            
            TextOffset=((device.width-w) / 2,(device.height-30))
            draw.text(TextOffset,str(index+1),font=font, fill="white")    
            device.display(background.convert(device.mode))

def GamesMenu():
    global menu
    global games
    global Text
    global selected
    global race
    global fight
    global racelevel
    selected=0
    Text='Race'
    font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
    
    background = Image.new("1", device.size, "black")
    time.sleep(0.2)
    
    
    #games stat shop
    while games==True:
        
        if not button_L.value :
            if selected==0:
                selected=3
                Text='Casino'
                time.sleep(0.2)
            else:     
                if selected==3:
                    selected=2
                    Text='Race'
                    time.sleep(0.2)
                else:
                    if selected==2:
                        selected=1
                        Text='Fight'
                        time.sleep(0.2)
                    else:
                        if selected==1:
                            selected=0
                            Text='Guess'
                            time.sleep(0.2)
                
        if not button_R.value :
            if selected==0:
                selected=1
                Text='Fight'
                time.sleep(0.2)
            else:     
                if selected==1:
                    selected=2
                    Text='Race'
                    time.sleep(0.2)
                else:
                    if selected==2:
                        selected=3
                        Text='Casino'
                        time.sleep(0.2)
                    else:
                        if selected==3:
                            selected=0
                            Text='Guess'
                            time.sleep(0.2)
                        
                            
                
        if not button_B.value:
            if selected==0:
                race=True
                games=False
                RaceMenu()
            if selected==1:
                fight=True
                games=False
                FightMenu()
            
        if not button_A.value:
            games=False
            menu=True
            Menu()
            return
        
        background = Image.new("1", device.size, "black")       
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize("< "+ Text + " >", font=font)            
        TextOffset=((device.width-w) / 2,(device.height-30) / 2)
        draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
        device.display(background.convert(device.mode))
    selected=0
    
def RaceMenu():
    global menu
    global games
    global Text
    global selected
    global race
    global fight
    global racelevel
    global racing
    time.sleep(0.2)
    font = make_font("C&C Red Alert [INET].ttf", device.height - 52)
    background = Image.new("1", device.size, "black")
    Text='Select the race type'
    background = Image.new("1", device.size, "black")       
    draw = ImageDraw.Draw(background)
    w, h = draw.textsize("< "+ Text + " >", font=font)            
    TextOffset=((device.width-w) / 2,(device.height-30) / 2)
    draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
    device.display(background.convert(device.mode))
    time.sleep(1.5)
    font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
    Text='Run'
    selected=2
    while race==True:
        
        if not button_L.value :
            if selected==3:
                selected=2
                Text='Run'
                time.sleep(0.2)
            else:     
                if selected==2:
                    selected=1
                    Text='Fly'
                    time.sleep(0.2)
                else:     
                    if selected==1:
                        selected=0
                        Text='Swim'
                        time.sleep(0.2)
                    else:     
                        if selected==0:
                            selected=3
                            Text='Power'
                            time.sleep(0.2)
                
        if not button_R.value :
            if selected==0:
                selected=1
                Text='Fly'
                time.sleep(0.2)
            else:     
                if selected==1:
                    selected=2
                    Text='Run'
                    time.sleep(0.2)
                else:     
                    if selected==2:
                        selected=3
                        Text='Power'
                        time.sleep(0.2)
                    else:     
                        if selected==3:
                            selected=0
                            Text='Swim'
                            time.sleep(0.2)
        
        
        background = Image.new("1", device.size, "black")       
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize("< "+ Text + " >", font=font)            
        TextOffset=((device.width-w) / 2,(device.height-30) / 2)
        draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
        device.display(background.convert(device.mode))
        
        if not button_B.value:
            race=False
            games=False
            racing=True
            CreateRace(Text)
            return
            
        if not button_A.value:
            games=True
            menu=False
            GamesMenu()
            return
        
        
        
        
        
    

def CreateRace(Sel):
    global menu
    global games
    global Text
    global selected
    global racing
    global race
    global fight
    global RunMedal
    global FlyMedal
    global SwimMedal
    global PowerMedal
    global RaceLenght
    global RaceType
    global racegui
    global Selection
    MaxLevel=1
    Selection=Sel
    if Selection=='Fly':
        MaxLevel=FlyMedal
        RaceType='Fly'
    if Selection=='Run':
        MaxLevel=RunMedal
        RaceType='Run'
    if Selection=='Power':
        MaxLevel=PowerMedal
        RaceType='Power'
    if Selection=='Swim':
        MaxLevel=SwimMedal
        RaceType='Swim'
    
    
    font = make_font("C&C Red Alert [INET].ttf", device.height - 52)
    background = Image.new("1", device.size, "black")
    Text='Select the level'
    background = Image.new("1", device.size, "black")       
    draw = ImageDraw.Draw(background)
    w, h = draw.textsize("< "+ Text + " >", font=font)            
    TextOffset=((device.width-w) / 2,(device.height-30) / 2)
    draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
    device.display(background.convert(device.mode))
    time.sleep(1.5)
    selected=0
    
    background = Image.new("1", device.size, "black")       
    draw = ImageDraw.Draw(background)
    Text='*'
    w, h = draw.textsize("< "+ Text + " >", font=font)            
    TextOffset=((device.width-w) / 2,(device.height-30) / 2)
    draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
    device.display(background.convert(device.mode))
    font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
    while racing==True:
        if not button_L.value :
            if selected==4:
                selected=3
                Text='****'
                time.sleep(0.2)
            else:     
                if selected==3:
                    selected=2
                    Text='***'
                    time.sleep(0.2)
                else:     
                    if selected==2:
                        selected=1
                        Text='**'
                        time.sleep(0.2)
                    else:     
                        if selected==1:
                            selected=0
                            Text='*'
                            time.sleep(0.2)
                        else:     
                            if selected==0 and MaxLevel==4:
                                selected=4
                                Text='*****'
                                time.sleep(0.2)
                
        if not button_R.value :
            if selected==0 and MaxLevel==2:
                selected=1
                Text='**'
                time.sleep(0.2)
            else:     
                if selected==1 and MaxLevel==3:
                    selected=2
                    Text='***'
                    time.sleep(0.2)
                else:     
                    if selected==2 and MaxLevel==4:
                        selected=3
                        Text='****'
                        time.sleep(0.2)
                    else:     
                        if selected==3 and MaxLevel==5:
                            selected=4
                            Text='*****'
                            time.sleep(0.2)
                        else:     
                            if selected==4:
                                selected=0
                                Text='*'
                                time.sleep(0.2)
        
        
        background = Image.new("1", device.size, "black")       
        draw = ImageDraw.Draw(background)
        w, h = draw.textsize("< "+ Text + " >", font=font)            
        TextOffset=((device.width-w) / 2,(device.height-30) / 2)
        draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
        device.display(background.convert(device.mode))
    
        
        if not button_B.value:
            racing=False
            RaceLenght=random.randint(100*MaxLevel,150*MaxLevel)
            RaceType=Selection
            racegui=True
            RaceGUI()
            return
            
        if not button_A.value:
            games=False
            menu=False
            race=True
            RaceMenu()
            return
        
    
def CreateRacer():
    global ListRacer
    global Chao
    global Fly
    global Run
    global Swim
    global Power
    global Int
    global Luck
    global NameList
    global Name
    pointchoosen=0
    
    Face=''
    fly=0
    run=0
    swim=0
    power=0
    intell=0
    luck=0
    del ListRacer[:]
    ListRacer=[[Chao,Fly,Run,Swim,Power,Int,Luck,""]]
    ListRacer[0][0]=Chao
    ListRacer[0][1]=Fly
    ListRacer[0][2]=Run
    ListRacer[0][3]=Swim
    ListRacer[0][4]=Power
    ListRacer[0][5]=Int
    ListRacer[0][6]=Luck
    ListRacer[0][7]=Name
    i=0
    while (i<7):
        i=i+1
        ChaoPoint=Fly+Run+Swim+Power+Int+Luck
        ChaoPoint=random.randint(ChaoPoint,ChaoPoint)
        while(ChaoPoint>0):    
                selection=random.randint(1,6)
                if selection==1:
                    pointchoosen=random.randint(1,ChaoPoint)
                    fly=fly+pointchoosen
                    ChaoPoint=ChaoPoint-pointchoosen
                if selection==2:
                    pointchoosen=random.randint(1,ChaoPoint)
                    run=run+pointchoosen
                    ChaoPoint=ChaoPoint-pointchoosen
                if selection==3:
                    pointchoosen=random.randint(1,ChaoPoint)
                    swim=swim+pointchoosen
                    ChaoPoint=ChaoPoint-pointchoosen
                if selection==4:
                    pointchoosen=random.randint(1,ChaoPoint)
                    power=power+pointchoosen
                    ChaoPoint=ChaoPoint-pointchoosen
                if selection==5:
                    pointchoosen=random.randint(1,ChaoPoint)
                    intell=intell+pointchoosen
                    ChaoPoint=ChaoPoint-pointchoosen
                if selection==6:
                    pointchoosen=random.randint(1,ChaoPoint)
                    luck=luck+pointchoosen
                    ChaoPoint=ChaoPoint-pointchoosen
        if fly>run and fly>swim and fly>power:
            Face=random.choice(["Fly.jpg","DevilFly.jpg","HeroFly.jpg"])
        else:
            if run>fly and run>swim and run>power:
                Face=random.choice(["Run.jpg","DevilRun.jpg","HeroRun.jpg"])
            else:
                if swim>fly and swim>run and swim>power:
                    Face=random.choice(["Swim.jpg","DevilSwim.jpg","HeroSwim.jpg"])
                else:
                    if power>fly and power>run and power>swim:
                        Face=random.choice(["Power.jpg","DevilPower.jpg","HeroPower.jpg"])
                    else:
                        Face=random.choice(ChaoList)
        ListRacer.append([Face,fly,run,swim,power,intell,luck,random.choice(NameList)])
    logging.info(ListRacer)
    return
    



class Ball(object):
    def __init__(self, w, h, radius, color,f,r,s,p,intel,l,ID):
        global Positions
        global Trip
        global RaceLenght
        global Selection
        global boost
        
        self.Boost=boost
        self.id=ID
        self.fly=f
        self.run=r
        self.swim=s
        self.power=p
        self.intel=intel
        self.luck=l
        if Selection=='Fly':
            self.speed=self.fly
        if Selection=='Run':
            self.speed=self.run
        if Selection=='Power':
            self.speed=self.power
        if Selection=='Swim':
            self.speed=self.swim
        
        self._w = w
        self._h = h
        self._radius = radius
        self._color = color
        self._x_speed =(self.speed/RaceLenght)+1 #(random.random() - 0.5) * 10
        self._y_speed =0 #(random.random() - 0.5) * 10
        self._x_pos = 1
        self._y_pos = self._h - 10
        self.counter=0
        
        
    def update_pos(self):
        
        if self._x_pos + self._radius > self._w and self._x_speed!=0.001 and self._x_speed!=0:
            self._x_speed = 0
            Positions.append(self.id)
            logging.info(Positions)
            return
        
        if self.counter==0 and self._x_speed==0.001:
            self._x_speed =(self.speed/RaceLenght)+1
        
        if self.counter==0 and random.randint(int(12-(self.speed/100)),100)>99 and self._x_speed!=0.001:
            self.counter=random.randint(5,15)
        
        if self.counter!=0:
            self._x_speed =0.001
            self.counter=self.counter-1
            return

        elif self._x_pos - self._radius < 0.0:
            self._x_speed = abs(self._x_speed)

        if self._y_pos + self._radius > self._h:
            self._y_speed = 0
            
        elif self._y_pos - self._radius < 0.0:
            self._y_speed = abs(self._y_speed)
        
        if self.id==0 and self.Boost==True:
            self._x_pos += self._x_speed+0.5
        else:
            self._x_pos += self._x_speed
        
        self._y_pos += self._y_speed

    def draw(self, canvas):
        global CurrentChao
        if CurrentChao==self.id:
            canvas.ellipse((self._x_pos - self._radius, self._y_pos - self._radius,
                       self._x_pos + self._radius, self._y_pos + self._radius), fill='black',outline='black')
            canvas.ellipse((self._x_pos - int(self._radius/2), self._y_pos - self._radius-2,
                       self._x_pos + int(self._radius/2), self._y_pos + self._radius), fill='black',outline='black')
        else:
            canvas.ellipse((self._x_pos - self._radius, self._y_pos - self._radius,
                       self._x_pos + self._radius, self._y_pos + self._radius), fill=self._color,outline='black')

        
    

def RaceGUI():
    global Stamina
    global w
    global h     
    global Chao
    global frame
    global MaxFrame
    global ListRacer
    global CurrentChao
    global Positions
    global Text
    global race
    global racing
    global racegui
    global menu
    global fight
    global stat
    global games
    global shop
    global inventory
    global RunMedal
    global FlyMedal
    global SwimMedal
    global PowerMedal
    global Selection
    global Ani
    global YAni
    global walk
    global fall
    global Trip
    global boost
    del Positions[:]
    ChaoSelected=Chao
    CurrentChao=0
    CreateRacer()
    
    boost=False
    Bcount=8
    
    i=0
    balls=[Ball(device.width, device.height, 3, 'white',ListRacer[i][1],ListRacer[i][2],ListRacer[i][3],ListRacer[i][4],ListRacer[i][5],ListRacer[i][6],i) for i in range(0,8,1)]
    #canvas = luma.core.render.canvas(device)
    Trip=False
    Ani=fall
    YAni=[2,2,2,2]
    MaxStam=Stamina
    time.sleep(0.2)
    while(True):  
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'SpritesJpeg', ChaoSelected))
        spritemap = Image.open(img_path).convert("1")
        background = Image.new("L",device.size, "white")
        
        draw = ImageDraw.Draw(background)
        font = make_font("C&C Red Alert [INET].ttf", device.height - 50)
        f, t = draw.textsize(str(ListRacer[CurrentChao][7]), font=font)            
        TextOffset=(device.width-48,5)
        draw.text(TextOffset,str(ListRacer[CurrentChao][7]),font=font, fill="black")
        
        draw = ImageDraw.Draw(background)
        font = make_font("C&C Red Alert [INET].ttf", device.height - 50)
        f, t = draw.textsize(str("Stamina"), font=font)            
        TextOffset=(2,5)
        draw.text(TextOffset,str("Stamina"),font=font, fill="black")
        
        scale = device.height / float(h)
        new_size = (int((scale * w)/2.5), int(device.height/2.5))
        if Trip==True:
            Ani=fall
            YAni=[2,2,2,2]
        else:
            Ani=walk
            YAni=[0,0,0,0]
        x = w * (Ani[frame] % 8)
        y = h * (YAni[frame] % 8)
        img = spritemap.crop((x, y, x + w, y + h)).resize(new_size)   
        offset = ((device.width - img.width) // 2)
        background.paste(img, (offset, 0))
        if not button_R.value:
            #Stamina-=0.1
            #boost=True
            if CurrentChao<7:
                CurrentChao=CurrentChao+1
                ChaoSelected=ListRacer[CurrentChao][0]
                
            else:
                CurrentChao=0
                ChaoSelected=ListRacer[CurrentChao][0]
                
        if not button_L.value:
            #Stamina-=0.1
            #boost=True
            if CurrentChao>0:
                CurrentChao=CurrentChao-1
                ChaoSelected=ListRacer[CurrentChao][0]
               
            else:
                CurrentChao=7
                ChaoSelected=ListRacer[CurrentChao][0]
        
        if not button_B.value:
            if MaxStam>0 and boost==False:
                MaxStam-=5
                boost=True
                logging.info("Boost " + str(boost))
            else:
                 if MaxStam<6:
                    MaxStam=0
                    
                
        if boost==True and Bcount!=0:
            Bcount-=1        
            logging.info("Bcount " + str(Bcount))
            
        if Bcount==0:
            Bcount=8
            boost=False
            
        time.sleep(0.2)
        #device.display(background.convert(device.mode))
        canvas = luma.core.render.canvas(device,background.convert(device.mode))
        frame += 1
        if Trip==True and frame==MaxFrame:
            frame -=1
        if frame == MaxFrame:
            frame = 0
        with canvas as c:
            c.line([(2,device.height-3),(device.width-3,device.height-3)])
            if MaxStam!=0:
                c.line([(4,20),(((MaxStam/Stamina)*40),20)],"black",2)
            #c.rectangle(device.bounding_box, outline="white", fill="white")
            for b in balls:
                if CurrentChao==b.id and b._x_speed==0:
                    frame=0
                if CurrentChao==b.id and b._x_speed==0.001:
                    Trip=True
                else:
                    if CurrentChao==b.id and b._x_speed!=0.001:
                        Trip=False
                b.Boost=boost
                b.update_pos()
                b.draw(c)
        if len(Positions)>7:
            if Positions[0]==0:
                Text='FIRST PLACE'
                font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
                background = Image.new("1", device.size, "black")    
                draw = ImageDraw.Draw(background)
                f, t = draw.textsize("< "+ Text + " >", font=font)            
                TextOffset=((device.width-f) / 2,(device.height-30) / 2)
                draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
                device.display(background.convert(device.mode))
                time.sleep(2)
                racegui=False
                menu=False
                inventory=False
                shop=False
                games=False
                stat=False
                race=False
                racing=False
                racegui=False
                if Selection=='Fly':
                    FlyMedal=FlyMedal+1
                if Selection=='Run':
                    RunMedal=RunMedal+1
                if Selection=='Power':
                    PowerMedal=PowerMedal+1
                if Selection=='Swim':
                    SwimMedal=SwimMedal+1
                
                
                return
            if Positions[1]==0:
                Text='SECOND PLACE'
                font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
                background = Image.new("1", device.size, "black")    
                draw = ImageDraw.Draw(background)
                f, t = draw.textsize("< "+ Text + " >", font=font)            
                TextOffset=((device.width-f) / 2,(device.height-30) / 2)
                draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
                device.display(background.convert(device.mode))
                time.sleep(2)
                racegui=False
                menu=False
                inventory=False
                shop=False
                games=False
                stat=False
                race=False
                racing=False
                racegui=False
                
                return
            if Positions[2]==0:
                Text='THIRD PLACE'
                font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
                background = Image.new("1", device.size, "black")    
                draw = ImageDraw.Draw(background)
                f, t  = draw.textsize("< "+ Text + " >", font=font)            
                TextOffset=((device.width-f) / 2,(device.height-30) / 2)
                draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
                device.display(background.convert(device.mode))
                time.sleep(2)
                racegui=False
                menu=False
                inventory=False
                shop=False
                games=False
                stat=False
                race=False
                racing=False
                racegui=False
                
                return
            if Positions[3]==0 or Positions[4]==0 or Positions[5]==0 or Positions[6]==0 or Positions[7]==0:
                Text='TOO BAD'
                font = make_font("C&C Red Alert [INET].ttf", device.height - 40)
                background = Image.new("1", device.size, "black")    
                draw = ImageDraw.Draw(background)
                f, t  = draw.textsize("< "+ Text + " >", font=font)            
                TextOffset=((device.width-f) / 2,(device.height-30) / 2)
                draw.text(TextOffset,"< "+ Text + " >",font=font, fill="white")    
                device.display(background.convert(device.mode))
                time.sleep(2)
                racegui=False
                menu=False
                inventory=False
                shop=False
                games=False
                stat=False
                race=False
                racing=False
                racegui=False
                
                return

            
def FightMenu():
    pass

def Slot():
    pass

def Number():
    pass

@tl.job(interval=timedelta(seconds=VelocityDec))
def Decision():
    global Chao
    global Dec
    global Ani
    global YAni
    global BackMove
    global ObjList
    global Age
    global Evolve
    global Inv
    global i
    if menu==True or games==True or shop==True or stat==True or racing==True or racegui==True or race==True or inventory==True:
        return
    
    RandomEncounter=random.randint(0,100)
    RandomPlace=random.randint(0,100)
    
    
    logging.info("AGE " + str(Age))
    if Age>=100 and Evolve==False:
        Evolve=True
        Evolution()
    
    Dec=random.choice(Mood)
    #Lets explore
    
    
    
        
    logging.info("DEC " + Dec)
    if Dec=="Walk":
        Ani=walk
        YAni=[0,0,0,0]
        BackMove=True
        Age=Age+0.1
        if RandomPlace>99:
            i=random.choice([0,1,2])
            logging.info("back + " + str(i))
        if RandomEncounter>99:
            Dec="Happy"
            Inv.append(random.choice(ObjList))
            logging.info("INV + " + str(Inv))
    if Dec=="Swim":
        if Swim/10>2:
            Ani=swimming
            YAni=[4,4,4,4]
            BackMove=True
            Age=Age+0.1
            if RandomPlace>99:
                i=random.choice([0,1,2])
                logging.info("back + " + str(i))
            if RandomEncounter>99:
                Dec="Happy"
                Inv.append(random.choice(ObjList))
                logging.info("INV + " + str(Inv))
        else:
            Ani=cantswim
            YAni=[3,4,3,4]
            BackMove=False
        
    if Dec=="Fly":
        Ani=fly
        YAni=[5,5,5,5]
        BackMove=True
        Age=Age+0.1
        if RandomPlace>99:
            i=random.choice([0,1,2])
            logging.info("back + " + str(i))
        if RandomEncounter>99:
            Dec="Happy"
            Inv.append(random.choice(ObjList))
            logging.info("INV + " + str(Inv))
    if Dec=="Sleep":
        Ani=sleep
        YAni=[3,3,3,3]
        BackMove=False
    if Dec=="Sad":
        Ani=cry
        YAni=[3,3,3,3]
        BackMove=False
    if Dec=="Tired":
        Ani=sit
        YAni=[0,0,0,0]
        BackMove=False
    if Dec=="Happy":
        Ani=jump
        YAni=[6,7,7,7]
        BackMove=False
    if Dec=="Think":
        Ani=thinking
        YAni=[3,3,3,3]
        BackMove=False
    if Dec=="Hello":
        Ani=hellothere
        YAni=[7,7,7,7]
        BackMove=False
    if Dec=="Draw":
        Ani=drawing
        YAni=[1,1,1,1]
        BackMove=False
    

@tl.job(interval=timedelta(seconds=0.5))
def Animation():
    global i
    global MaxFrame
    global w
    global h     
    global bw
    global bh
    global frame
    global frameblx
    global framebsx
    global Chao
    global menu
    global imglx
    global imgrx
    global meters
    global background
    global BackMove
    if menu==True or games==True or shop==True or stat==True or racing==True or racegui==True or race==True or inventory==True:
        return
    
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'SpritesJpeg', Chao))
    spritemap = Image.open(img_path).convert("1")
    background = Image.new("L", device.size, "white")
    img_bak = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'SpritesJpeg', Back))
    spritebak= Image.open(img_bak).convert("1")
    

   
    scale = device.height / float(h)
    scaleb =device.height / float(bh)
    new_size = (int(scale * w), device.height)
    new_sizeb =  (int(scaleb * bw), device.height)
    
    x = w * (Ani[frame] % 8)
    y = h * (YAni[frame] % 8)
           
    bxsx = 38 + bw * (frameblx % 8)
    
    bxdx= 38 + bw * (framebsx % 8)
    if BackMove==True:   
        by = 94 + bh * (i)
        #by = 35 + bh * (i)
        imglx = spritebak.crop((bxsx, by, bxsx + bw, by + bh)).resize(new_sizeb)
        imgrx = spritebak.crop((bxdx, by, bxdx + bw, by + bh)).resize(new_sizeb)
        meters+=0.5
    else:
        imglx = spritebak.crop((bxsx, 94 + bh * (i), bxsx + bw, 94 + bh * (i)+bh)).resize(new_sizeb)
        imgrx = spritebak.crop((bxdx, 94 + bh * (i), bxdx + bw, 94 + bh * (i)+bh)).resize(new_sizeb)
        
    img = spritemap.crop((x, y, x + w, y + h)).resize(new_size)           
    
            
    offset = ((device.width - img.width) // 2)
    offsetlx = 0
    offsetrx = ((device.width - imgrx.width))
    background.paste(img, (offset, 0))
    background.paste(imglx, (offsetlx, 0))
    background.paste(imgrx, (offsetrx, 0))
    device.display(background.convert(device.mode))
            
    frame += 1
    if BackMove==True:
        frameblx+= 2
        framebsx+= 2
    if frame == MaxFrame:
        frame = 0
        if BackMove==True:
            frameblx= 0
            framebsx= 1
            
            
if __name__ == "__main__":
    try:
        j=0
        device = get_device()
        background = Image.new("L", device.size, "black")
        device.display(background.convert(device.mode))
        if os.path.isfile("/home/pi/Chao.save"):
            print ("File exist")
            Load()
        else:
            print ("File not exist")
            while (j<30):
                Mood[j]=random.choice(Choice)
                logging.info(Mood[j])
                j+=1
            i=random.choice([0,1,2])
        tl.start(block=True)
    except KeyboardInterrupt:
        pass
        
    