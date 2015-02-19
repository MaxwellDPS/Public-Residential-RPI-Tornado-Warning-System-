import feedparser
import pifacedigitalio as pfio
import time
import smtplib
import datetime

tornado = False
horn = False
strobe = False
_alarm = False
alarmack = False
reset_ = False

mailsent =False
mailalreadysent = False
pfio.init()



while True:
        print("------------------------------------------------------------------")
         #url = 'http://alerts.weather.gov/cap/us.php?x=1'
        url = 'http://alerts.weather.gov/cap/wwaatmget.php?x=NEC109&y=0'
        feed = feedparser.parse(url)
        print (feed.entries[0].title)
        if feed.entries[0].has_key("cap_event") is False:
            
                print('Alert: None')
                tornado = False
                
              
        else:
           
                print ('Alert:', feed.entries[0].cap_event)
                if feed.entries[0].cap_event == "Tornado Warning":
                        tornado = True
                        sendmail()
                        
                else:
                        tornado = False
                        
        localtime = time.asctime( time.localtime(time.time()) )
        
        print("Tornado Warning:",tornado)
        print ("Current Local Time:", localtime)
        print("------------------------------------------------------------------")
       
        
#ALARM
        
        if tornado == True:
                _alarm = True
                horn = True
                strobe = True
                print("---------------------------------------------------------------------")
                print("Tornado Warning Issued, TAKE SHELTER... TAKE SHELTER... TAKE SHELTER")
                print("ALARM ACTIVE")
                print("---------------------------------------------------------------------")
               
        else:
                _alarm = False
                horn = False
                strobe = False                
                print("---------------------------------------------------------------------")
                print("No Tornado Warning Issued")
                print("ALARM INACTIVE")
                print("---------------------------------------------------------------------")
              
                
       
        if pfio.digital_read(0) == 1:
                alarmack= True
        else:
                alarmack = False
        if pfio.digital_read(1) == 1:
                reset_ = True
        else:
                reset_ = False
      
       
        #GPIO
        _rly1 = False
        _rly2 = False
        
        _reset = False
        #while True:
        print("---------------------------------------------------------------------")
        if reset_ == False:
                if horn == True and alarmack == False:
                        _rly2 = True
                        print("Horn: Active")
                elif alarmack == True and horn == True:
                        _rly2 = False
                        print("Horn: Inactive")
                        _rly2 = False
                elif alarmack== False and horn == False:
                        print("Horn: Inactive")
                        _rly2 = False                                
                if strobe == True:
                        _rly1 = True
                        print("Strobe: Active")
                else:
                        _rly1 = False
                        print("Strobe: Inactive")
        else:
                _reset = True
                _rly1 = False
                _rly2 = False
        print("---------------------------------------------------------------------")   
                
        
         
        if _rly1 == True:
                pfio.digital_write(0,1)
        else:
                pfio.digital_write(0,0)
        if _rly2 == True:
                pfio.digital_write(1,1)
        else:
                pfio.digital_write(1,0)  
                
       
        print("reset")
       
        

        
