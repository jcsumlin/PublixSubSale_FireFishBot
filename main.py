import requests
import re
from loguru import logger

from faunadb import query as q
from faunadb.client import FaunaClient
from dotenv import load_dotenv
import os

load_dotenv()

client = FaunaClient(secret=os.getenv("FAUNA_KEY"))
coll = client.query(q.collection("sub_sale"))

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
            chicken_tender = True
        doc = client.query(q.create(coll, {'data': {'sub': item["title"], 'is_chicken_tender': chicken_tender}}))
        break
