"""
ORQUOR Account Creator — Automatiza creación de cuentas sociales
Usa Playwright para controlar navegador Windows
"""
import asyncio
import json
import os
import time
from playwright.async_api import async_playwright

CREDS_FILE = r"C:\Users\frefe\OneDrive\Desktop\START UP\orquor\credenciales.txt"
EMAIL = "freddy@orquor.com"

# Cargar contraseñas
PASSWORDS = {}
if os.path.exists(CREDS_FILE):
    with open(CREDS_FILE, "r") as f:
        for line in f:
            if "LinkedIn" in line:
                PASSWORDS["linkedin"] = line.split("|")[-1].strip()
            elif "GitHub" in line:
                PASSWORDS["github"] = line.split("|")[-1].strip()
            elif "X/Twitter" in line:
                PASSWORDS["x"] = line.split("|")[-1].strip()

async def create_linkedin():
    """Crear cuenta LinkedIn personal + Company Page."""
    print("[LinkedIn] Starting signup...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 1. Crear cuenta personal primero
        await page.goto("https://www.linkedin.com/signup")
        await page.wait_for_timeout(3000)
        
        try:
            # Email
            email_input = await page.wait_for_selector("input[name='email-address']", timeout=5000)
            await email_input.fill(EMAIL)
            await page.wait_for_timeout(300)
            
            # Password
            pass_input = await page.query_selector("input[name='password']")
            if pass_input:
                await pass_input.fill(PASSWORDS.get("linkedin", "Orquor.2026!"))
            
            # Submit
            submit = await page.query_selector("button[type='submit']")
            if submit:
                await submit.click()
                await page.wait_for_timeout(3000)
            
            print("[LinkedIn] Signup submitted. Check email for verification.")
            await page.screenshot(path=r"C:\Users\frefe\OneDrive\Desktop\START UP\orquor\.linkedin_signup.png")
            
            # Mantener abierto para verificacion
            await asyncio.sleep(120)
            
        except Exception as e:
            print(f"[LinkedIn] Error: {e}")
            await page.screenshot(path=r"C:\Users\frefe\OneDrive\Desktop\START UP\orquor\.linkedin_error.png")
        
        await browser.close()

async def create_github():
    """Crear cuenta GitHub + Organization."""
    print("[GitHub] Starting...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Crear cuenta personal
        await page.goto("https://github.com/signup")
        await page.wait_for_timeout(3000)
        
        try:
            # Email
            email_input = await page.wait_for_selector("input[type='email']", timeout=5000)
            await email_input.fill(EMAIL)
            await page.wait_for_timeout(500)
            
            # Continue button
            continue_btn = await page.query_selector("button[type='submit']")
            if continue_btn:
                await continue_btn.click()
            
            print("[GitHub] Email submitted. Continue manually for captcha...")
            await page.screenshot(path=r"C:\Users\frefe\OneDrive\Desktop\START UP\orquor\.github_setup.png")
            
        except Exception as e:
            print(f"[GitHub] Error: {e}")
            await page.screenshot(path=r"C:\Users\frefe\OneDrive\Desktop\START UP\orquor\.github_error.png")
        
        # NO cerrar - mantener abierto para CAPTCHA
        print("[GitHub] Ventana abierta. Completa el CAPTCHA.")
        await asyncio.sleep(300)  # 5 min para completar

async def main():
    print("=== ORQUOR Account Creator ===")
    print(f"Email: {EMAIL}")
    print(f"Passwords loaded: {list(PASSWORDS.keys())}")
    
    # Ejecutar en orden
    await create_github()
    await create_linkedin()
    
    print("Done. Screenshots saved.")

if __name__ == "__main__":
    asyncio.run(main())
