import requests
import json
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

# cookies = {
#     'currency': 'EUR',
#     'AKA_A2': 'A',
#     'ABTest_ABTEST_COMPARATOR_CPE_BE': 'ABTEST_COMPARATOR%40A%402024-09-17%2011%3A01%3A58',
#     'storedSearchParams': '{"multiparticipants":[{"senior":{"key":2,"value":2},"adult":{"key":1,"value":1},"pet":{"key":0,"value":0},"ages":[{"key":4,"value":4},{"key":11,"value":11},{"key":9,"value":9},{"key":9,"value":9},{"key":8,"value":8}]}],"countrysite":[{"key":"l2_HA","code":"HA","value":""}],"isFlexPeriod":false,"flexZone":"","date":[{"key":"2025-07-07","value":"2025-07-07"}],"dateend":[{"key":"2025-07-13","value":"2025-07-13"}]}',
#     'marketLanguageChoice': 'be-wl',
#     'SESSIONID': '33bmbv48qvk9h081fapsecojep',
#     'productHistory': '{"HA":{"startDate":"2025-07-07","duration":"6","capacity":8,"hc":"HA1813"}}',
#     'leadGen': '{"location":"https://www.centerparcs.be/be-wl/belgique/fp_HA_vacances-domaine-park-de-haan/cottages","count":3}',
#     'biasingSearchParams': '{"HA":2}',
#     'mainSearchUsed': '2',
# }

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,nl;q=0.7,fr-FR;q=0.6,nl-BE;q=0.5,fr-BE;q=0.4,it-IT;q=0.3,it;q=0.2',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.centerparcs.be/be-wl',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
}

# Generate all monday dates for the specified year
def mondays(year):
    jan1 = date(year,1,1)
    
    monday = jan1 + timedelta(days=(7-jan1.weekday()) %7)
    
    while 1:
        if monday.year != year:
            break
        yield monday
        monday += timedelta(days=7)

result = []

for monday in mondays(2025):
    # Request search page for all monday between April and September
    if monday.month >= 4 and monday.month <= 9 :
        response = requests.get(
            f'https://www.centerparcs.be/be-wl/belgique/fp_HA_vacances-domaine-park-de-haan/cottages?market=be&language=wl&c=CPE_PRODUCT&univers=cpe&type=PRODUCT_COTTAGES&item=HA&currency=EUR&group=housing&sort=popularity_housing&asc=asc&page=1&nb=30&displayPrice=default&dateuser=1&facet[NUMBEROFBEDROOMS][]=4&facet[DISPO]=-1&facet[DATE]={monday}&facet[DATEEND]={monday+timedelta(days=6)}&facet[COUNTRYSITE][]=l2_HA&facet[MULTIPARTICIPANTS][0][adult]=1&facet[MULTIPARTICIPANTS][0][senior]=2&facet[MULTIPARTICIPANTS][0][pet]=0&facet[MULTIPARTICIPANTS][0][ages][]=4&facet[MULTIPARTICIPANTS][0][ages][]=11&facet[MULTIPARTICIPANTS][0][ages][]=9&facet[MULTIPARTICIPANTS][0][ages][]=9&facet[MULTIPARTICIPANTS][0][ages][]=8',
#             cookies=cookies,
            headers=headers,
        )

        # populate the list with start date, prices and resultListPrio (which contains prices and more information from webpage)
        soup = BeautifulSoup (response.text, "html.parser")
        resultListPrio = soup.find("div",class_="resultListPrio")
        try:
            prices = [div["data-pricecollapse"] for div in resultListPrio.find_all("div",class_="accCart")]
        except AttributeError:
            prices = [0, 0]
        try:
            result.append({str(monday): (prices[0], prices[1], str(resultListPrio))})
        except IndexError :
            result.append({str(monday): (None, None, str(resultListPrio))})


# save all data in a file name based on today
filename = datetime.now().strftime("%Y_%m_%d")+".json"
with open(filename, "w") as outfile:
    outfile.write(json.dumps(result))