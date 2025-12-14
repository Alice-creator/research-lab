from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from tee_public.spiders.constant import SELECTOR
from typing import Optional

def add_or_replace_query_string(url: str, **updates) -> str:
    u = urlparse(url)
    query_string = parse_qs(u.query)
    for k, v in updates.items():
        query_string[k] = [v]
    new_q = urlencode([(k, v) for k, vals in query_string.items() for v in vals])
    return urlunparse(u._replace(query=new_q))

def get_page_num(url: str) -> int:
    try:
        return int(parse_qs(urlparse(url).query).get("page", ["1"])[0])
    except Exception:
        return 1
    
def extract_next_href(response) -> Optional[str]:
    return response.css(SELECTOR["rel_next"]).get()
