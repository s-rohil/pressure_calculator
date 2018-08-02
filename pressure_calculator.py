from creds import key,url
import requests
import datetime
from datetime import timedelta
from uszipcode import ZipcodeSearchEngine
import argparse


class Pressure():


    def __init__(self,key,url):
        self.key=key
        self.url=url


    def calculatepressure(self,zipcode):

        try:


            start_dt = datetime.datetime.now() - timedelta(days=5)
            end_dt = datetime.datetime.now() - timedelta(days=1)
            start_dt = start_dt.strftime('%Y-%m-%d')
            end_dt = end_dt.strftime('%Y-%m-%d')
            my_date=','.join((start_dt,end_dt))

            final_url = url+key+'/postal_codes/'+str(zipcode)+',us/history.json?'
            final_params = {'period':'day','timestamp_between':my_date,'fields':'timestamp,mslPresAvg'}
            y = requests.get(url=final_url, params=final_params)
            t = requests.get(url=final_url,params=final_params)
            x= t.json()
            #print (x)
            new_list=[]
            for item in x:
                new_list.append((item['timestamp'][:10], item['mslPresAvg']))

            my_list = sorted(new_list,key=lambda k:k[1], reverse=True)
            #print(my_list)
            print ('Date            '+'Pressure')
            for element in my_list:
                print('{}      {}'.format(element[0],element[1]))
        except:
            print("Unexpected error occured. Please try again later")

    def validZip(self,zip):
        search = ZipcodeSearchEngine()
        zipcode = search.by_zipcode(zip)
        if zipcode['Zipcode'] is not None:
            self.calculatepressure(zipcode=zipcode['Zipcode'])
        else:
            print('Please enter a valid zip code')



if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description="A script to find atmospheric pressure of a location given by zip code")
    parser.add_argument("--echo", help='Instructions for using this tool.\n E.g - python pressure_calculator.py --zip 02120')
    parser.add_argument("-z","--zip" ,action='store',help='Please provide a valid zip code')
    try:
        args = parser.parse_args()

        if args.zip:
            p = Pressure(key, url=url)
            p.validZip(args.zip)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print('Unexpected Interrupt encountered')
    except:
        parser.print_help()




