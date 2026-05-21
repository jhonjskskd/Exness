from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Allow Python to look inside the root directory for your individual scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import execution components directly from your 5 scripts
from 1_udemy_metric_collector import UdemyMetricCollector
from 2_domain_discoverer import UdemyDomainDiscoverer
from 3_contact_scraper import ContactScraper
from 4_copywriter_engine import CopywriterEngine
from 5_telegram_dispatcher import TelegramDispatcher

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Triggers the full 5-script automated data pipeline."""
        print("🚀 Vercel Request Received: Initiating Davies Partner Lead Engine...")
        
        # 1. Execute Udemy Metric Extractions
        collector = UdemyMetricCollector()
        collector.execute_mining_operation()
        
        # 2. Parse Profile Layouts for Domain Targets
        discoverer = UdemyDomainDiscoverer()
        discoverer.execute_discovery()
        
        # 3. Scrape Target Web Codes for Emails & WhatsApp Numbers
        scraper = ContactScraper()
        scraper.run_scraper()
        
        # 4. Generate High-Converting Pitch Letter Variations
        copywriter = CopywriterEngine()
        copywriter.run_copywriting_compiler()
        
        # 5. Fire Agency Lead Cards Straight to Telegram Chat
        dispatcher = TelegramDispatcher()
        dispatcher.execute_dispatch_pipeline()

        # Build a clean JSON confirmation payload response for your web browser screen
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_payload = {
            "status": "success",
            "engine": "Davies_Partner_Udemy_Engine_2026",
            "message": "Pipeline executed. Check your Telegram app for active lead cards!"
        }
        
        self.wfile.write(json.dumps(response_payload).encode('utf-8'))

