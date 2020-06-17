# downdetector_feed
a simple python demo script which parses the downdetector website for json data for use in reporting



## usage
```bash

downdetector datascrapeer

optional arguments:
  -h, --help            show this help message and exit
  --company COMPANY, -c COMPANY
                        the company name you wish to get data for
  --start-year START_YEAR, -sy START_YEAR
                        beginning year to search from
  --start-month START_MONTH, -sm START_MONTH
                        beginning month to search from
  --end-year END_YEAR, -ey END_YEAR
                        ending year to search to. Defaults to this year
  --end-month END_MONTH, -em END_MONTH
                        ending month to search to. Defaults to this month
  --output OUTPUT, -o OUTPUT
                        The file you want to dump the csv data into. Defaults to a calculated name in this directory
  --plot, -p            plot this data in a window
  --plot-title PLOT_TITLE, -pt PLOT_TITLE
                        X axis titles: M=Months, W=Weeks, D=Days. Defaults to M
  --debug, -d           show processing information

 ```

