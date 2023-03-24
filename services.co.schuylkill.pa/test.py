import requests
from bs4 import BeautifulSoup
from lxml import etree
import csv

import urllib.request

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

# test
import time

with open('counter.csv', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        counter = int(row[0])
csv_writer = open('order1.csv','a',encoding='utf-8')

for i in range(counter,90000):
    if not connect():
        print('waiting for internet')
        time.sleep(700)


    try:
        url = f"https://services.co.schuylkill.pa.us/mapviewercontent/cama.asp?id={counter}"
        
        
        # import pdb;pdb.set_trace()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        tree = etree.HTML(str(soup))


        csv_writer = open('order1.csv','a',encoding='utf-8')
        all_data = tree.xpath('//*[@face="Verdana, Arial, Helvetica, sans-serif"]') 
        parcel_address = tree.xpath('//*[@face="Verdana, Arial, Helvetica, sans-serif"]/text()') 
    

        max_data = all_data[4].text.strip()
        parcel_address_1 =parcel_address[5].strip()
        parcel_address_2 =parcel_address[6].strip()
        parcel_address = parcel_address_1 + ' '+ parcel_address_2.replace(',','')
        
        
        school_district = all_data[8].text.strip().replace(',','')
        muncipality = all_data[10].text.strip().replace(',','')
        land_use_type = all_data[21].text.strip().replace(',','')
        roll_section = all_data[23].text.strip().replace(',','')
        assessment_property_class = all_data[25].text.strip().replace(',','')


        owner_info = tree.xpath('//html/descendant::*[@width="607"][1]//*[@face="Verdana, Arial, Helvetica, sans-serif"]')
        try:
            owner_name = owner_info[5].text.strip()
            owner_name = owner_name.split(' ',1)
            owner_first_name = owner_name[0].replace(',','')
            
        except:
            owner_first_name = ''
        try:
            owner_last_name =  owner_name[1].replace(',','')
        except:
            owner_last_name = ''
            
        try:
            owner_address = owner_info[6].text.strip().replace(',','')
        except:
            owner_Address = ''

        deed_bk_pg = owner_info[7].text.strip().replace(',','')

        sale_date = owner_info[8].text.strip().replace(',','')

        bill_info = tree.xpath('//html/descendant::*[@width="607"][2]//*[@face="Verdana, Arial, Helvetica, sans-serif"]')

        bill_owner_name = bill_info[3].text.strip().replace(',','').replace(',','')
        try:
            bill_owner_name = bill_owner_name.split()
            bill_owner_first_name = bill_owner_name[0]
        except:
            bill_owner_first_name = ''
            
        try:
            bill_owner_last_name = bill_owner_name[1]
        except:
            bill_owner_last_name = ''
        bill_owner_address = bill_info[4].text.strip().replace(',',';')
        mailing_address = bill_owner_address
        
        base_year = []
        value = tree.xpath('//html/descendant::*[text()="Base Year Value"]/ancestor::td[2]//*[@face="Verdana, Arial, Helvetica, sans-serif"]')


        for i in range(5,22,2):
            base_year_value = value[i].text.strip()
            base_year.append(base_year_value)
            
        base_year = str(base_year).replace(',',';')   
        site_information = tree.xpath("//html/descendant::*[contains(text(),'Site ')]/ancestor::td[2]//*[@face='Verdana, Arial, Helvetica, sans-serif']")

        site = site_information[2].text.strip()

        csv_writer.write(f'{max_data},{parcel_address},{school_district},{muncipality},{land_use_type},{roll_section},\
            {assessment_property_class},{owner_first_name},{owner_last_name},{owner_address},{deed_bk_pg},{sale_date}, \
            {mailing_address},{bill_owner_first_name },{bill_owner_last_name } , {base_year},{site}\n')
        print(counter) 
        counter = counter + 1
        counter_writer = open('counter.csv','w')
        counter_writer.write(str(counter))
    
       

    except:
        print(counter) 
        counter = counter + 1
        counter_writer = open('counter.csv','w')
        counter_writer.write(str(counter))
    
 


