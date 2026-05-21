from flask import Flask, jsonify
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

# CRITICAL: This defines the top-level 'app' variable Vercel is demanding
app = Flask(__name__)

@app.route('/')
@app.route('/api')
def run_pipeline():
    """Triggers the full 5-script automated data pipeline."""
    try:
        print("🚀 Vercel Webhook Triggered: Initiating Davies Partner Lead Engine...")
        
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

        return jsonify({
            "status": "success",
            "engine": "Davies_Partner_Udemy_Engine_2026",
            "message": "Pipeline executed successfully! Check your Telegram app for active lead cards."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Pipeline execution failed: {str(e)}"
        }), 500

# Required for local testing if running manually
if __name__ == '__main__':
    app.run(debug=True)
