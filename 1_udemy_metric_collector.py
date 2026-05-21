import requests
import json
import time
import os

# --- ENTERPRISE ENGINE DESIGN ---
# High-ticket sectors where instructors have capital and urgent marketing needs
TARGET_SECTORS = [
    "python programming",
    "real estate marketing",
    "crypto trading",
    "excel automation"
]

# 20 listings per page. 2 pages = 40 hot prospects per sector.
MAX_PAGES_PER_SECTOR = 2  
DATABASE_FILE = "udemy_engine_db.json"

class UdemyMetricCollector:
    def __init__(self):
        """Initializes a high-trust browser fingerprint to access data layers safely."""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.udemy.com/",
            "Origin": "https://www.udemy.com"
        }
        self.api_url = "https://www.udemy.com/api-2.0/courses/"

    def load_existing_database(self):
        """Ensures we don't overwrite old data and can keep building our asset list."""
        if os.path.exists(DATABASE_FILE):
            try:
                with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def fetch_udemy_pool(self, keyword, page=1):
        """Queries Udemy's internal backend marketplace directory directly."""
        params = {
            "search": keyword,
            "page": page,
            "page_size": 20,
            "fields[course]": "title,visible_instructors,rating,num_subscribers,url",
            "ordering": "relevance"
        }
        try:
            response = requests.get(self.api_url, headers=self.headers, params=params, timeout=15)
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                print(f"      ⚠️ Search Link Diagnostic: Received status response {response.status_code}")
                return []
        except Exception as e:
            print(f"      ❌ Critical network timeout on sector segment: {e}")
            return []

    def process_raw_batch(self, raw_courses, keyword, current_db):
        """Cleans data, parses metadata, and structures target records."""
        new_records_count = 0
        existing_urls = {item["udemy_profile_url"] for item in current_db}
        
        for course in raw_courses:
            instructors = course.get("visible_instructors", [])
            if not instructors:
                continue
                
            instructor = instructors[0]
            profile_slug = instructor.get("url")
            full_profile_url = f"https://www.udemy.com{profile_slug}"
            
            # Duplication Guard: Never harvest the same instructor twice
            if full_profile_url in existing_urls:
                continue
                
            student_count = course.get("num_subscribers", 0)
            rating = course.get("rating", 0.0)
            
            lead_dossier = {
                "instructor_name": instructor.get("display_name"),
                "primary_course_title": course.get("title"),
                "market_niche": keyword,
                "student_count": student_count,
                "star_rating": round(rating, 2),
                "udemy_profile_url": full_profile_url,
                "personal_website": "Not Found",
                "twitter_url": "Not Found",
                "linkedin_url": "Not Found",
                "business_email": "Not Found",
                "whatsapp_number": "Not Found",
                "has_meta_pixel": "Unknown",
                "pipeline_status": "PENDING_DOMAIN_DISCOVERY" # Target flag for Script 2
            }
            
            current_db.append(lead_dossier)
            existing_urls.add(full_profile_url)
            new_records_count += 1
            
        return current_db, new_records_count

    def execute_mining_operation(self):
        """Runs the primary catalog data gathering routine."""
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🛡️  DAVIES | PARTNER LEAD ENGINE 2026")
        print("🚀 Executing Script 1: Master Database Init & Extraction")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        db = self.load_existing_database()
        print(f"📊 Current Database Stature: {len(db)} existing profiles loaded.")
        
        total_new = 0
        for sector in TARGET_SECTORS:
            print(f"📡 Harvesting Category Segment: [{sector.upper()}]")
            for page in range(1, MAX_PAGES_PER_SECTOR + 1):
                print(f"   ↳ Crawling Catalog Registry Page {page}...")
                raw_data = self.fetch_udemy_pool(sector, page)
                
                if not raw_data:
                    break
                    
                db, new_scraped = self.process_raw_batch(raw_data, sector, db)
                total_new += new_scraped
                time.sleep(2.5) # Compliance throttling to stay safe
                
        # Save records back to file matrix
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
            
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"✅ HARVEST COMPLETE: Added {total_new} brand new high-intent target matrices.")
        print(f"📂 Master Matrix file updated successfully: `{DATABASE_FILE}`")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    engine = UdemyMetricCollector()
    engine.execute_mining_operation()
                          
