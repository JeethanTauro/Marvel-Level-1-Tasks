import requests
from bs4 import BeautifulSoup

domain = input("Enter the website: ")

response = requests.get(f"https://who.is/whois/{domain}") #made a response

content = response.text #put all the text in content

parsed_content = BeautifulSoup(content,'html.parser') #parsed the content

ip_address = parsed_content.find_all('div', class_="col-4 queryResponseBodyValue")
ip_address_list = []
for tag in ip_address:
    ip_address_list.append(tag.text.strip())
print(ip_address_list)


#for the documentation => https://beautiful-soup-4.readthedocs.io/en/latest/