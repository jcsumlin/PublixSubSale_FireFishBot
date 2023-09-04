import requests
import re
from loguru import logger

from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('TOKEN')
instance = os.getenv('INSTANCE')
headers = {
 'Authorization': 'Bearer ' + token,
}


pattern = re.compile("^Save \$\d\.\d{2} on Whole$")
data = requests.get(
    'https://services.publix.com/search/productdata/productitems?Id=b69a5de8-8d37-4746-b8eb-199faecdd786&StoreNbr=1724&pbsource=WEB_PD_ORDER_AHEAD_MENU_EXPERIENCE')
if not data.ok:
    logger.error("failed to get publix sale items")
data = data.json()

for item in data:
    if item["promoMsg"] is not None and pattern.match(item['promoMsg']):
        logger.debug("Sale Item Found")
        logger.info(item["title"])
        chicken_tender = False
        if "Chicken Tender" in item["title"]:
            message = f"YES!\n\n#Publix {item['title']} {item['priceLine']}"
        else:
            message = f"No!\n\n#Publix {item['title']} {item['priceLine']}"
        json_data = {
            'text': message,
        }

        response = requests.post('https://' + instance + '/api/notes/create', headers=headers, json=json_data)
        response = response.json()
        logger.debug(response["createdNote"]["id"])
        logger.debug(response["createdNote"]["text"])
        break

