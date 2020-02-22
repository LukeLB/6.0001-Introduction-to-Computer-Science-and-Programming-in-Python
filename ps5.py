# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
#from unittest.test.test_result import __init__
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    timezone = pytz.timezone("EST")
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)
        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
            pubdate = pubdate.astimezone(pytz.timezone('EST'))
            pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
        newsStory = NewsStory(guid, title, description, link, pubdate)    
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory():
    def __init__(self, guid, title, description, link, pubdate):
        self.g = guid
        self.t = title 
        self.d = description
        self.l = link 
        self.p = pubdate
    def get_guid(self):
        return self.g
        print(self.g)
    def get_title(self):
        return self.t
        print(self.t)
    def get_description(self):
        return self.d
        print(self.d)
    def get_link(self):
        return self.l
        print(self.l)
    def get_pubdate(self):
        return self.p
        print(self.p)



#======================
# Triggers
#======================

class Trigger(NewsStory):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__ (self, ph):
        self.ph = ph
    
def is_phrase_in(self, text):
        new_text = ''
        for chars in text: #takes out the punctuation of the inputted text and reforms this text as a string new_text
            if chars in string.punctuation:
                new_text += chars.replace(chars, ' ')
            else:
                new_text += chars 
        lower_string = new_text.lower()            #lower the case of the string
        text_list = new_text.split(' ')            #make string into a list
        new_list = list(filter(None, text_list))#filter list to remove spaces 
        s = ' ' 
        parsed_string = s.join(new_list)        #reform list into a string
        ps_string_length = len(parsed_string)+1                            #to make sure there is a space at the end of the phrase string and the text string
        parsed_string_space = parsed_string.ljust(ps_string_length)        #lines 114 to 118 were implemented to stop false positives for plurals by putting a space at the end of each string 
        lower_p = self.ph.lower()                                        
        p_string_length = len(lower_p)+1                                
        lower_p_space = lower_p.ljust(p_string_length)                    
        parsed_string_l = parsed_string_space.lower()                    
        if lower_p_space in parsed_string_l:
            return True 
        else:
            return False
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return is_phrase_in(self, story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return is_phrase_in(self, story.get_description())
        
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        self.tz = pytz.timezone("EST")
        self.tm = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        self.tmest = self.tz.localize(self.tm)
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate_v = story.get_pubdate()
        if pubdate_v < self.tmest:
            return True 
        else:
            return False 
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate_v = story.get_pubdate()
        if pubdate_v > self.tmest:
            return True
        else:
            return False 

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.tr = trigger 
    def evaluate(self, story):
        if self.tr.evaluate(story) is True:
            return False 
        elif self.tr.evaluate(story) is False:
            return True 

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.tr1 = trigger_1
        self.tr2 = trigger_2
    def evaluate(self, story):
        if self.tr1.evaluate(story) and self.tr2.evaluate(story) == True:
            return True 
        
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger_1, trigger_2):
        self.tr1 = trigger_1
        self.tr2 = trigger_2
    def evaluate(self, story):
        Trigger = 0
        while Trigger < 1:
            if self.tr1.evaluate(story) == True:
                Trigger += 1
            elif self.tr2.evaluate(story) == True:
                Trigger += 1
            else:
                return False     
        return True         
#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                filtered_stories.append(story)
    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

