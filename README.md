# RSS-PROJECT
Project is about using rss feeds to create an excel report of desired Contents.
#xlsx.py
# This python file executes one function i.e:
  1. This function crawls the rss feed urls from file.xlsx and creates an output excel file with all the links in new file.xlsx
     
#comparision.py 
# This python File executes two functions i.e:
  1. Select the output_file from rss feeds and update new contents there after removing the old files based on the timestamp of the file
  2. Later the newly updated file is sent to filter the matching keyword using keywords.xlsx file
  3. Desired content file is saved in the s3 folder

#ses.py
# This function executes one function i.e:
  1. This function will create an email to subscriber and attach the file with matching contents as decribed by the subcriber.
  2. Uses SES to send mail to verified subscriber.
