#!/usr/bin/env python3
"""
Script principale che integra l'estrazione dell'AI Overview e l'analisi del content gap

Questo script combina le due funzioni principali:
1. Estrazione automatica dell'AI Overview da Google
2. Analisi del content gap confrontando articoli con l'AI Overview
"""

import sys
import json
import os
from ai_overview_extractor import AIOverviewExtractor
from content_gap_analyzer import ContentGapAnalyzer

def print_menu():
    """Stampa il menu principale"""
    print("\n" + "="*60)
    print("    AI OVERVIEW & CONTENT GAP ANALYZER")
    print("="*60)
    print("1. Estrai AI Overview da Google")
    print("2. Analizza Content Gap di un articolo")
    print("3. Analizza Content Gap di più articoli")
    print("4. Workflow completo (Estrai + Analizza)")
    print("5. Visualizza AI Overview salvato")
    print("0. Esci")
    print("="*60)

def extract_ai_overview():
    """Funzione per estrarre l'AI Overview"""
    print("\n--- ESTRAZIONE AI OVERVIEW ---")
    
    query = input("Inserisci la query di ricerca: ").strip()
    if not query:
        print("Query non valida!")
        return None
    
    headless = input("Eseguire in modalità headless? (y/n): ").lower().startswith('y')
    
    extractor = AIOverviewExtractor(headless=headless)
    
    try:
        print(f"\nEstraendo AI Overview per: '{query}'...")
        result = extractor.extract_ai_overview_from_query(query)
        
        if result:
            # Crea un oggetto compatibile per mantenere la compatibilità
            ai_overview_data = {
                "found": True,
                "text": result,
                "full_content": result,
                "expanded_text": ""
            }
            
            # Salva il risultato
            filename = "ai_overview_result.json"
            extractor.save_to_file(ai_overview_data, filename)
            
            print("\n✅ AI Overview estratto con successo!")
            print(f"📄 Salvato in: {filename}")
            print(f"📊 Lunghezza testo: {len(result)} caratteri")
            
            # Mostra un'anteprima
            preview = result[:300] + "..." if len(result) > 300 else result
            print(f"\n📋 Anteprima:\n{preview}")
            
            return ai_overview_data
        else:
            print("❌ AI Overview non trovato")
            return None
            
    except Exception as e:
        print(f"❌ Errore durante l'estrazione: {e}")
        return None
    finally:
        extractor.close()

def analyze_single_article():
    """Funzione per analizzare un singolo articolo"""
    print("\n--- ANALISI CONTENT GAP - SINGOLO ARTICOLO ---")
    
    # Verifica se esiste l'AI Overview
    if not os.path.exists("ai_overview_result.json"):
        print("❌ AI Overview non trovato. Esegui prima l'estrazione (opzione 1).")
        return
    
    url = input("Inserisci l'URL dell'articolo: ").strip()
    if not url:
        print("URL non valido!")
        return
    
    analyzer = ContentGapAnalyzer()
    
    try:
        # Carica l'AI Overview
        analyzer.load_ai_overview_from_file("ai_overview_result.json")
        
        print(f"\nAnalizzando: {url}...")
        result = analyzer.analyze_article_gap(url)
        
        if result['success']:
            # Salva il risultato
            filename = f"gap_analysis_{hash(url) % 10000}.json"
            analyzer.save_analysis_report(result, filename)
            
            print("\n✅ Analisi completata!")
            print(f"📄 Report salvato in: {filename}")
            
            # Mostra i risultati
            gap = result['gap_analysis']
            print(f"\n📊 RISULTATI:")
            print(f"   📰 Titolo: {result['title']}")
            print(f"   📝 Parole: {result['word_count']}")
            print(f"   📈 Copertura: {gap['coverage_percentage']}%")
            print(f"   ✅ Argomenti coperti: {len(gap['covered_topics'])}")
            print(f"   ⚠️  Parzialmente coperti: {len(gap['partially_covered'])}")
            print(f"   ❌ Argomenti mancanti: {len(gap['missing_topics'])}")
            
            if gap['missing_topics']:
                print(f"\n🔍 ARGOMENTI MANCANTI:")
                for i, topic in enumerate(gap['missing_topics'][:10], 1):
                    print(f"   {i}. {topic}")
                if len(gap['missing_topics']) > 10:
                    print(f"   ... e altri {len(gap['missing_topics']) - 10}")
            
            print(f"\n💡 RACCOMANDAZIONI:")
            for i, rec in enumerate(gap['recommendations'], 1):
                print(f"   {i}. {rec}")
                
        else:
            print(f"❌ Errore nell'analisi: {result['error']}")
            
    except Exception as e:
        print(f"❌ Errore durante l'analisi: {e}")

def analyze_multiple_articles():
    """Funzione per analizzare più articoli"""
    print("\n--- ANALISI CONTENT GAP - ARTICOLI MULTIPLI ---")
    
    # Verifica se esiste l'AI Overview
    if not os.path.exists("ai_overview_result.json"):
        print("❌ AI Overview non trovato. Esegui prima l'estrazione (opzione 1).")
        return
    
    print("Inserisci gli URL degli articoli (uno per riga, riga vuota per terminare):")
    urls = []
    while True:
        url = input(f"URL {len(urls) + 1}: ").strip()
        if not url:
            break
        urls.append(url)
    
    if not urls:
        print("Nessun URL inserito!")
        return
    
    analyzer = ContentGapAnalyzer()
    
    try:
        # Carica l'AI Overview
        analyzer.load_ai_overview_from_file("ai_overview_result.json")
        
        print(f"\nAnalizzando {len(urls)} articoli...")
        results = analyzer.analyze_multiple_articles(urls)
        
        # Salva il risultato
        filename = "multiple_gap_analysis.json"
        analyzer.save_analysis_report(results, filename)
        
        print("\n✅ Analisi completata!")
        print(f"📄 Report salvato in: {filename}")
        
        # Mostra il riassunto
        summary = results['summary']
        if 'error' not in summary:
            print(f"\n📊 RIASSUNTO:")
            print(f"   📰 Articoli analizzati: {summary['total_articles_analyzed']}")
            print(f"   📈 Copertura media: {summary['average_coverage_percentage']}%")
            
            if summary['most_common_missing_topics']:
                print(f"\n🔍 ARGOMENTI PIÙ COMUNEMENTE MANCANTI:")
                for topic, count in summary['most_common_missing_topics'][:5]:
                    print(f"   • {topic} (manca in {count} articoli)")
            
            if summary['articles_with_low_coverage']:
                print(f"\n⚠️  ARTICOLI CON BASSA COPERTURA (<50%):")
                for article in summary['articles_with_low_coverage']:
                    print(f"   • {article['coverage']}% - {article['url']}")
        else:
            print(f"❌ Errore nel riassunto: {summary['error']}")
            
    except Exception as e:
        print(f"❌ Errore durante l'analisi: {e}")

def complete_workflow():
    """Workflow completo: estrazione + analisi"""
    print("\n--- WORKFLOW COMPLETO ---")
    
    # Passo 1: Estrazione AI Overview
    print("\n🔄 PASSO 1: Estrazione AI Overview")
    ai_result = extract_ai_overview()
    
    if not ai_result or not ai_result["found"]:
        print("❌ Impossibile procedere senza AI Overview")
        return
    
    # Passo 2: Analisi articoli
    print("\n🔄 PASSO 2: Analisi Content Gap")
    choice = input("Analizzare un singolo articolo (1) o più articoli (2)? ").strip()
    
    if choice == "1":
        analyze_single_article()
    elif choice == "2":
        analyze_multiple_articles()
    else:
        print("Scelta non valida")

def view_saved_ai_overview():
    """Visualizza l'AI Overview salvato"""
    print("\n--- AI OVERVIEW SALVATO ---")
    
    try:
        with open("ai_overview_result.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if data.get('found', False):
            content = data.get('full_content', '')
            print(f"\n📄 Contenuto AI Overview ({len(content)} caratteri):")
            print("="*60)
            print(content)
            print("="*60)
        else:
            print("❌ AI Overview non trovato nel file")
            
    except FileNotFoundError:
        print("❌ File ai_overview_result.json non trovato")
    except Exception as e:
        print(f"❌ Errore nel leggere il file: {e}")

def main():
    """Funzione principale"""
    print("🚀 Benvenuto nel sistema AI Overview & Content Gap Analyzer!")
    
    while True:
        print_menu()
        
        try:
            choice = input("\nScegli un'opzione (0-5): ").strip()
            
            if choice == "0":
                print("👋 Arrivederci!")
                break
            elif choice == "1":
                extract_ai_overview()
            elif choice == "2":
                analyze_single_article()
            elif choice == "3":
                analyze_multiple_articles()
            elif choice == "4":
                complete_workflow()
            elif choice == "5":
                view_saved_ai_overview()
            else:
                print("❌ Opzione non valida. Riprova.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Operazione interrotta. Arrivederci!")
            break
        except Exception as e:
            print(f"❌ Errore inaspettato: {e}")
            input("Premi Invio per continuare...")

if __name__ == "__main__":
    main()