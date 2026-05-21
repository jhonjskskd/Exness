import requests
from bs4 import BeautifulSoup
import json
import time
import os

DATABASE_FILE = "udemy_engine_db.json"

class UdemyDomainDiscoverer:
    def __init__(self):
        """
        Establishes an enterprise-grade desktop browser fingerprint 
        to bypass frontend profiling blocks on Udemy's static pages.
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://www.udemy.com/"
        }

    def load_database(self):
        """Loads your central local storage lead registry safely."""
        if not os.path.exists(DATABASE_FILE):
            print(f"❌ Structural Failure: Database `{DATABASE_FILE}` not located. Run Script 1 first.")
            return []
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Database Access Error: Could not read JSON file structural format: {e}")
            return []

    def follow_redirects(self, initial_url):
        """
        Ensures we get the true business destination if the instructor 
        uses shorteners or tracking link pathways.
        """
        try:
            response = requests.get(initial_url, headers=self.headers, timeout=8, allow_redirects=True)
            return response.url
        except:
            return initial_url

    def extract_external_assets(self, profile_url):
        """Crawls the profile page source code deeply to pull raw anchor points."""
        discovered_assets = {
            "personal_website": "Not Found",
            "twitter_url": "Not Found",
            "linkedin_url": "Not Found"
        }
        
        try:
            response = requests.get(profile_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"      ⚠️ Network warning: Profile wall returned connection status: {response.status_code}")
                return discovered_assets

            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look across the primary layout block where external profiles are systematically placed
            links_container = soup.find("div", class_="instructor-profile--links--")
            if not links_container:
                # Fallback sweep to check all links across the entire canvas profile area
                links_container = soup.find("div", class_="main-content-context") or soup
                
            for anchor in links_container.find_all("a", href=True):
                href_raw = anchor["href"].strip()
                href_lower = href_raw.lower()
                
                # Filter structural assets into clear communication targets
                if "twitter.com" in href_lower or "x.com" in href_lower:
                    discovered_assets["twitter_url"] = href_raw
                elif "linkedin.com" in href_lower:
                    discovered_assets["linkedin_url"] = href_raw
                elif "udemy.com" not in href_lower and "facebook.com" not in href_lower and "youtube.com" not in href_lower:
                    # Resolve links if they point out to personal portfolios or custom agencies
                    if href_raw.startswith("http"):
                        final_destination = self.follow_redirects(href_raw)
                        discovered_assets["personal_website"] = final_destination
                    
        except Exception as e:
            print(f"      ❌ Script Exception: Internal layout tracking disrupted: {e}")
            
        return discovered_assets

    def execute_discovery(self):
        """Processes the master matrix backlog and saves status updates safely."""
        db = self.load_database()
        if not db:
            print("⚠️ Pipeline Idle: No actionable database entries identified.")
            return

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🛡️  DAVIES | PARTNER LEAD ENGINE 2026")
        print("🚀 Executing Script 2: Full Profile Domain Discoverer")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        updates_tracked = 0

        for lead in db:
            # Targets only the pristine entries scraped from Script 1
            if lead.get("pipeline_status") == "PENDING_DOMAIN_DISCOVERY":
                name = lead["instructor_name"]
                print(f"📡 Probing External Footprints for: [{name.upper()}]")
                
                # Execute link extractions
                assets = self.extract_external_assets(lead["udemy_profile_url"])
                lead.update(assets)
                
                # Progress flag so Script 3 knows exactly which entries are enriched
                lead["pipeline_status"] = "PENDING_CONTACT_CRAWL"
                updates_tracked += 1
                
                print(f"   ↳ Core Domain: {lead['personal_website']}")
                print(f"   ↳ Twitter/X:  {lead['twitter_url']}")
                print(f"   ↳ LinkedIn:   {lead['linkedin_url']}")
                
                # Strategic server safety window delay
                time.sleep(3.2)

        if updates_tracked > 0:
            # Rewrite updated list to the central file framework in-place
            with open(DATABASE_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4, ensure_ascii=False)
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"✅ CONVERSION: Mapped {updates_tracked} new target records.")
            print(f"📂 Master File Registry `{DATABASE_FILE}` successfully updated.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        else:
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("ℹ️  Pipeline Review: No newer profiles required enrichment at this time.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    engine = UdemyDomainDiscoverer()
    engine.execute_discovery()
      
