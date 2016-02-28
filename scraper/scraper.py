import requests
import json
from time import sleep

#country to iso-2 mapping
with open('country_iso3166.json') as data_file:    
    data = json.load(data_file)

#top 100 countries by GDP
major_countries = ["United States", "China", "Japan", "India", "Germany", "United Kingdom", "Russia", "Brazil", "Italy", "Mexico", "Spain", "Canada", "South Korea", "Indonesia", "Turkey", "Iran", "Australia", "Taiwan", "Netherlands", "Poland", "Saudi Arabia", "Argentina", "Thailand", "South Africa", "Pakistan", "Egypt", "Colombia", "Belgium", "Malaysia", "Venezuela", "Sweden", "Greece", "Nigeria", "Ukraine", "Austria", "Philippines", "Switzerland", "Hong Kong", "Romania", "Czech Republic", "Norway", "Chile", "Vietnam", "Singapore", "Peru", "Portugal", "Algeria", "Bangladesh", "Hungary", "Denmark", "Israel", "Finland", "Ireland", "United Arab Emirates", "Kazakhstan", "Kuwait", "Morocco", "Slovakia", "New Zealand", "Belarus", "Iraq", "Angola", "Cuba", "Ecuador", "Syria", "Bulgaria", "Sri Lanka", "Libya", "Sudan", "Qatar", "Tunisia", "Serbia", "Dominican Republic", "Azerbaijan", "Croatia", "Uzbekistan", "Puerto Rico", "Guatemala", "Oman", "Ethiopia", "Lithuania", "Kenya", "Slovenia", "Yemen", "Myanmar", "Tanzania", "Costa Rica", "Lebanon", "El Salvador", "Bolivia", "Cameroon", "Uruguay", "North Korea", "Luxembourg", "Latvia", "Panama", "Uganda", "Ghana", "Ivory Coast", "Honduras"]

#map country code to country name
def getCC(name):
     for cc,cname in data.items():
         if cname.upper() == name.upper():
             return cc

#count routes between countries
def getRoute(src, dst):
    while True :
        r = requests.get('http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/GB/GBP/en-GB/' + src + '/' + dst + '/anytime/anytime',params={'apiKey': 'ah336295199871411555194842941115'},headers={'Accept': 'application/json'})
        if r.status_code >= 400:
            #error
            print('error')
            if r.status_code == 400:
                return -1
            elif r.status_code == 403:
                return -2
            elif r.status_code == 500:
                return -3
            else:
                sleep(1)
        else:
            if 'Quotes' in r.json():
                return len(r.json()['Quotes'])
            else:
                return 0;

def main():
    routes = []
    for src in major_countries:
        for dst in major_countries:
            if not src == dst:
                num = getRoute(getCC(src),getCC(dst))
                print(src + "," + dst + "," + str(num))
                routes.append({
                'e' : src,
                'i' : dst,
                'v' : num,
                'wc' : 'mil'
                })
                sleep(1)
    output = {
      "timeBins": [{
        "data":routes}]}
    with open('routes.json', 'w') as outfile:
        json.dump(output, outfile)
    
if __name__ == "__main__":
    main()