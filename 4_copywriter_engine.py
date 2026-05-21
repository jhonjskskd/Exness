import json
import urllib.parse
import os

DATABASE_FILE = "udemy_engine_db.json"

class CopywriterEngine:
    def __init__(self):
        pass

    def load_database(self):
        """Accesses the main enriched lead repository."""
        if not os.path.exists(DATABASE_FILE):
            print(f"❌ Error: Database File `{DATABASE_FILE}` not found.")
            return []
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Read Failure: Unable to parse database records: {e}")
            return []

    def build_custom_pitches(self, lead):
        """Injects metrics into advanced psychological templates based on performance standing."""
        name = lead["instructor_name"]
        topic = lead["market_niche"]
        students = lead["student_count"]
        rating = lead["star_rating"]
        pixel = lead["has_meta_pixel"]
        
        email_pitch = ""
        whatsapp_pitch = ""

        # --- BUCKET A: THE STRUGGLING CREATOR (Under 500 Students) ---
        if students < 500:
            lead_type = "STRUGGLING"
            
            # Email Script Drafting
            email_pitch = (
                f"Subject: Your {topic} course is a hidden gem (but hidden from Udemy search)\n\n"
                f"Hi {name},\n\n"
                f"I was looking through the {topic} category and came across your course. Your syllabus and "
                f"delivery style are fantastic—easily on par with creators holding 20k+ enrollments. However, I noticed "
                f"you currently have only {students} students enrolled.\n\n"
                f"Here is the harsh reality of Udemy's search matrix: it aggressively buries newer courses without massive review volumes "
                f"on page 10, killing your traffic. You've built a stellar product; letting it sit waiting for organic discovery is a losing game.\n\n"
                f"I build automated external lead funnels on LinkedIn and X to locate students actively searching for help with {topic} "
                f"and route them directly to your page via your 97% instructor coupons. This triggers the algorithm into pushing you up the ranks.\n\n"
                f"I've mapped out a quick 3-step blueprint to force outside traffic to your listing this week. Worth a 2-minute look if I send it over?\n\n"
                f"Best,\nDavies | Partner Engine"
            )
            
            # WhatsApp Script Drafting
            whatsapp_pitch = (
                f"Hi {name}, love your course content on Udemy! The production style is excellent, but the search system "
                f"is completely burying you on page 10 because you have only {students} students. I built a quick 3-step strategy to "
                f"inject outside buyers from X/LinkedIn straight to your course using your instructor coupons. Open to taking a look?"
            )

        # --- BUCKET B: THE ELITE CREATOR (5000+ Students or High Stars) ---
        else:
            lead_type = "ELITE"
            pixel_notice = ""
            
            # Dynamically adapt the pitch text if Script 3 caught a tracking deficit
            if pixel == "No":
                pixel_notice = "your landing page completely lacks a tracking pixel, meaning you lose hot student data daily."
            else:
                pixel_notice = "your social traffic pipelines aren't fully insulated outside of the Udemy environment."

            # Email Script Drafting
            email_pitch = (
                f"Subject: Quick note on your top-tier {topic} course (and the 63% revenue leak)\n\n"
                f"Hi {name},\n\n"
                f"I was analyzing top-performing assets in the {topic} ecosystem and went through your reviews. Brilliant work "
                f"on maintaining your high standing—it's rare to see students explicitly praising your material in 5-star feedback.\n\n"
                f"Because you are leading the market, I did a technical assessment of your off-platform footprint and spotted a major structural leak: "
                f"Right now, {pixel_notice} Worse, by staying entirely within Udemy's closed loop, you give up to 63% of your hard-earned revenue per sale to marketplace commissions.\n\n"
                f"Your top competitors are already establishing independent external pipelines on X and LinkedIn to recapture 100% of their traffic margins and secure their ranking status.\n\n"
                f"I build automated lead generation engines that capture these high-intent users on social platforms and bring them directly into your proprietary funnels.\n\n"
                f"I've mapped out a quick 3-step strategy to insulate your #1 spot and halt the platform tax. Open to seeing the text breakdown?\n\n"
                f"Best,\nDavies | Partner Engine"
            )
            
            # WhatsApp Script Drafting
            whatsapp_pitch = (
                f"Hi {name}, brilliant work leading the Udemy market for {topic}! I ran a quick assessment on your external layout "
                f"and noticed a massive revenue leak. Udemy is taking up to a 63% cut of your organic sales. I built an independent lead engine "
                f"concept for your course so you can keep 100% of your margins off-platform. Can I drop the 3-step breakdown here?"
            )

        return lead_type, email_pitch, whatsapp_pitch

    def run_copywriting_compiler(self):
        """Processes lead records and formats communication properties."""
        db = self.load_database()
        if not db:
            return

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("🛡️  DAVIES | PARTNER LEAD ENGINE 2026")
        print("🚀 Executing Script 4: Dynamic Copywriter AI Engine")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        compiled_count = 0

        for lead in db:
            if lead.get("pipeline_status") == "PENDING_COPYWRITING":
                name = lead["instructor_name"]
                print(f"📝 Compiling Conversion Scripts for: [{name.upper()}]")
                
                # Generate specific custom copy assets
                l_type, email_text, wa_text = self.build_custom_pitches(lead)
                
                # Append copy structures directly onto our dictionary record
                lead["instructor_segment"] = l_type
                lead["compiled_email_pitch"] = email_text
                
                # Encode text parameters perfectly for direct browser/WhatsApp deep linking actions
                encoded_wa_string = urllib.parse.quote(wa_text)
                target_phone = lead["whatsapp_number"]
                
                if target_phone != "Not Found":
                    # Build clean direct launching link
                    lead["whatsapp_launch_link"] = f"https://api.whatsapp.com/send?phone={target_phone.replace('+', '')}&text={encoded_wa_string}"
                else:
                    lead["whatsapp_launch_link"] = "No WhatsApp Number Available"

                # Advance status flag seamlessly to preparation delivery for Script 5
                lead["pipeline_status"] = "PENDING_DISPATCH"
                compiled_count += 1
                
                print(f"   ↳ Categorized Segment: {lead['instructor_segment']}")
                print(f"   ↳ WhatsApp Engine Hook: Compiled & Encoded")
                print(f"   ↳ Email Copy Block: Generated successfully")
                print("   -------------------------------------------------")

        if compiled_count > 0:
            # Save newly mapped text copies straight back into local storage database
            with open(DATABASE_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=4, ensure_ascii=False)
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"✅ SYSTEM SUCCESS: Tailored pitch letters compiled for {compiled_count} targets.")
            print(f"📂 Updated central matrix parameters locally in: `{DATABASE_FILE}`")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        else:
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("ℹ️  Pipeline Notice: No pending entries required copywriting assembly.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    engine = CopywriterEngine()
    engine.run_copywriting_compiler()
          
