import requests
from bs4 import BeautifulSoup
import json
import re
import time
import os

DATABASE_FILE = "udemy_engine_db.json"

class ContactScraper:
    def __init__(self):
        # High-trust browser agent to guarantee entry into external instructor domains
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }
        # Deep text scraping regex pattern to catch raw email chains natively
        self.email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    def load_database(self):
        """Loads data records from the master JSON asset matrix."""
        if not os.path.exists(DATABASE_FILE):
            print(f"❌ Structural Failure: Database File `{DATABASE_FILE}` not found.")
            return []
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Access Error: Could not parse database contents: {e}")
            return []

    def crawl_site_source(self, site_url):
        """Crawls HTML data deeply to unearth secret communication and pixel data."""
        extracted_data = {"email": "Not Found", "whatsapp": "Not Found", "has_pixel": "No"}
        
        # Skip if Script 2 did not successfully locate an external website profile
        if not site_url or site_url == "Not Found" or not site_url.startswith("http"):
            return extracted_data

        try:
            response = requests.get(site_url, headers=self.headers, timeout=12)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            lower_html = html_content.lower()

            # 1. PIXEL ANALYSIS: Verify if the domain is leaking audience traffic
            if "fbevents.js" in lower_html or "connect.facebook.net" in lower_html or "fbq(" in lower_html:
                extracted_data["has_pixel"] = "Yes"

            # 2. EMAIL HARVEST: Isolate pristine text strings matching standard email paths
            all_emails = re.findall(self.email_regex, html_content)
            if all_emails:
                # Discard asset junk paths that mimic email formatting patterns
                clean_emails = [
                    email for email in all_emails 
                    if not email.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', 'email.com'))
                ]
                if clean_emails:
                    # Select the primary discovered email address asset
                    extracted_data["email"] = clean_emails[0]

            # 3. WHATSAPP DETECT: Trace anchor hooks for instant chat links
            for anchor in soup.find_all("a", href=True):
                href = anchor["href"].lower().strip()
                if "wa.me/" in href or "api.whatsapp.com/send" in href or "whatsapp.com/biz/" in href:
                    # Clean out query chains to isolate the pure phone digit variables
                    phone_match = re.search(r'(?:wa\.me|phone=|send\?phone=)([^&?/ \s]+)', href)
                    if phone_match:
                        # Strip symbols to store the clean international format number
                        clean_num = re.sub(r'[^\d]', '', phone_match.group(1))
                        if clean_num:
                            extracted_data["whatsapp"] = f"+{clean_num}"
                            break

        except Exception as e:
            print(f"      ⚠️  Domain Skip: Connection dropped or timeout during analysis on link.")
            
        return extracted_data

    def run_pipeline(self):
        """Runs the loop, updates records, and updates the state of the database file."""
        db = self.load_database()
        if not db:
            print("⚠️ Pipeline Halt: Active lead records are currently empty.")
            return

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🛡️  DAVIES | PARTNER LEAD ENGINE 2026")
        print("🚀 Executing Script 3: Deep Contact & Technical Scraper")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        records_processed = 0

        for lead in db:
            if lead.get("pipeline_status") == "PENDING_CONTACT_CRAWL":
                name = lead["instructor_name"]
                domain_url = lead["personal_website"]
                
                print(f"🔍 Digging HTML source variables for: [{name.upper()}]")
                
                # Run the deep domain check execution
                site_metrics = self.crawl_site_source(domain_url)
                
                lead["business_email"] = site_metrics["email"]
                lead["whatsapp_number"] = site_metrics["whatsapp"]
                lead["has_meta_pixel"] = site_metrics["has_pixel"]
                
                # Shift status flag seamlessly forward so Script 4 can process it
                lead["pipeline_status"] = "PENDING_COPYWRITING"
                records_processed += 1
                
                print(f"   ↳ Scraped Email: {lead['business_email']}")
                print(f"   ↳ Scraped WhatsApp: {lead['whatsapp_number']}")
                print(f"   ↳ Meta Pixel Active: {lead['has_meta_pixel']}")
                print("   -------------------------------------------------")
                
                # Calm trailing break window to protect networking processes
                time.sleep(2.5)

        if records_processed > 0:
            # Commit the newly found information straight back to local storage
            with open(DATABASE_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4, ensure_ascii=False)
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"✅ HARVEST SUCCESS: Processed and updated {records_processed} instructor domains.")
            print(f"📂 Storage Matrix updated locally inside: `{DATABASE_FILE}`")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        else:
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("ℹ️  Pipeline Notice: No pending domains required contact scraping.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    engine = ContactScraper()
    engine.run_pipeline()

