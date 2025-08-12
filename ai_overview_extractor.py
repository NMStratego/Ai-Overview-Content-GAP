#!/usr/bin/env python3
"""
Funzione 1: Automatizzazione del browser per estrarre contenuti dall'AI Overview di Google

Questo script utilizza Playwright (2025) per automatizzare il browser, navigare su Google,
eseguire una ricerca e estrarre il contenuto dell'AI Overview incluso il testo
espanso dopo aver cliccato "Mostra altro".

Playwright è stato scelto come migliore soluzione per il 2025 rispetto a Selenium/Puppeteer
per la sua robustezza nella gestione dei popup e migliori performance.
"""

import time
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

class AIOverviewExtractor:
    def __init__(self, headless=False):
        """
        Inizializza l'estrattore AI Overview con Playwright (2025)
        
        Args:
            headless (bool): Se True, esegue il browser in modalità headless
        """
        self.browser = None
        self.page = None
        self.headless = headless
        self.playwright = None
        self.setup_browser()
    
    def setup_browser(self):
        """Configura Playwright con le migliori opzioni per gestire popup Google (2025) e fix per Windows"""
        try:
            print("🚀 Inizializzando Playwright (2025)...")
            print(f"📍 Sistema operativo: {os.name}")
            print(f"📍 Directory corrente: {os.getcwd()}")
            
            # Fix per Windows Python 3.13 - imposta event loop policy
            if os.name == 'nt':  # Windows
                import asyncio
                try:
                    # Prova a impostare WindowsProactorEventLoopPolicy
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                    print("✅ Event loop policy impostata per Windows")
                except Exception as policy_error:
                    print(f"⚠️ Avviso policy: {policy_error}")
                    # Fallback: crea nuovo event loop
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        print("✅ Nuovo event loop creato")
                    except Exception as loop_error:
                        print(f"⚠️ Avviso loop: {loop_error}")
            
            # Usa esclusivamente Playwright
            self.playwright = sync_playwright().start()
            print("✅ Playwright avviato con successo")
            self._setup_playwright_browser()
                
        except Exception as e:
            print(f"❌ Errore nell'inizializzazione Playwright: {e}")
            raise Exception(f"Impossibile inizializzare Playwright: {e}")
    
    def _setup_playwright_browser(self):
        """Setup specifico per Playwright"""
        # Opzioni browser ottimizzate per gestire popup di consenso Google
        browser_args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-extensions',
            '--disable-default-apps',
            '--disable-sync',
            '--disable-translate',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-field-trial-config',
            '--disable-back-forward-cache',
            '--disable-ipc-flooding-protection',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-popup-blocking',  # Importante per gestire popup
            '--disable-notifications',   # Disabilita notifiche
            '--disable-infobars',        # Disabilita barre info
            '--disable-save-password-bubble',  # Disabilita popup password
        ]
        
        # Avvia browser Chromium
        print("🌐 Avviando browser Chromium...")
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=browser_args
        )
        print("✅ Browser Chromium avviato con successo")
        
        # Crea contesto con impostazioni anti-rilevamento
        print("🔧 Creando contesto browser...")
        context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='it-IT',
            timezone_id='Europe/Rome',
            permissions=['geolocation'],  # Gestisce permessi automaticamente
            extra_http_headers={
                'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8'
            }
        )
        print("✅ Contesto browser creato")
        
        # Crea pagina
        print("📄 Creando nuova pagina...")
        self.page = context.new_page()
        print("✅ Pagina creata con successo")
        
        # Script anti-rilevamento
        self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['it-IT', 'it', 'en']});
            window.chrome = {runtime: {}};
        """)
        
        print("✅ Playwright configurato con successo")
        self.browser_type = 'playwright'
    

    
    def _wait_for_timeout(self, milliseconds):
        """Attende per il tempo specificato"""
        self.page.wait_for_timeout(milliseconds)
    
    def _find_element(self, selector):
        """Trova un elemento nella pagina"""
        return self.page.locator(selector)
    
    def _click_element(self, selector):
        """Clicca un elemento se visibile"""
        if self.page.locator(selector).count() > 0:
            element = self.page.locator(selector).first
            if element.is_visible():
                element.click()
                return True
        return False
    
    def _navigate_to(self, url):
        """Naviga a un URL"""
        self.page.goto(url, wait_until="domcontentloaded", timeout=10000)
    
    def _get_page_content(self):
        """Ottiene il contenuto della pagina"""
        return self.page.content()
    
    def _find_elements(self, selector):
        """Trova più elementi nella pagina"""
        return self.page.locator(selector)
    
    def _get_element_text(self, element):
        """Ottiene il testo di un elemento"""
        return element.inner_text()
    
    def handle_popups_and_captcha(self):
        """Gestisce popup di consenso Google con strategie avanzate 2025"""
        try:
            print("🔍 Ricerca popup di consenso Google...")
            
            # Attendi caricamento popup
            self._wait_for_timeout(3000)
            
            # Selettori aggiornati per popup Google 2025
            consent_selectors = [
                # Selettori principali Google 2025
                "button[id='L2AGLb']",  # "Accetta tutto" principale
                "button[aria-label*='Accept all']",
                "button[aria-label*='Accetta tutto']",
                "button[aria-label*='Accept']",
                "button[aria-label*='Accetta']",
                "div[role='button'][aria-label*='Accept']",
                "div[role='button'][aria-label*='Accetta']",
                
                # Selettori alternativi
                "button[data-ved]",
                "button:has-text('Accept all')",
                "button:has-text('Accetta tutto')",
                "button:has-text('I agree')",
                "button:has-text('Accetto')",
                "button:has-text('OK')",
                
                # Selettori per iframe di consenso
                "iframe[src*='consent'] button",
                "iframe[src*='cookiechoices'] button",
                
                # Selettori generici
                "[data-testid*='accept']",
                "[data-testid*='consent']",
                "button[class*='consent']",
                "button[class*='accept']"
            ]
            
            popup_closed = False
            
            # Prova ogni selettore
            for selector in consent_selectors:
                try:
                    # Usa metodo compatibile per cliccare
                    if self._click_element(selector):
                        print(f"✅ Popup chiuso con: {selector}")
                        popup_closed = True
                        break
                except Exception as e:
                    continue
            
            # Gestione iframe di consenso
            if not popup_closed:
                try:
                    # Cerca iframe di consenso
                    iframe_selectors = [
                        "iframe[src*='consent']",
                        "iframe[src*='cookiechoices']",
                        "iframe[name*='consent']"
                    ]
                    
                    for iframe_selector in iframe_selectors:
                        if self.page.locator(iframe_selector).count() > 0:
                            frame = self.page.frame_locator(iframe_selector)
                            # Cerca pulsanti nell'iframe
                            for btn_selector in ["button:has-text('Accept')", "button:has-text('OK')", "button[aria-label*='Accept']"]:
                                try:
                                    if frame.locator(btn_selector).count() > 0:
                                        frame.locator(btn_selector).first.click()
                                        print(f"✅ Popup iframe chiuso con: {btn_selector}")
                                        popup_closed = True
                                        break
                                except:
                                    continue
                            if popup_closed:
                                break
                except Exception as e:
                    print(f"Errore gestione iframe: {e}")
            
            # Gestione overlay/modal generici
            if not popup_closed:
                try:
                    overlay_selectors = [
                        "div[role='dialog'] button",
                        "div[class*='modal'] button",
                        "div[class*='overlay'] button",
                        "div[class*='popup'] button"
                    ]
                    
                    for overlay_sel in overlay_selectors:
                        if self.page.locator(overlay_sel).count() > 0:
                            buttons = self.page.locator(overlay_sel)
                            for i in range(buttons.count()):
                                btn = buttons.nth(i)
                                if btn.is_visible():
                                    text = btn.inner_text().lower()
                                    if any(word in text for word in ['accept', 'accetta', 'ok', 'agree']):
                                        btn.click()
                                        print(f"✅ Overlay chiuso: {text}")
                                        popup_closed = True
                                        break
                            if popup_closed:
                                break
                except Exception as e:
                    print(f"Errore gestione overlay: {e}")
            
            if popup_closed:
                self._wait_for_timeout(2000)  # Attendi chiusura
                print("✅ Popup di consenso gestito con successo")
            else:
                print("ℹ️ Nessun popup di consenso rilevato")
            
            # Gestione captcha
            try:
                if self.page.locator("iframe[src*='recaptcha']").count() > 0:
                    print("⚠️ Captcha rilevato. Attesa 10 secondi...")
                    self._wait_for_timeout(10000)
            except:
                pass
                
        except Exception as e:
            print(f"❌ Errore gestione popup: {e}")
    
    def search_google(self, query):
        """Esegue una ricerca su Google con Playwright e timeout robusti"""
        import time
        search_start = time.time()
        max_search_time = 20  # Timeout massimo per la ricerca
        
        try:
            print(f"🔍 Ricerca: {query}")
            print(f"⏰ Timeout ricerca: {max_search_time} secondi")
            
            # Naviga a Google con timeout
            try:
                self._navigate_to("https://www.google.com")
                print("✅ Navigazione a Google completata")
            except Exception as nav_error:
                print(f"❌ Errore navigazione: {nav_error}")
                return False
            
            # Controlla timeout
            if time.time() - search_start > max_search_time:
                print("⏰ Timeout durante navigazione")
                return False
            
            # Gestisci popup di consenso con timeout
            try:
                self.handle_popups_and_captcha()
                print("✅ Popup gestiti")
            except Exception as popup_error:
                print(f"⚠️ Errore gestione popup: {popup_error}")
                # Continua comunque
            
            # Controlla timeout
            if time.time() - search_start > max_search_time:
                print("⏰ Timeout dopo gestione popup")
                return False
            
            # Trova e compila il campo di ricerca
            search_selectors = [
                "input[name='q']",
                "textarea[name='q']",
                "input[title='Cerca']",
                "input[aria-label*='Cerca']",
                "input[role='combobox']"
            ]
            
            search_box = None
            found_selector = None
            for selector in search_selectors:
                try:
                    element = self._find_element(selector)
                    if element and element.is_visible():
                        search_box = element
                        found_selector = selector
                        print(f"✅ Campo ricerca trovato: {selector}")
                        break
                except Exception as selector_error:
                    print(f"⚠️ Errore selettore {selector}: {selector_error}")
                    continue
            
            if not search_box:
                print("❌ Campo di ricerca non trovato")
                return False
            
            # Controlla timeout
            if time.time() - search_start > max_search_time:
                print("⏰ Timeout durante ricerca campo")
                return False
            
            # Pulisci e inserisci la query
            try:
                search_box.clear()
                search_box.fill(query)
                search_box.press("Enter")
                print("✅ Query inviata")
            except Exception as input_error:
                print(f"❌ Errore inserimento query: {input_error}")
                return False
            
            # Attendi il caricamento dei risultati con timeout ridotto
            try:
                self.page.wait_for_selector("div[id='search']", timeout=10000)
                print("✅ Risultati caricati")
            except Exception as results_error:
                print(f"❌ Errore caricamento risultati: {results_error}")
                return False
            
            # Attendi che l'AI Overview si carichi se presente (timeout ridotto)
            self._wait_for_timeout(2000)
            
            search_duration = time.time() - search_start
            print(f"✅ Ricerca completata in {search_duration:.2f} secondi")
            return True
            
        except Exception as e:
            search_duration = time.time() - search_start
            print(f"❌ Errore durante la ricerca dopo {search_duration:.2f} secondi: {e}")
            return False
    
    def extract_ai_overview(self):
        """
        Estrae il contenuto dell'AI Overview dalla pagina dei risultati con Playwright e timeout robusti
        
        Returns:
            dict: Dizionario contenente il testo dell'AI Overview
        """
        import time
        start_time = time.time()  # Definizione di start_time per il finally
        extract_start = time.time()
        max_extract_time = 25  # Timeout massimo per l'estrazione completa
        timeout_seconds = max_extract_time  # Definizione di timeout_seconds per il controllo finale
        
        ai_overview_content = {
            "found": False,
            "text": "",
            "expanded_text": "",
            "full_content": ""
        }
        
        try:
            print("🤖 Ricerca AI Overview...")
            print(f"⏰ Timeout estrazione: {max_extract_time} secondi")
            
            # Selettori specifici per AI Overview aggiornati
            ai_overview_selectors = [
                ".LT6XE",
                ".QVRyCf",
                ".pyPiTc",
                ".rPeykc",
                ".EIJn2 :nth-child(1)",
                ".EIJn2 ul",
                "#m-x-content :nth-child(1)",
                "#_S7xvaILyI7Tq7_UP1_-T2A0_17+ .WaaZC .pyPiTc",
                ".RJPOee.EIJn2",
                "#m-x-content > div > div > div.RJPOee.mNfcNd > div > div > div > div:nth-child(1) > div > div > div.LT6XE > div > div:nth-child(1) > div:nth-child(22) > div > ul",
                "#m-x-content > div > div > div.RJPOee.mNfcNd > div > div > div > div:nth-child(1) > div > div > div.LT6XE > div > div:nth-child(1) > div:nth-child(21) > div > div",
                ".rPeykc.pyPiTc",
                "#m-x-content > div > div > div.RJPOee.mNfcNd > div > div > div > div:nth-child(1) > div > div > div.LT6XE > div > div:nth-child(1) > div:nth-child(1) > div > div",
                "#m-x-content > div > div > div.RJPOee.mNfcNd > div > div > div > div:nth-child(1) > div > div > div.LT6XE > div > div:nth-child(1) > div:nth-child(4) > div",
                "#m-x-content > div > div > div.RJPOee.mNfcNd > div > div > div > div:nth-child(1) > div > div > div.LT6XE > div > div:nth-child(1) > div:nth-child(3)",
                # Selettori aggiuntivi per catturare più contenuto
                "div[data-ved] p",
                "div[data-ved] span",
                "div[data-ved] div:has-text('AI')",
                "div[data-ved] div:has-text('intelligenza')",
                "[data-ved] .VwiC3b",
                "[data-ved] .hgKElc",
                "[data-ved] .LTKOO",
                "[data-ved] .sATSHe",
                "div.g div[data-ved]",
                "div.ULSxyf div[data-ved]"
            ]
            
            ai_overview_element = None
            found_selector = None
            
            # Prova diversi selettori per trovare l'AI Overview
            all_content = []
            seen_content = set()  # Per tracciare contenuto già visto
            
            def is_duplicate_content(new_text, existing_content):
                """Controlla se il nuovo testo è duplicato o contenuto in testi esistenti"""
                new_text_clean = new_text.lower().strip()
                
                # Controlla se il testo è identico
                if new_text_clean in seen_content:
                    return True
                
                # Controlla se il testo è contenuto in un testo esistente (>90% overlap)
                for existing in existing_content:
                    existing_clean = existing.lower().strip()
                    if len(new_text_clean) > 100 and len(existing_clean) > 100:
                        # Calcola sovrapposizione solo per testi molto lunghi
                        if new_text_clean in existing_clean or existing_clean in new_text_clean:
                            return True
                        
                        # Controlla similarità solo per frasi molto lunghe con soglia più alta
                        words_new = set(new_text_clean.split())
                        words_existing = set(existing_clean.split())
                        if len(words_new) > 20 and len(words_existing) > 20:
                            overlap = len(words_new.intersection(words_existing))
                            similarity = overlap / min(len(words_new), len(words_existing))
                            if similarity > 0.9:
                                return True
                
                return False
            
            for idx, selector in enumerate(ai_overview_selectors):
                # Controlla timeout ad ogni iterazione del selettore
                if time.time() - extract_start > max_extract_time:
                    print(f"⏰ Timeout durante ricerca selettore {idx+1}/{len(ai_overview_selectors)}")
                    break
                    
                try:
                    print(f"🔍 Testando selettore {idx+1}/{len(ai_overview_selectors)}: {selector[:50]}...")
                    
                    elements = self.page.locator(selector)
                    count = min(elements.count(), 10)  # Aumentato a 10 elementi per selettore
                    
                    if count > 0:
                        print(f"✅ Trovati {count} elementi con questo selettore")
                    
                    for i in range(count):
                        # Controlla timeout anche nel loop interno
                        if time.time() - extract_start > max_extract_time:
                            print("⏰ Timeout durante analisi elementi")
                            break
                            
                        try:
                            element = elements.nth(i)
                            if element.is_visible():  # Rimozione parametro timeout non supportato
                                text = element.inner_text().strip()
                                
                                # Raccoglie tutto il contenuto significativo con deduplicazione meno aggressiva
                                if (len(text) > 15 and 
                                    not is_duplicate_content(text, all_content) and
                                    # Esclude elementi di navigazione
                                    not any(nav_word in text.lower() for nav_word in [
                                        'search', 'images', 'videos', 'news', 'shopping',
                                        'maps', 'more', 'tools', 'settings', 'sign in'
                                    ])):
                                    
                                    all_content.append(text)
                                    seen_content.add(text.lower().strip())
                                    if not ai_overview_element:
                                        ai_overview_element = element
                                        found_selector = selector
                                        print(f"✅ Primo elemento AI Overview trovato: {len(text)} caratteri")
                                    
                                    # Aumentato il limite per catturare più contenuto
                                    if len(all_content) >= 20:
                                        print(f"📝 Raggiunto limite contenuti: {len(all_content)}")
                                        break
                        except Exception as element_error:
                            print(f"⚠️ Errore elemento {i}: {element_error}")
                            continue
                    
                    # Se abbiamo raggiunto il limite, usciamo dal loop principale
                    if len(all_content) >= 20:
                        break
                        
                except Exception as e:
                    print(f"⚠️ Errore selettore {selector[:50]}...: {e}")
                    continue
            
            # Se abbiamo raccolto contenuto da più elementi, lo combiniamo
            if all_content:
                combined_content = '\n\n'.join(all_content)
                print(f"✅ AI Overview trovato con {len(all_content)} elementi: {found_selector}")
                print(f"📝 Contenuto combinato: {len(combined_content)} caratteri")
                
                # Imposta il contenuto combinato ma continua per cercare espansioni
                ai_overview_content["found"] = True
                ai_overview_content["text"] = combined_content
                ai_overview_content["full_content"] = combined_content
                
                # Continua per cercare il pulsante "Mostra altro" se abbiamo un elemento principale
                if ai_overview_element:
                    print("🔍 Ricerca pulsante 'Mostra altro' per contenuto combinato...")
            
            # Ricerca alternativa per contenuti AI in iframe o shadow DOM
            if not ai_overview_element and time.time() - extract_start < max_extract_time:
                try:
                    print("🔍 Ricerca in iframe...")
                    # Cerca in iframe
                    iframe_selectors = ["iframe[src*='ai']", "iframe[src*='overview']"]
                    for iframe_sel in iframe_selectors:
                        # Controlla timeout
                        if time.time() - extract_start > max_extract_time:
                            print("⏰ Timeout durante ricerca iframe")
                            break
                            
                        if self.page.locator(iframe_sel).count() > 0:
                            frame = self.page.frame_locator(iframe_sel)
                            frame_content = frame.locator("body").inner_text()
                            if len(frame_content) > 50:
                                ai_content = frame_content
                                found_selector = f"iframe: {iframe_sel}"
                                print(f"✅ AI Overview trovato in iframe: {iframe_sel}")
                                return ai_content
                except Exception as e:
                    print(f"❌ Errore ricerca iframe: {e}")
                
                # Strategia di fallback: cerca elementi con molto testo
                if time.time() - extract_start < max_extract_time:
                    try:
                        print("🔍 Strategia fallback...")
                        fallback_selectors = [
                            "div[data-ved]:has-text('AI')",
                            "div[data-ved]:has-text('intelligenza')",
                            "div[data-ved]:has-text('artificial')",
                            "div[id='search'] div"
                        ]
                        
                        for fallback_sel in fallback_selectors:
                            # Controlla timeout
                            if time.time() - extract_start > max_extract_time:
                                print("⏰ Timeout durante strategia fallback")
                                break
                                
                            elements = self.page.locator(fallback_sel)
                            for i in range(min(elements.count(), 5)):  # Controlla solo i primi 5
                                # Controlla timeout anche nel loop interno
                                if time.time() - extract_start > max_extract_time:
                                    print("⏰ Timeout durante analisi fallback")
                                    break
                                    
                                element = elements.nth(i)
                                if element.is_visible():
                                    text = element.inner_text().strip()
                                    if len(text) > 100 and not text.startswith('http'):
                                        ai_overview_element = element
                                        found_selector = f"fallback: {fallback_sel}"
                                        print(f"✅ AI Overview trovato con fallback: {fallback_sel}")
                                        break
                            if ai_overview_element:
                                break
                    except Exception as e:
                        print(f"❌ Errore strategia fallback: {e}")
            
            if ai_overview_element:
                try:
                    # Estrai il testo dall'elemento
                    ai_text = ai_overview_element.inner_text().strip()
                    
                    if ai_text and len(ai_text) > 20:  # Verifica che ci sia contenuto significativo
                        print(f"✅ AI Overview estratto con: {found_selector}")
                        print(f"📝 Contenuto: {len(ai_text)} caratteri")
                        print(f"📄 Anteprima: {ai_text[:200]}...")
                        
                        ai_overview_content["found"] = True
                        ai_overview_content["text"] = ai_text
                    else:
                        print("⚠️ AI Overview trovato ma contenuto insufficiente")
                        
                except Exception as e:
                    print(f"❌ Errore nell'estrazione del testo: {e}")
                
                # Cerca il pulsante "Mostra altro" o "Show more" con Playwright
                try:
                    print("🔍 Ricerca pulsante 'Mostra altro'...")
                    
                    show_more_selectors = [
                        # Selettori aggiornati per "Mostra altro" (2025)
                        ".niO4u.VDgVie.SlP8xc",
                        "div.niO4u.VDgVie.SlP8xc",
                        "span.niO4u.VDgVie.SlP8xc",
                        "button.niO4u.VDgVie.SlP8xc",
                        "[class*='niO4u'][class*='VDgVie'][class*='SlP8xc']",
                        
                        # Selettori specifici per testo
                        "button:has-text('Mostra altro')",
                        "button:has-text('Show more')",
                        "span:has-text('Mostra altro')",
                        "span:has-text('Show more')",
                        "div:has-text('Mostra altro')",
                        "div:has-text('Show more')",
                        "a:has-text('Mostra altro')",
                        "a:has-text('Show more')",
                        
                        # Selettori con attributi role
                        "[role='button']:has-text('altro')",
                        "[role='button']:has-text('more')",
                        "[role='button']:has-text('Mostra')",
                        "[role='button']:has-text('Show')",
                        
                        # Selettori con aria-label
                        "button[aria-label*='Mostra']",
                        "button[aria-label*='Show']",
                        "button[aria-label*='more']",
                        "button[aria-label*='altro']",
                        "[aria-label*='Mostra altro']",
                        "[aria-label*='Show more']",
                        
                        # Selettori con data-ved
                        "[data-ved][role='button']",
                        "button[data-ved]",
                        "div[data-ved][role='button']",
                        "span[data-ved][role='button']",
                        
                        # Classi CSS specifiche Google
                        ".oHglmf",
                        ".GKS7yf",
                        ".pkphOe",
                        ".s75CSd",
                        ".CvDJxb",
                        ".RveJvd",
                        ".dmenKe",
                        ".CL9Uqc",
                        ".wHYlTd",
                        ".sATSHe",
                        
                        # Selettori generici per elementi cliccabili
                        "[onclick*='more']",
                        "[onclick*='altro']",
                        "[onclick*='expand']",
                        "[onclick*='espandi']"
                    ]
                    
                    show_more_button = None
                    
                    # Cerca il pulsante nell'elemento AI Overview
                    for selector in show_more_selectors:
                        try:
                            # Cerca prima nell'elemento AI Overview
                            buttons = ai_overview_element.locator(selector)
                            if buttons.count() > 0:
                                button = buttons.first
                                if button.is_visible():
                                    show_more_button = button
                                    print(f"✅ Pulsante 'Mostra altro' trovato: {selector}")
                                    break
                        except:
                            continue
                    
                    # Se non trovato nell'elemento, cerca nella pagina
                    if not show_more_button:
                        for selector in show_more_selectors:
                            try:
                                buttons = self.page.locator(selector)
                                if buttons.count() > 0:
                                    button = buttons.first
                                    if button.is_visible():
                                        show_more_button = button
                                        print(f"✅ Pulsante 'Mostra altro' trovato nella pagina: {selector}")
                                        break
                            except:
                                continue
                    
                    # Prova con XPath specifico se non trovato
                    if not show_more_button:
                        try:
                            xpath_selector = "//*[@id='_L5FvaJOBM43_7_UPgvGUsQ0_1']/div[1]/div/div[3]/div/div/div"
                            xpath_button = self.page.locator(f"xpath={xpath_selector}")
                            if xpath_button.count() > 0 and xpath_button.first.is_visible():
                                show_more_button = xpath_button.first
                                print(f"✅ Pulsante 'Mostra altro' trovato con XPath specifico")
                        except Exception as e:
                            print(f"⚠️ XPath specifico non funzionante: {e}")
                    
                    # Fallback: cerca qualsiasi elemento cliccabile con testo relativo
                    if not show_more_button:
                        try:
                            print("🔍 Ricerca fallback del pulsante 'Mostra altro'...")
                            fallback_selectors = [
                                "*:has-text('Mostra') >> visible=true",
                                "*:has-text('altro') >> visible=true",
                                "*:has-text('Show') >> visible=true",
                                "*:has-text('more') >> visible=true",
                                "[role='button'] >> visible=true",
                                "button >> visible=true",
                                "div[role='button'] >> visible=true",
                                "span[role='button'] >> visible=true",
                                "a >> visible=true"
                            ]
                            
                            for fallback in fallback_selectors:
                                try:
                                    elements = self.page.locator(fallback)
                                    count = elements.count()
                                    print(f"🔍 Controllando {count} elementi con selettore: {fallback}")
                                    
                                    for i in range(min(count, 5)):
                                        element = elements.nth(i)
                                        try:
                                            if element.is_visible():
                                                text = element.inner_text().lower().strip()
                                                print(f"📝 Testo elemento {i}: '{text[:50]}...'")
                                                
                                                # Controllo più preciso delle parole chiave
                                                keywords = ['mostra altro', 'show more', 'mostra', 'altro', 'show', 'more']
                                                if any(keyword in text for keyword in keywords):
                                                    # Verifica che l'elemento sia effettivamente cliccabile
                                                    if element.is_enabled():
                                                        show_more_button = element
                                                        print(f"✅ Pulsante trovato con fallback: {fallback} - Testo: '{text}'")
                                                        break
                                        except Exception as elem_e:
                                            print(f"⚠️ Errore controllo elemento {i}: {elem_e}")
                                            continue
                                    
                                    if show_more_button:
                                        break
                                except Exception as sel_e:
                                    print(f"⚠️ Errore con selettore {fallback}: {sel_e}")
                                    continue
                                    
                        except Exception as e:
                            print(f"⚠️ Fallback search failed: {e}")
                    
                    # Se trova il pulsante, cliccalo
                    if show_more_button:
                        try:
                            print("🖱️ Click su 'Mostra altro'...")
                            
                            # Strategia di click multipla per gestire elementi che intercettano
                            click_success = False
                            
                            # Tentativo 1: Click normale
                            try:
                                show_more_button.click(timeout=5000)
                                click_success = True
                                print("✅ Click normale riuscito")
                            except Exception as e1:
                                print(f"⚠️ Click normale fallito: {str(e1)[:100]}...")
                                
                                # Tentativo 2: Force click
                                try:
                                    show_more_button.click(force=True, timeout=5000)
                                    click_success = True
                                    print("✅ Force click riuscito")
                                except Exception as e2:
                                    print(f"⚠️ Force click fallito: {str(e2)[:100]}...")
                                    
                                    # Tentativo 3: JavaScript click
                                    try:
                                        show_more_button.evaluate("element => element.click()")
                                        click_success = True
                                        print("✅ JavaScript click riuscito")
                                    except Exception as e3:
                                        print(f"⚠️ JavaScript click fallito: {str(e3)[:100]}...")
                            
                            if click_success:
                                # Attendi che il contenuto si espanda
                                self.page.wait_for_timeout(3000)
                            else:
                                print("❌ Tutti i tentativi di click sono falliti")
                                ai_overview_content["full_content"] = ai_overview_content["text"]
                                return ai_overview_content
                            
                            # Estrai il contenuto espanso
                            expanded_text = ai_overview_element.inner_text().strip()
                            
                            # Confronto più intelligente per verificare l'espansione
                            # Usa il contenuto combinato originale invece del singolo elemento
                            original_combined = ai_overview_content["text"]
                            original_length = len(original_combined)
                            expanded_length = len(expanded_text)
                            length_increase = expanded_length - original_length
                            
                            # Utilizza sempre il contenuto più lungo tra quello originale combinato e quello espanso
                            if expanded_length > original_length:
                                ai_overview_content["expanded_text"] = expanded_text
                                ai_overview_content["full_content"] = expanded_text
                                print(f"✅ Contenuto espanso estratto: {expanded_length} caratteri (+{length_increase})")
                            else:
                                # Mantieni il contenuto combinato originale se è più lungo
                                ai_overview_content["full_content"] = original_combined
                                print(f"ℹ️ Mantenuto contenuto originale combinato: {original_length} caratteri (espanso: {expanded_length})")
                                
                        except Exception as e:
                            print(f"❌ Errore nel click 'Mostra altro': {e}")
                            ai_overview_content["full_content"] = ai_overview_content["text"]
                    else:
                        ai_overview_content["full_content"] = ai_overview_content["text"]
                        print("ℹ️ Pulsante 'Mostra altro' non trovato")
                        
                except Exception as e:
                    print(f"❌ Errore nella gestione 'Mostra altro': {e}")
                    ai_overview_content["full_content"] = ai_overview_content["text"]
            
            else:
                print("❌ AI Overview non trovato nella pagina")
                
        except Exception as e:
            print(f"❌ Errore durante l'estrazione dell'AI Overview: {e}")
        
        finally:
            # Log finale del tempo di esecuzione
            final_duration = time.time() - start_time
            print(f"⏱️ Estrazione AI Overview completata in {final_duration:.2f} secondi")
            
            # Controllo finale timeout
            if final_duration > timeout_seconds:
                print(f"⚠️ ATTENZIONE: Estrazione ha superato il timeout di {timeout_seconds}s")
        
        return ai_overview_content
    
    def extract_ai_overview_from_query(self, query):
        """
        Funzione principale che esegue la ricerca ed estrae l'AI Overview
        con gestione robusta per prevenire loop infiniti su Render
        
        Args:
            query (str): La query di ricerca
            
        Returns:
            str: Contenuto dell'AI Overview estratto o None se non trovato
        """
        import time
        start_time = time.time()
        max_execution_time = 45  # Timeout massimo di 45 secondi
        
        try:
            print(f"🔍 Ricerca di: {query}")
            print(f"⏰ Timeout impostato: {max_execution_time} secondi")
            
            # Controlla timeout prima della ricerca
            if time.time() - start_time > max_execution_time:
                raise TimeoutError("Timeout durante l'inizializzazione")
            
            # Esegui la ricerca con timeout
            print("🌐 Avvio ricerca Google...")
            search_start = time.time()
            
            if not self.search_google(query):
                print("❌ Ricerca fallita")
                return None
            
            search_duration = time.time() - search_start
            print(f"✅ Ricerca completata in {search_duration:.2f} secondi")
            
            # Controlla timeout prima dell'estrazione
            if time.time() - start_time > max_execution_time:
                raise TimeoutError("Timeout dopo la ricerca")
            
            print("🤖 Estrazione dell'AI Overview...")
            extraction_start = time.time()
            
            ai_content = self.extract_ai_overview()
            
            extraction_duration = time.time() - extraction_start
            total_duration = time.time() - start_time
            
            print(f"⏱️ Estrazione completata in {extraction_duration:.2f} secondi")
            print(f"⏱️ Tempo totale: {total_duration:.2f} secondi")
            
            if ai_content and ai_content.get('found', False):
                print("✅ AI Overview estratto con successo!")
                return ai_content
            else:
                print("❌ AI Overview non trovato")
                return None
            
        except TimeoutError as te:
            print(f"⏰ Timeout raggiunto: {te}")
            return None
            
        except Exception as e:
            print(f"❌ Errore durante l'estrazione: {e}")
            # Log dettagliato per debug su Render
            import traceback
            print(f"📋 Stack trace: {traceback.format_exc()}")
            return None
            
        finally:
            total_time = time.time() - start_time
            print(f"🏁 Processo completato in {total_time:.2f} secondi")
            
            # Forza garbage collection per liberare memoria
            import gc
            gc.collect()
    
    def save_to_file(self, content, filename):
        """
        Salva il contenuto estratto in un file JSON
        
        Args:
            content (dict): Contenuto da salvare
            filename (str): Nome del file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"Contenuto salvato in: {filename}")
        except Exception as e:
            print(f"Errore nel salvare il file: {e}")
    
    def close(self):
        """
        Chiude il browser e rilascia le risorse con gestione robusta per Render
        """
        try:
            print("🔒 Iniziando chiusura risorse browser...")
            
            # Chiudi la pagina
            if hasattr(self, 'page') and self.page:
                try:
                    self.page.close()
                    print("✅ Pagina chiusa")
                except Exception as e:
                    print(f"⚠️ Errore chiusura pagina: {e}")
                finally:
                    self.page = None
            
            # Chiudi il browser
            if hasattr(self, 'browser') and self.browser:
                try:
                    self.browser.close()
                    print("✅ Browser chiuso")
                except Exception as e:
                    print(f"⚠️ Errore chiusura browser: {e}")
                finally:
                    self.browser = None
            
            # Ferma Playwright
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    self.playwright.stop()
                    print("✅ Playwright fermato")
                except Exception as e:
                    print(f"⚠️ Errore stop Playwright: {e}")
                finally:
                    self.playwright = None
            
            print("🔒 Tutte le risorse browser rilasciate correttamente")
            
        except Exception as e:
            print(f"❌ Errore durante la chiusura: {e}")
            # Forza la pulizia delle variabili anche in caso di errore
            self.page = None
            self.browser = None
            self.playwright = None
            
        # Garbage collection forzato per Render
        import gc
        gc.collect()
        print("🧹 Garbage collection eseguito")


def main():
    """Funzione principale per testare l'estrattore"""
    extractor = AIOverviewExtractor(headless=False)
    
    try:
        # Query di test aggiornata per il 2025
        query = "migliori smartphone 2025"
        
        # Estrai l'AI Overview
        result = extractor.extract_ai_overview_from_query(query)
        
        # Salva il risultato
        if result:
            filename = f"ai_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            extractor.save_to_file(result, filename)
            print(f"📁 Risultato salvato in: {filename}")
            
            # Stampa il risultato
            print("\n=== CONTENUTO AI OVERVIEW ===")
            print(result)
        else:
            print("❌ Nessun AI Overview trovato")
        
    finally:
        extractor.close()


if __name__ == "__main__":
    main()