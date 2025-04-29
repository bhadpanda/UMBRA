import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from datetime import datetime
import json
import re
import argparse
from scrapy.exceptions import DropItem

OUTPUT_FILE = "umbra_output.json"

class DuplicatesPipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        key = item.get("url")
        if key in self.seen:
            raise DropItem("Duplicate item found: %s" % item)
        self.seen.add(key)
        return item

def validate_query(email=None, username=None, fullname=None):
    if email:
        pattern = r'^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
    elif username:
        pattern = r'^[A-Za-z0-9_.-]+$'
        if not re.match(pattern, username):
            raise ValueError("Invalid username format")
    elif fullname:
        pattern = r'^[A-Za-z ]+$'
        if not re.match(pattern, fullname.strip()):
            raise ValueError("Invalid fullname")
    else:
        raise ValueError("No input provided")

class UmbraSpider(scrapy.Spider):
    name = "umbra"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0",
        "LOG_LEVEL": "ERROR",
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "DOWNLOAD_TIMEOUT": 15,
        "COOKIES_ENABLED": False,
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "ITEM_PIPELINES": {
            '__main__.DuplicatesPipeline': 100
        }
    }

    def __init__(self, email=None, username=None, fullname=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validate_query(email=email, username=username, fullname=fullname)
        self.email = email
        self.username = username
        self.fullname = fullname
        self.start_urls = self.build_urls()
        self.collected_results = []

    def build_urls(self):
        urls = []

        if self.username:
            urls += [
                f"https://www.reddit.com/user/{self.username}",
                f"https://github.com/{self.username}",
                f"https://twitter.com/{self.username}",
                f"https://www.instagram.com/{self.username}",
                f"https://www.youtube.com/@{self.username}",
                f"https://www.facebook.com/{self.username}",
                f"https://dev.to/{self.username}",
                f"https://keybase.io/{self.username}",
                f"https://steamcommunity.com/id/{self.username}",
                f"https://medium.com/@{self.username}",
                f"https://{self.username}.tumblr.com",
                f"https://{self.username}.wordpress.com",
                f"https://venmo.com/{self.username}",
                f"https://html.duckduckgo.com/html/?q={self.username}+site:youtube.com"
            ]

        elif self.email:
            query_sites = [
                "pastebin.com", "haveibeenpwned.com", "dehashed.com",
                "twitter.com", "github.com", "facebook.com", "youtube.com"
            ]

            for site in query_sites:
                dork = f'"{self.email}" site:{site}'
                urls.append(f"https://html.duckduckgo.com/html/?q={dork}")

        elif self.fullname:
            name_query = '+'.join(self.fullname.strip().split())
            urls += [
                f"https://html.duckduckgo.com/html/?q={name_query}+site:linkedin.com",
                f"https://html.duckduckgo.com/html/?q={name_query}+site:facebook.com",
                f"https://html.duckduckgo.com/html/?q={name_query}+site:instagram.com",
                f"https://html.duckduckgo.com/html/?q={name_query}+site:just.edu.jo",
                f"https://html.duckduckgo.com/html/?q={name_query}+site:researchgate.net",
                f"https://html.duckduckgo.com/html/?q={name_query}+site:academia.edu",
                f"https://html.duckduckgo.com/html/?q={name_query}+site:youtube.com"
            ]

        return urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.errback_handler)

    def errback_handler(self, failure):
        self.logger.error(f"Request failed: {failure}")

    def parse(self, response):
        if "profile not found" in response.text.lower() or len(response.text) < 100:
            return

        title = response.css("title::text").get(default="N/A")
        text = " ".join(response.css("body *::text").getall()).lower()

        result = {
            "url": response.url,
            "status": response.status,
            "title": title
        }

        try:
            age = None
            age_match = re.search(r"(\d{1,2})\s?(?:y/?o|years?\s?old|yrs)", text)
            if age_match:
                age = age_match.group(1)
            else:
                birth_year_match = re.search(r"born\s?(in\s)?(19\d{2}|20[0-2]\d)", text)
                if birth_year_match:
                    birth_year = int(birth_year_match.group(2))
                    age = str(datetime.now().year - birth_year)
            if age:
                result["inferred_age"] = age
        except Exception as e:
            self.logger.warning(f"Failed to parse age: {e}")

        try:
            location_match = re.search(r"(?:lives in|based in|from|resides in)\s+([a-zA-Z\s,]+)", text)
            if location_match:
                result["inferred_location"] = location_match.group(1).strip()
        except Exception as e:
            self.logger.warning(f"Location detection failed: {e}")

        try:
            hobby_keywords = {
                "gaming": ["fps", "rpg", "videogames", "esports"],
                "music": ["guitar", "piano", "violin", "band"],
                "fitness": ["gym", "workout", "lifting"],
                "coding": ["python", "programming", "java", "github"],
                "drawing": ["art", "sketch", "painting"],
                "writing": ["poetry", "journal", "fanfic"],
                "reading": ["books", "reading", "library", "novel"],
                "traveling": ["travel", "wanderlust", "vacation", "backpacking"]
            }

            hobbies_found = [hobby for hobby, keys in hobby_keywords.items() if any(k in text for k in keys)]
            if hobbies_found:
                result["inferred_hobbies"] = hobbies_found
        except Exception as e:
            self.logger.warning(f"Hobby detection failed: {e}")

        self.collected_results.append(result)
        yield result

    def closed(self, reason):
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.collected_results, f, indent=2)
        self.logger.info(f"All results saved to: {OUTPUT_FILE}")

def run_cli():
    parser = argparse.ArgumentParser(description="UMBRA OSINT Scanner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--username", help="Target's username")
    group.add_argument("--email", help="Target's email")
    group.add_argument("--fullname", help="Target's full name")
    args = parser.parse_args()

    validate_query(email=args.email, username=args.username, fullname=args.fullname)

    print(f"Running OSINT scan on: {{'username': args.username, 'email': args.email, 'fullname': args.fullname}}")
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    process = CrawlerProcess()
    process.crawl(UmbraSpider, email=args.email, username=args.username, fullname=args.fullname)
    process.start()

if __name__ == "__main__":
     run_cli()
    
