#!/bin/python
# downtime detector scraper
#import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from   urllib.request import Request, urlopen
import datetime
import argparse

class downdetector_scraper:
   company_name=""
   start_year=0
   start_month=0
   end_year=0
   end_month=0
   data_file=""
   debug=None

   # init/constructor for class
   def __init__(self,company,start_year,start_month,end_year=None,end_month=None,data_file=None,debug=None):
      now = datetime.datetime.now()

      self.company_name=company
      self.start_year=start_year
      self.start_month=start_month
      
      if end_year==None:
         self.end_year=now.year
      else:
         self.end_year=end_year
      
      if end_month==None:
         self.end_month=now.month
      else:
         self.end_month=end_month
      
      if data_file==None:
         self.data_file="{0}_{1}_{2}-{3}_{4}_downtime.csv".format(self.company_name,self.start_year,self.start_month,self.end_year,self.end_month)
      else:
         self.data_file=data_file

      self.debug=debug
      
   # used for printing info messages to the screen for the user
   def info(self,msg):
      print(" Info: "+msg)

   # used for printing error messages to the screen for the user
   def error(self,msg):
      print(" Error: "+msg)

   # used for preformatting ARCHIVE URL's
   def get_url(self,year,month,company_name):
      month_str="{0:02d}".format(month)
      url="https://downdetector.com/status/{2}/archive/{0}/{1}/".format(year,month_str,company_name)
      return url

   # used for matching string in the HTTP content
   def detect_start(self,data,match):
      if match in data.strip():
         return True
      return None

   # used for dumping the data to disk
   def write_data(self,file,header,data):
      try:
         dest_file = open(file, 'w') 
         # header needed for plotting
         dest_file.write(header+"\n")
         # data
         dest_file.write("\n".join(data))
         # Closing file 
         dest_file.close() 
      except Exception as ex:
         print("Error: {0}".format(ex))

   # initial round of url scraping
   def scrape_archive_urls(self):
      downtime=[]

      for year in range(self.start_year,self.end_year+1):
         for month in range(1,13):
            # ignore time ranges out of bounds.. (easy math)
            if self.start_year==year and month<self.start_month: 
               continue
            if self.end_year==year and month>self.end_month: 
               continue
            url=self.get_url(year,month,self.company_name)

         if self.debug:
            self.info("Parsing: {0}".format(url))
            try:
               req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
               data = urlopen(req).read()
               if "No outages here" in str(data):
                  if self.debug:
                     self.info("No outages for: {0}-{1}".format(year,month))
                  continue
               lines=str(data).split("\\n")
               
               for line in lines:
                  if "problems-at" in line:
                     url="https://downdetector.com/"+line.strip()[10:-3]
                     downtime.append(url)
            except :
               self.error("Company name invalid")
               exit(1)
      return downtime

   def scrape_incident_urls(self,urls):
      # loop through url's and pull them down one at a time ans scrape.
      start_line="series: ["
      end_line="]"
      mapped_data=[]
      for url in urls:
         req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
         if self.debug:
            self.info("Parsing: {0}".format(url))
         data = urlopen(req).read()
         data=str(data).split("\\n")
         in_data=None
         for data_l in data:
            # Data looks like -> { x: \'2020-04-15T03:44:32-04:00\', y: 1  },
            if in_data:
               point=data_l.strip()
               if "http" in data_l:
                  continue
               p_year=point[7:32]
               token=point.split("y:")
               if len(token) >1:
                  p_count=token[1][0:-2].strip()
               else:
                  continue
               if p_count=="0":
                  continue
               # at some point they changed date format.. then changed back... just fix the data
               year2=p_year.replace(".13085","-04:00")
               row="{0},{1}".format(year2,p_count)
               if self.debug:
                  self.info(row)

               mapped_data.append(row)
               if self.detect_start(data_l,end_line):
                  break;
               continue

            if self.detect_start(data_l,start_line):
               in_data=True
      return mapped_data;


   # main processing function
   def parse(self):
      # this gives us a list of incident pages to parse
      downtime=self.scrape_archive_urls()
      data=self.scrape_incident_urls(downtime)
      header='"date","count"'
      self.write_data(self.data_file,header,data)
      return data

def plot_downtime(file,plot_title):
   data = pd.read_csv(file, usecols=['date','count'], parse_dates=['date'])
   data.set_index('date',inplace=True)

   #plot data
   fig, ax = plt.subplots(figsize=(15,2))
   data.plot(ax=ax)

   #set ticks every week
   if plot_title=="M":
      ax.xaxis.set_major_locator(mdates.MonthLocator())
   elif plot_title=="W":
      ax.xaxis.set_major_locator(mdates.WeekdayLocator())
   elif plot_title=="D":
      ax.xaxis.set_major_locator(mdates.DayLocator())
   #set major ticks format
   ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
   #data.plot(kind='bar', ax=ax)
   plt.show()



parser = argparse.ArgumentParser(description='downdetector datascrapeer')
parser.add_argument('--company'    , '-c' , help='the company name you wish to get data for', required=True)
parser.add_argument('--start-year' , '-sy', help='beginning year to search from'            , type=int, required=True)
parser.add_argument('--start-month', '-sm', help='beginning month to search from'           , type=int, required=True)
parser.add_argument('--end-year'   , '-ey', help='ending year to search to. Defaults to this year'  , type=int, default=None)
parser.add_argument('--end-month'  , '-em', help='ending month to search to. Defaults to this month', type=int, default=None)
parser.add_argument('--output'     , '-o' , help='The file you want to dump the csv data into. Defaults to a calculated name in this directory',default=None)
parser.add_argument('--plot'       , '-p' , help='plot this data in a window' ,action='store_true', default=None)
parser.add_argument('--plot-title' , '-pt', help='X axis titles: M=Months, W=Weeks, D=Days. Defaults to M' , default="D")
parser.add_argument('--debug'      , '-d' , help='show processing information',action='store_true', default=None)

args = parser.parse_args()

if args.company:
   scraper=downdetector_scraper(args.company,args.start_year,args.start_month,args.end_year,args.end_month,args.output,args.debug)
   scraper.parse()

   if args.plot:
      # I just combo'd this function to get a quick plot
      plot_downtime(scraper.data_file,args.plot_title)
else:
   parser.print_help()
