"use strict";

const SYMBOL = process.env.SYMBOL || "XAU/USD";
const PRIMARY_INTERVAL = process.env.PRIMARY_INTERVAL || "15min";
const CONFIRM_INTERVAL = process.env.CONFIRM_INTERVAL || "1h";
const OUTPUT_SIZE = Number(process.env.OUTPUT_SIZE || 300);
const CHECK_EVERY_MINUTES = Number(process.env.CHECK_EVERY_MINUTES || 15);
const MIN_SCORE = Number(process.env.MIN_SCORE || 8);
const COOLDOWN_MINUTES = Number(process.env.COOLDOWN_MINUTES || 45);

const TWELVEDATA_API_KEY = process.env.TWELVEDATA_API_KEY;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;

if (!TWELVEDATA_API_KEY) throw new Error("Missing TWELVEDATA_API_KEY");
if (!TELEGRAM_BOT_TOKEN) throw new Error("Missing TELEGRAM_BOT_TOKEN");
if (!TELEGRAM_CHAT_ID) throw new Error("Missing TELEGRAM_CHAT_ID");

// --- rest of your bot code ---
