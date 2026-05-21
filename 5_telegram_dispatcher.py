import requests
import json
import os
import time

DATABASE_FILE = "udemy_engine_db.json"

# --- 2026 DAVIES VERIFIED CONFIGURATION ---
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

class TelegramDispatcher:
    def __init__(self):
        self.telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    def load_database(self):
        """Accesses your main local storage lead database."""
        if not os.path.exists(DATABASE_FILE):
            print(f"❌ Error: Database File `{DATABASE_FILE}` not found.")
            return []
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Access Error: Unable to read database: {e}")
            return []

    def dispatch_lead_card(self, lead):
        """Constructs an agency-style layout and pushes it to your Telegram."""
        name = lead["instructor_name"]
        niche = lead["market_niche"].upper()
        title = lead["primary_course_title"]
        students = lead["student_count"]
        rating = lead["star_rating"]
        email = lead["business_email"]
        phone = lead["whatsapp_number"]
        pixel = lead["has_meta_pixel"]
        segment = lead["instructor_segment"]
        wa_link = lead["whatsapp_launch_link"]
        email_body = lead["compiled_email_pitch"]

        # Dynamic visual indicator for tech deficits
        pixel_status = "✅ ACTIVE" if pixel == "Yes" else "❌ MISSING (Pixel Deficit Hook)"

        # PREMIUM AGENCY BRANDED LAYOUT
        message = (
            f"💎 **{segment} LEADER FOUND**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Instructor:** {name}\n"
            f"📚 **Niche Niche:** {niche}\n"
            f"📊 **Metrics:** {students:,} Students | {rating} ⭐\n"
            f"🌐 **Website Pixel:** {pixel_status}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📧 **Business Email:** `{email}`\n"
            f"📱 **WhatsApp ID:** `{phone}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 **Primary Course:** \"{title[:60]}...\"\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
        )

        # Append actionable link button if WhatsApp number was found
        if "http" in wa_link:
            message += f"📥 [LAUNCH PITCH ON WHATSAPP]({wa_link})\n"
        else:
            message += "📥 *WhatsApp:* No direct phone link uncovered.\n"

        message += (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🛡️ *Davies | Partner Lead Engine 2026*"
        )

        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }

        try:
            response = requests.post(self.telegram_url, json=payload, timeout=12)
            if response.status_code == 200:
                return True
            else:
                print(f"      ⚠️ Delivery issue: Telegram API returned code {response.status_code}")
                return False
        except Exception as e:
            print(f"      ❌ Transmission failure: {e}")
            return False

    def execute_dispatch_pipeline(self):
        """Processes the backlog queue and moves leads to finished status states."""
        db = self.load_database()
        if not db:
            return

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🛡️  DAVIES | PARTNER LEAD ENGINE 2026")
        print("🚀 Executing Script 5: Agency Card Telegram Dispatcher")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        dispatched_count = 0

        for lead in db:
            if lead.get("pipeline_status") == "PENDING_DISPATCH":
                name = lead["instructor_name"]
                print(f"📡 Transmitting Lead Card data to phone: [{name.upper()}]")
                
                # Send card to your Telegram Bot
                success = self.dispatch_lead_card(lead)
                
                if success:
                    # Update status to completely closed out
                    lead["pipeline_status"] = "COMPLETED"
                    dispatched_count += 1
                    print(f"   ↳ Status: Transmitted successfully.")
                else:
                    print(f"   ↳ Status: Delivery failed. Held in queue.")
                
                print("   -------------------------------------------------")
                time.sleep(2.0) # Rate-limit control window for Telegram API servers

        if dispatched_count > 0:
            # Commit status updates to prevent spam re-runs
            with open(DATABASE_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4, ensure_ascii=False)
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"✅ PIPELINE TRANSMISSION COMPLETE: Dispatched {dispatched_count} leads straight to your device.")
            print(f"📂 Status updates saved inside: `{DATABASE_FILE}`")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        else:
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("ℹ️  Pipeline Notice: No pending lead documents required transmission.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    engine = TelegramDispatcher()
    engine.execute_dispatch_pipeline()

