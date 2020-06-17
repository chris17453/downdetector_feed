# downdetector_feed
a simple python demo script which parses the downdetector website for json data for use in reporting

### note
This was a 3 hour demo project. Nothing deep. Evaluate as such

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


## Example
```
# show me the issues at amazon for June of 2020. Plot and use Days in the title
# csv is saved to the local directory calculated
./downdetector_feed.py -c amazon  -sy 2020 -sm 6 -d -p -pt d

```
## example plot of the data
![](amazon.png?raw=true)

## exxample csv data
```
"date","count"
2020-06-11T03:44:10-04:00,4
2020-06-11T03:59:10-04:00,7
2020-06-11T04:14:10-04:00,6
2020-06-11T04:29:10-04:00,6
2020-06-11T04:44:10-04:00,2
2020-06-11T04:59:10-04:00,4
2020-06-11T05:14:10-04:00,12
2020-06-11T05:29:10-04:00,9
2020-06-11T05:44:10-04:00,2
2020-06-11T05:59:10-04:00,1
2020-06-11T06:14:10-04:00,5
2020-06-11T06:29:10-04:00,4
2020-06-11T06:44:10-04:00,4
2020-06-11T06:59:10-04:00,9
2020-06-11T07:14:10-04:00,8
2020-06-11T07:29:10-04:00,4
2020-06-11T07:44:10-04:00,7
2020-06-11T07:59:10-04:00,14
2020-06-11T08:14:10-04:00,7
2020-06-11T08:29:10-04:00,6
2020-06-11T08:44:10-04:00,16
2020-06-11T08:59:10-04:00,12
2020-06-11T09:14:10-04:00,6
2020-06-11T09:29:10-04:00,8
```
