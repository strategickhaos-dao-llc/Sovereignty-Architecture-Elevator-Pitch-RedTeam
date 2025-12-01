from fastapi import FastAPI, Query, HTTPException
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio
import json, datetime, os

app = FastAPI(title="Sovereign Browser Node", description="Full stealth browsing behind this machine's unique Proton VPN IP")

def psyche_log(event: str, **kwargs):
    entry = {"timestamp": datetime.datetime.utcnow().isoformat() + "Z", "event": event, **kwargs}
    log_path = os.environ.get("LOG_PATH", "/logs/events.jsonl")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

async def sovereign_browse(url: str, instructions: str = "") -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        await stealth_async(context)  # undetectable
        page = await context.new_page()
        
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)  # let JS settle
            
            title = await page.title()
            screenshot = await page.screenshot(full_page=True)
            content = await page.content()
            
            result = {
                "url": url,
                "final_url": page.url,
                "title": title,
                "text_length": len(content),
                "screenshot_bytes": len(screenshot)
            }
            
            if instructions:
                # simple LLM-free extraction using instructions as CSS/XPath hints would go here
                # for now just return raw HTML snippet
                try:
                    result["extracted"] = await page.eval_on_selector("body", "el => el.innerText.substring(0, 10000)")
                except Exception:
                    result["extracted"] = ""
            
            return result
            
        finally:
            await browser.close()

@app.get("/browse")
async def browse(url: str = Query(...), instructions: str = ""):
    psyche_log("sovereign_browse", url=url, instructions=instructions[:100])
    try:
        result = await sovereign_browse(url, instructions)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/health")
async def health():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                page = await browser.new_page()
                await page.goto("https://api.ipify.org?format=text", timeout=10000)
                ip_text = await page.text_content("body")
                return {"status": "sovereign", "exit_ip": ip_text}
            except Exception:
                return {"status": "sovereign", "exit_ip": "unavailable"}
            finally:
                await browser.close()
    except Exception as e:
        return {"status": "error", "message": str(e)}
