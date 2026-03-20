"use strict";

/** 
XAU/USD Premium Signal Bot
- Fetches 15m and 1h candles from Twelve Data
- Calculates EMA(21), EMA(50), EMA(200), RSI(14), ATR(14)
- Sends Telegram alerts when score passes threshold
- Temporary test message included
**/

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

let running = false;
let lastAlert = { direction: null, sentAt: 0 };

// --- Helpers ---
function sleep(ms) { return new Promise(res => setTimeout(res, ms)); }
function toNum(v) { const n = Number(v); return Number.isFinite(n) ? n : null; }
function mean(arr) { if (!arr.length) return null; return arr.reduce((a,b)=>a+b,0)/arr.length; }
function max(arr) { if (!arr.length) return null; return arr.reduce((a,b)=>a>b?a:b, arr[0]); }
function min(arr) { if (!arr.length) return null; return arr.reduce((a,b)=>a<b?a:b, arr[0]); }
function format(n,d=2){return Number.isFinite(n)?n.toFixed(d):"n/a";}

// --- Fetch Candles ---
async function fetchCandles(interval, outputsize=OUTPUT_SIZE){
  const url = new URL("https://api.twelvedata.com/time_series");
  url.searchParams.set("symbol", SYMBOL);
  url.searchParams.set("interval", interval);
  url.searchParams.set("outputsize", String(outputsize));
  url.searchParams.set("apikey", TWELVEDATA_API_KEY);

  const res = await fetch(url.toString());
  const json = await res.json();

  if (!res.ok || (json.status && json.status !== "ok")) throw new Error(json.message||json.code||"Twelve Data error");
  if (!Array.isArray(json.values) || json.values.length<60) throw new Error(`Not enough candles for ${interval}`);

  const candles = json.values.map(x=>({
    datetime:x.datetime,
    open:toNum(x.open),
    high:toNum(x.high),
    low:toNum(x.low),
    close:toNum(x.close),
    volume:x.volume===undefined?null:toNum(x.volume)
  })).filter(x=>[x.open,x.high,x.low,x.close].every(Number.isFinite));

  candles.sort((a,b)=>new Date(a.datetime)-new Date(b.datetime));
  return candles;
}

// --- EMA, RSI, ATR ---
function emaSeries(values, period){
  if(values.length<period) return [];
  const out=Array(values.length).fill(null);
  const k=2/(period+1);
  let seed=mean(values.slice(0,period));
  if(!Number.isFinite(seed)) return [];
  out[period-1]=seed;
  let prev=seed;
  for(let i=period;i<values.length;i++){prev=values[i]*k+prev*(1-k);out[i]=prev;}
  return out;
}

function rsiSeries(values,period=14){
  if(values.length<=period) return [];
  const out=Array(values.length).fill(null);
  let gain=0, loss=0;
  for(let i=1;i<=period;i++){
    const diff=values[i]-values[i-1];
    if(diff>=0) gain+=diff; else loss+=Math.abs(diff);
  }
  let avgGain=gain/period, avgLoss=loss/period;
  out[period]=avgLoss===0?100:100-100/(1+avgGain/avgLoss);
  for(let i=period+1;i<values.length;i++){
    const diff=values[i]-values[i-1];
    const curGain=diff>0?diff:0;
    const curLoss=diff<0?Math.abs(diff):0;
    avgGain=(avgGain*(period-1)+curGain)/period;
    avgLoss=(avgLoss*(period-1)+curLoss)/period;
    out[i]=avgLoss===0?100:100-100/(1+avgGain/avgLoss);
  }
  return out;
}

function atrSeries(candles,period=14){
  if(candles.length<=period) return [];
  const out=Array(candles.length).fill(null);
  const trs=[];
  for(let i=1;i<candles.length;i++){
    const cur=candles[i], prev=candles[i-1];
    trs.push(Math.max(cur.high-cur.low, Math.abs(cur.high-prev.close), Math.abs(cur.low-prev.close)));
  }
  let firstATR=mean(trs.slice(0,period));
  if(!Number.isFinite(firstATR)) return [];
  out[period]=firstATR;
  let prevATR=firstATR;
  for(let i=period+1;i<candles.length;i++){
    prevATR=(prevATR*(period-1)+trs[i-1])/period;
    out[i]=prevATR;
  }
  return out;
}

// --- Candlestick helpers ---
function isBullish(c){return c.close>c.open;}
function isBearish(c){return c.close<c.open;}
function bodySize(c){return Math.abs(c.close-c.open);}
function upperWick(c){return c.high-Math.max(c.open,c.close);}
function lowerWick(c){return Math.min(c.open,c.close)-c.low;}
function bullishEngulfing(p,c){return isBearish(p)&&isBullish(c)&&c.open<=p.close&&c.close>=p.open;}
function bearishEngulfing(p,c){return isBullish(p)&&isBearish(c)&&c.open>=p.close&&c.close<=p.open;}
function bullishPinBar(c){const body=bodySize(c), lw=lowerWick(c), uw=upperWick(c); return lw>=body*2&&uw<=body*1.1&&c.close>=(c.high+c.low)/2;}
function bearishPinBar(c){const body=bodySize(c), lw=lowerWick(c), uw=upperWick(c); return uw>=body*2&&lw<=body*1.1&&c.close<=(c.high+c.low)/2;}

// --- Analyze ---
function analyzeTimeframe(candles){
  const closes=candles.map(c=>c.close);
  const highs=candles.map(c=>c.high);
  const lows=candles.map(c=>c.low);
  const ema21=emaSeries(closes,21), ema50=emaSeries(closes,50), ema200=emaSeries(closes,200);
  const rsi14=rsiSeries(closes,14), atr14=atrSeries(candles,14);
  const i=candles.length-1, p=candles.length-2;
  const last=candles[i], prev=candles[p];
  return {
    last, prev, closes, highs, lows,
    ema21:ema21[i], ema50:ema50[i], ema200:ema200[i],
    rsi:rsi14[i], atr:atr14[i],
    trendBull:ema21[i]>ema50[i]&&ema50[i]>ema200[i],
    trendBear:ema21[i]<ema50[i]&&ema50[i]<ema200[i],
    slopeUp:ema21[i]>ema21[p],
    slopeDown:ema21[i]<ema21[p],
    recentHigh:max(highs.slice(-20)),
    recentLow:min(lows.slice(-20)),
    bullEngulf:bullishEngulfing(prev,last),
    bearEngulf:bearishEngulfing(prev,last),
    bullPin:bullishPinBar(last),
    bearPin:bearishPinBar(last),
  };
}

// --- Score & Signal ---
function scoreDirection(primary, confirm){
  let buy=0,sell=0,reasons=[];
  if(primary.trendBull){buy+=3; reasons.push("15m trend bullish");}
  if(primary.trendBear){sell+=3; reasons.push("15m trend bearish");}
  if(primary.slopeUp) buy+=1;
  if(primary.slopeDown) sell+=1;
  if(primary.rsi<=30) {buy+=2; reasons.push(`15m RSI oversold ${format(primary.rsi)}`);}
  else if(primary.rsi>=70) {sell+=2; reasons.push(`15m RSI overbought ${format(primary.rsi)}`);}
  if(primary.bullEngulf||primary.bullPin){buy+=2; reasons.push("Bullish candle pattern");}
  if(primary.bearEngulf||primary.bearPin){sell+=2; reasons.push("Bearish candle pattern");}
  if(primary.last.close-primary.recentLow<=primary.atr*0.45) buy+=1;
  if(primary.recentHigh-primary.last.close<=primary.atr*0.45) sell+=1;
  return {buy,sell,reasons};
}

function buildSignal(primary, confirm){
  const scored=scoreDirection(primary,confirm
