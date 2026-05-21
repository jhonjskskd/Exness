from flask import Flask, jsonify
import sys
import os

# Ensure Python can find your root scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from 1_udemy_metric_collector import UdemyMetricCollector
from 2_domain_discoverer import UdemyDomainDiscoverer
from 3_contact_scraper import ContactScraper
from 4_copywriter_engine import CopywriterEngine
from 5_telegram_dispatcher import TelegramDispatcher

app = Flask(__name__)

@app.route('/')
@app.route('/api')
def run_pipeline():
    """Triggers the full pipeline completely in-memory to bypass Vercel's read-only disk."""
    try:
        print("🚀 Executing In-Memory Lead Generation Pipeline...")

        # 1. Collect initial metrics from Udemy
        collector = UdemyMetricCollector()
        # Custom override: intercept the list creation directly before it hits disk save
        db = []
        for sector in ["python programming", "real estate marketing", "crypto trading", "excel automation"]:
            raw_data = collector.fetch_udemy_pool(sector, page=1)
            db, _ = collector.process_raw_batch(raw_data, sector, db)

        if not db:
            return jsonify({"status": "idle", "message": "No new instructors found right now."}), 200

        # 2. Discover Domains (Process in-memory loop)
        discoverer = UdemyDomainDiscoverer()
        for lead in db:
            if lead.get("pipeline_status") == "PENDING_DOMAIN_DISCOVERY":
                assets = discoverer.extract_external_assets(lead["udemy_profile_url"])
                lead.update(assets)
                lead["pipeline_status"] = "PENDING_CONTACT_CRAWL"

        # 3. Scrape Contact Details & Pixels
        scraper = ContactScraper()
        for lead in db:
            if lead.get("pipeline_status") == "PENDING_CONTACT_CRAWL":
                site_metrics = scraper.crawl_site_source(lead["personal_website"])
                lead["business_email"] = site_metrics["email"]
                lead["whatsapp_number"] = site_metrics["whatsapp"]
                lead["has_meta_pixel"] = site_metrics["has_pixel"]
                lead["pipeline_status"] = "PENDING_COPYWRITING"

        # 4. Generate Copywriting Variations
        copywriter = CopywriterEngine()
        for lead in db:
            if lead.get("pipeline_status") == "PENDING_COPYWRITING":
                l_type, email_text, wa_text = copywriter.build_custom_pitches(lead)
                lead["instructor_segment"] = l_type
                lead["compiled_email_pitch"] = email_text
                
                import urllib.parse
                encoded_wa_string = urllib.parse.quote(wa_text)
                target_phone = lead["whatsapp_number"]
                if target_phone != "Not Found":
                    lead["whatsapp_launch_link"] = f"https://api.whatsapp.com/send?phone={target_phone.replace('+', '')}&text={encoded_wa_string}"
                else:
                    lead["whatsapp_launch_link"] = "No WhatsApp Number Available"
                lead["pipeline_status"] = "PENDING_DISPATCH"

        # 5. Dispatch Cards straight to Telegram Bot
        dispatcher = TelegramDispatcher()
        dispatched_count = 0
        for lead in db:
            if lead.get("pipeline_status") == "PENDING_DISPATCH":
                success = dispatcher.dispatch_lead_card(lead)
                if success:
                    lead["pipeline_status"] = "COMPLETED"
                    dispatched_count += 1

        return jsonify({
            "status": "success",
            "engine": "Davies_Partner_Udemy_Engine_2026",
            "leads_dispatched": dispatched_count
        }), 200

    except Exception as e:
        print(f"❌ Error during in-memory deployment run: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
