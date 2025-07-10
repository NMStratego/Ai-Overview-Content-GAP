#!/usr/bin/env python3
"""
Script di esempio per dimostrare l'utilizzo del sistema AI Overview & Content Gap Analyzer

Questo script mostra come utilizzare le funzioni principali in modo programmatico.
"""

import time
import json
from ai_overview_extractor import AIOverviewExtractor
from content_gap_analyzer import ContentGapAnalyzer

def esempio_estrazione_ai_overview():
    """
    Esempio di estrazione dell'AI Overview
    """
    print("\n" + "="*60)
    print("ESEMPIO 1: ESTRAZIONE AI OVERVIEW")
    print("="*60)
    
    # Query di esempio
    query = "machine learning"
    print(f"Query di ricerca: {query}")
    
    # Inizializza l'estrattore (modalità headless per velocità)
    extractor = AIOverviewExtractor(headless=True)
    
    try:
        print("\n🔄 Avvio estrazione...")
        start_time = time.time()
        
        # Estrai l'AI Overview
        result = extractor.extract_ai_overview_from_query(query)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        if result:
            print(f"✅ Estrazione completata in {duration} secondi")
            print(f"📄 Lunghezza contenuto: {len(result)} caratteri")
            
            # Crea un oggetto compatibile per mantenere la compatibilità
            ai_overview_data = {
                "found": True,
                "text": result,
                "full_content": result,
                "expanded_text": ""
            }
            
            # Salva il risultato
            filename = "esempio_ai_overview.json"
            extractor.save_to_file(ai_overview_data, filename)
            
            # Mostra anteprima
            preview = result[:200] + "..." if len(result) > 200 else result
            print(f"\n📋 Anteprima contenuto:\n{preview}")
            
            return ai_overview_data
        else:
            print(f"❌ AI Overview non trovato per la query: {query}")
            return None
            
    except Exception as e:
        print(f"❌ Errore durante l'estrazione: {e}")
        return None
    finally:
        extractor.close()

def esempio_analisi_content_gap():
    """
    Esempio di analisi del content gap
    """
    print("\n" + "="*60)
    print("ESEMPIO 2: ANALISI CONTENT GAP")
    print("="*60)
    
    # URL di esempio (sostituisci con URL reali)
    test_urls = [
        "https://it.wikipedia.org/wiki/Apprendimento_automatico",
        "https://www.ibm.com/it-it/topics/machine-learning"
    ]
    
    # Inizializza l'analizzatore
    analyzer = ContentGapAnalyzer()
    
    try:
        # Carica l'AI Overview (se disponibile)
        try:
            analyzer.load_ai_overview_from_file("esempio_ai_overview.json")
            print("✅ AI Overview caricato")
        except:
            # Se non disponibile, usa contenuto di esempio
            sample_content = """
            Il machine learning è una branca dell'intelligenza artificiale che si concentra 
            sullo sviluppo di algoritmi che permettono ai computer di apprendere dai dati. 
            Include tecniche come supervised learning, unsupervised learning, deep learning, 
            neural networks. Le applicazioni includono riconoscimento immagini, 
            elaborazione linguaggio naturale, sistemi di raccomandazione, veicoli autonomi.
            I vantaggi includono automazione, precisione, scalabilità. Le sfide includono 
            bias nei dati, interpretabilità, privacy, sicurezza.
            """
            analyzer.load_ai_overview(sample_content)
            print("✅ Contenuto AI Overview di esempio caricato")
        
        print(f"\n🔄 Analisi di {len(test_urls)} articoli...")
        
        # Analizza ogni URL
        for i, url in enumerate(test_urls, 1):
            print(f"\n--- Articolo {i}: {url} ---")
            
            start_time = time.time()
            result = analyzer.analyze_article_gap(url)
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            if result['success']:
                gap = result['gap_analysis']
                print(f"✅ Analisi completata in {duration} secondi")
                print(f"📰 Titolo: {result['title'][:50]}...")
                print(f"📝 Parole: {result['word_count']}")
                print(f"📈 Copertura: {gap['coverage_percentage']}%")
                print(f"✅ Argomenti coperti: {len(gap['covered_topics'])}")
                print(f"❌ Argomenti mancanti: {len(gap['missing_topics'])}")
                
                if gap['missing_topics']:
                    print(f"🔍 Primi 3 argomenti mancanti:")
                    for j, topic in enumerate(gap['missing_topics'][:3], 1):
                        print(f"   {j}. {topic}")
                
                print(f"💡 Prima raccomandazione: {gap['recommendations'][0] if gap['recommendations'] else 'Nessuna'}")
                
            else:
                print(f"❌ Errore nell'analisi: {result['error']}")
        
        # Analisi multipla
        print(f"\n🔄 Analisi comparativa...")
        multi_result = analyzer.analyze_multiple_articles(test_urls)
        
        if 'summary' in multi_result and 'error' not in multi_result['summary']:
            summary = multi_result['summary']
            print(f"\n📊 RIASSUNTO COMPARATIVO:")
            print(f"   📰 Articoli analizzati: {summary['total_articles_analyzed']}")
            print(f"   📈 Copertura media: {summary['average_coverage_percentage']}%")
            
            if summary['most_common_missing_topics']:
                print(f"\n🔍 Argomenti più comunemente mancanti:")
                for topic, count in summary['most_common_missing_topics'][:3]:
                    print(f"   • {topic} (manca in {count} articoli)")
        
        # Salva il report
        analyzer.save_analysis_report(multi_result, "esempio_gap_analysis.json")
        print(f"\n💾 Report salvato in: esempio_gap_analysis.json")
        
    except Exception as e:
        print(f"❌ Errore durante l'analisi: {e}")

def esempio_workflow_completo():
    """
    Esempio di workflow completo
    """
    print("\n" + "="*60)
    print("ESEMPIO 3: WORKFLOW COMPLETO")
    print("="*60)
    
    # Passo 1: Estrazione AI Overview
    print("\n🔄 PASSO 1: Estrazione AI Overview")
    ai_result = esempio_estrazione_ai_overview()
    
    if ai_result and ai_result["found"]:
        # Passo 2: Analisi Content Gap
        print("\n🔄 PASSO 2: Analisi Content Gap")
        esempio_analisi_content_gap()
        
        print("\n✅ Workflow completo terminato con successo!")
    else:
        print("\n❌ Workflow interrotto: impossibile estrarre AI Overview")

def esempio_personalizzato():
    """
    Esempio con parametri personalizzati
    """
    print("\n" + "="*60)
    print("ESEMPIO 4: CONFIGURAZIONE PERSONALIZZATA")
    print("="*60)
    
    # Configurazione personalizzata per l'estrattore
    print("\n🔧 Configurazione estrattore personalizzata...")
    
    extractor = AIOverviewExtractor(headless=False)  # Modalità visibile per debug
    
    try:
        # Query più specifica
        query = "deep learning neural networks"
        print(f"Query specifica: {query}")
        
        result = extractor.extract_ai_overview_from_query(query)
        
        if result:
            print("✅ Estrazione con configurazione personalizzata riuscita")
            
            # Analisi personalizzata
            analyzer = ContentGapAnalyzer()
            analyzer.load_ai_overview(result)
            
            # URL di test specifico
            test_url = "https://it.wikipedia.org/wiki/Rete_neurale_artificiale"
            analysis = analyzer.analyze_article_gap(test_url)
            
            if analysis['success']:
                print(f"\n📊 Analisi personalizzata completata:")
                print(f"   Copertura: {analysis['gap_analysis']['coverage_percentage']}%")
                print(f"   Raccomandazioni: {len(analysis['gap_analysis']['recommendations'])}")
        
    except Exception as e:
        print(f"❌ Errore nell'esempio personalizzato: {e}")
    finally:
        extractor.close()

def main():
    """
    Funzione principale che esegue tutti gli esempi
    """
    print("🚀 ESEMPI DI UTILIZZO - AI OVERVIEW & CONTENT GAP ANALYZER")
    print("\nQuesti esempi dimostrano come utilizzare il sistema programmaticamente.")
    print("\n⚠️  NOTA: Gli esempi utilizzano URL reali e richiedono connessione internet.")
    
    try:
        # Esempio 1: Solo estrazione
        esempio_estrazione_ai_overview()
        
        # Pausa tra esempi
        input("\n⏸️  Premi Invio per continuare con l'esempio di analisi...")
        
        # Esempio 2: Solo analisi
        esempio_analisi_content_gap()
        
        # Pausa tra esempi
        input("\n⏸️  Premi Invio per continuare con il workflow completo...")
        
        # Esempio 3: Workflow completo
        esempio_workflow_completo()
        
        # Esempio 4: Configurazione personalizzata
        risposta = input("\n❓ Vuoi eseguire l'esempio con configurazione personalizzata? (y/n): ")
        if risposta.lower().startswith('y'):
            esempio_personalizzato()
        
        print("\n🎉 Tutti gli esempi completati!")
        print("\n📁 File generati:")
        print("   • esempio_ai_overview.json")
        print("   • esempio_gap_analysis.json")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Esempi interrotti dall'utente")
    except Exception as e:
        print(f"\n❌ Errore negli esempi: {e}")

if __name__ == "__main__":
    main()