#!/usr/bin/env python3
"""
Funzione 2: Content Gap Analyzer

Questo script analizza gli articoli forniti tramite URL e li confronta con i contenuti
estratti dall'AI Overview per identificare quali argomenti mancano negli articoli.
"""

import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from difflib import SequenceMatcher
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string

# Download dei dati NLTK necessari (eseguire solo la prima volta)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ContentGapAnalyzer:
    def __init__(self):
        """
        Inizializza l'analizzatore di content gap
        """
        self.stop_words = set(stopwords.words('italian') + stopwords.words('english'))
        self.ai_overview_content = ""
        self.ai_overview_topics = []
        
    def load_ai_overview(self, ai_overview_text):
        """
        Carica il contenuto dell'AI Overview
        
        Args:
            ai_overview_text (str): Testo dell'AI Overview estratto
        """
        self.ai_overview_content = ai_overview_text
        self.ai_overview_topics = self.extract_topics(ai_overview_text)
        print(f"Caricati {len(self.ai_overview_topics)} argomenti dall'AI Overview")
    
    def load_ai_overview_from_file(self, filename):
        """
        Carica il contenuto dell'AI Overview da un file JSON
        
        Args:
            filename (str): Nome del file JSON contenente l'AI Overview
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('found', False):
                    self.load_ai_overview(data.get('full_content', ''))
                else:
                    print("AI Overview non trovato nel file")
        except Exception as e:
            print(f"Errore nel caricare il file AI Overview: {e}")
    
    def extract_article_content(self, url):
        """
        Estrae il contenuto testuale di un articolo da un URL
        
        Args:
            url (str): URL dell'articolo
            
        Returns:
            dict: Contenuto dell'articolo estratto
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Rimuovi script e style
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Estrai il titolo
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
            
            # Estrai il contenuto principale
            content = ""
            
            # Prova diversi selettori per il contenuto principale
            content_selectors = [
                'article',
                '.post-content',
                '.entry-content', 
                '.content',
                '.main-content',
                '#content',
                '.article-body',
                '.post-body',
                'main'
            ]
            
            content_element = None
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content_element = element
                    break
            
            if not content_element:
                # Se non trova selettori specifici, usa tutto il body
                content_element = soup.find('body')
            
            if content_element:
                # Estrai solo i paragrafi e gli heading
                paragraphs = content_element.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'success': True,
                'word_count': len(content.split())
            }
            
        except Exception as e:
            return {
                'url': url,
                'title': '',
                'content': '',
                'success': False,
                'error': str(e)
            }
    
    def extract_topics(self, text):
        """
        Estrae gli argomenti principali da un testo
        
        Args:
            text (str): Testo da analizzare
            
        Returns:
            list: Lista di argomenti/concetti chiave
        """
        if not text:
            return []
        
        # Pulisci il testo
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Tokenizza
        words = word_tokenize(text)
        
        # Rimuovi stopwords e parole troppo corte
        filtered_words = [
            word for word in words 
            if word not in self.stop_words 
            and len(word) > 2 
            and word.isalpha()
        ]
        
        # Conta le frequenze
        word_freq = Counter(filtered_words)
        
        # Estrai frasi chiave (bigrammi e trigrammi)
        sentences = sent_tokenize(text)
        key_phrases = []
        
        for sentence in sentences:
            # Cerca pattern specifici
            patterns = [
                r'\b(machine learning|deep learning|intelligenza artificiale|neural network|algoritmi|automazione)\b',
                r'\b(applicazioni|vantaggi|sfide|definizione|caratteristiche)\b',
                r'\b(sanità|trasporti|finanza|industria|robotica)\b'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, sentence.lower())
                key_phrases.extend(matches)
        
        # Combina parole frequenti e frasi chiave
        topics = []
        
        # Aggiungi le parole più frequenti
        for word, freq in word_freq.most_common(20):
            if freq > 1:  # Solo parole che appaiono più di una volta
                topics.append(word)
        
        # Aggiungi frasi chiave
        topics.extend(key_phrases)
        
        # Rimuovi duplicati mantenendo l'ordine
        seen = set()
        unique_topics = []
        for topic in topics:
            if topic not in seen:
                seen.add(topic)
                unique_topics.append(topic)
        
        return unique_topics
    
    def calculate_similarity(self, text1, text2):
        """
        Calcola la similarità tra due testi
        
        Args:
            text1 (str): Primo testo
            text2 (str): Secondo testo
            
        Returns:
            float: Valore di similarità tra 0 e 1
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def find_missing_topics(self, article_content):
        """
        Trova gli argomenti dell'AI Overview che mancano nell'articolo
        
        Args:
            article_content (str): Contenuto dell'articolo
            
        Returns:
            dict: Analisi dei gap di contenuto
        """
        if not self.ai_overview_content:
            return {'error': 'AI Overview non caricato'}
        
        article_topics = self.extract_topics(article_content)
        
        missing_topics = []
        covered_topics = []
        partially_covered = []
        
        for ai_topic in self.ai_overview_topics:
            found = False
            partial_match = False
            
            # Cerca corrispondenze esatte
            if ai_topic.lower() in article_content.lower():
                covered_topics.append(ai_topic)
                found = True
            else:
                # Cerca corrispondenze parziali
                for article_topic in article_topics:
                    similarity = self.calculate_similarity(ai_topic, article_topic)
                    if similarity > 0.7:  # Soglia di similarità
                        partially_covered.append({
                            'ai_topic': ai_topic,
                            'article_topic': article_topic,
                            'similarity': similarity
                        })
                        partial_match = True
                        break
            
            if not found and not partial_match:
                missing_topics.append(ai_topic)
        
        # Calcola statistiche
        total_ai_topics = len(self.ai_overview_topics)
        covered_count = len(covered_topics)
        partial_count = len(partially_covered)
        missing_count = len(missing_topics)
        
        coverage_percentage = ((covered_count + partial_count * 0.5) / total_ai_topics * 100) if total_ai_topics > 0 else 0
        
        return {
            'total_ai_topics': total_ai_topics,
            'covered_topics': covered_topics,
            'partially_covered': partially_covered,
            'missing_topics': missing_topics,
            'coverage_percentage': round(coverage_percentage, 2),
            'article_topics': article_topics[:10],  # Prime 10 per brevità
            'recommendations': self.generate_recommendations(missing_topics)
        }
    
    def generate_recommendations(self, missing_topics):
        """
        Genera raccomandazioni basate sugli argomenti mancanti
        
        Args:
            missing_topics (list): Lista degli argomenti mancanti
            
        Returns:
            list: Lista di raccomandazioni
        """
        recommendations = []
        
        # Categorizza gli argomenti mancanti
        categories = {
            'definizioni': ['definizione', 'intelligenza', 'artificiale', 'machine', 'learning', 'deep'],
            'applicazioni': ['applicazioni', 'sanità', 'trasporti', 'finanza', 'automazione', 'robotica'],
            'vantaggi': ['vantaggi', 'efficienza', 'precisione', 'innovazione'],
            'sfide': ['sfide', 'etica', 'sicurezza', 'lavoro', 'trasparenza']
        }
        
        for category, keywords in categories.items():
            missing_in_category = [topic for topic in missing_topics 
                                 if any(keyword in topic.lower() for keyword in keywords)]
            
            if missing_in_category:
                if category == 'definizioni':
                    recommendations.append(f"Aggiungi una sezione con definizioni chiare di: {', '.join(missing_in_category)}")
                elif category == 'applicazioni':
                    recommendations.append(f"Includi esempi di applicazioni pratiche: {', '.join(missing_in_category)}")
                elif category == 'vantaggi':
                    recommendations.append(f"Evidenzia i vantaggi: {', '.join(missing_in_category)}")
                elif category == 'sfide':
                    recommendations.append(f"Discuti le sfide e considerazioni etiche: {', '.join(missing_in_category)}")
        
        if not recommendations:
            recommendations.append("L'articolo copre bene gli argomenti principali dell'AI Overview")
        
        return recommendations
    
    def analyze_article_gap(self, article_url):
        """
        Analizza il gap di contenuto per un singolo articolo
        
        Args:
            article_url (str): URL dell'articolo da analizzare
            
        Returns:
            dict: Risultato completo dell'analisi
        """
        print(f"Analizzando articolo: {article_url}")
        
        # Estrai contenuto dell'articolo
        article_data = self.extract_article_content(article_url)
        
        if not article_data['success']:
            return {
                'url': article_url,
                'success': False,
                'error': article_data['error']
            }
        
        # Analizza i gap
        gap_analysis = self.find_missing_topics(article_data['content'])
        
        # Combina i risultati
        result = {
            'url': article_url,
            'title': article_data['title'],
            'word_count': article_data['word_count'],
            'success': True,
            'gap_analysis': gap_analysis
        }
        
        return result
    
    def analyze_multiple_articles(self, article_urls):
        """
        Analizza il gap di contenuto per più articoli
        
        Args:
            article_urls (list): Lista di URL degli articoli
            
        Returns:
            dict: Risultati dell'analisi per tutti gli articoli
        """
        results = []
        
        for url in article_urls:
            result = self.analyze_article_gap(url)
            results.append(result)
        
        # Genera un riassunto
        summary = self.generate_summary(results)
        
        return {
            'individual_results': results,
            'summary': summary
        }
    
    def generate_summary(self, results):
        """
        Genera un riassunto dell'analisi di più articoli
        
        Args:
            results (list): Lista dei risultati individuali
            
        Returns:
            dict: Riassunto dell'analisi
        """
        successful_analyses = [r for r in results if r.get('success', False)]
        
        if not successful_analyses:
            return {'error': 'Nessuna analisi riuscita'}
        
        # Calcola statistiche aggregate
        total_articles = len(successful_analyses)
        avg_coverage = sum(r['gap_analysis']['coverage_percentage'] for r in successful_analyses) / total_articles
        
        # Trova argomenti più comunemente mancanti
        all_missing = []
        for result in successful_analyses:
            all_missing.extend(result['gap_analysis']['missing_topics'])
        
        common_missing = Counter(all_missing).most_common(10)
        
        return {
            'total_articles_analyzed': total_articles,
            'average_coverage_percentage': round(avg_coverage, 2),
            'most_common_missing_topics': common_missing,
            'articles_with_low_coverage': [
                {'url': r['url'], 'coverage': r['gap_analysis']['coverage_percentage']} 
                for r in successful_analyses 
                if r['gap_analysis']['coverage_percentage'] < 50
            ]
        }
    
    def save_analysis_report(self, analysis_result, filename):
        """
        Salva il report dell'analisi in un file JSON
        
        Args:
            analysis_result (dict): Risultato dell'analisi
            filename (str): Nome del file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            print(f"Report salvato in: {filename}")
        except Exception as e:
            print(f"Errore nel salvare il report: {e}")


def main():
    """Funzione principale per testare l'analizzatore"""
    analyzer = ContentGapAnalyzer()
    
    # Carica l'AI Overview (assumendo che sia già stato estratto)
    try:
        analyzer.load_ai_overview_from_file("ai_overview_result.json")
    except:
        # Se il file non esiste, usa un contenuto di esempio
        sample_ai_overview = """
        L'intelligenza artificiale è un campo dell'informatica che si concentra sullo sviluppo di sistemi 
        capaci di simulare l'intelligenza umana. Include machine learning, deep learning, applicazioni 
        in sanità, trasporti, automazione. Presenta vantaggi come efficienza e precisione, ma anche 
        sfide etiche e di sicurezza.
        """
        analyzer.load_ai_overview(sample_ai_overview)
    
    # Esempio di analisi di un singolo articolo
    article_url = input("Inserisci l'URL dell'articolo da analizzare: ")
    
    if article_url:
        result = analyzer.analyze_article_gap(article_url)
        
        # Salva il risultato
        analyzer.save_analysis_report(result, "content_gap_analysis.json")
        
        # Stampa il risultato
        if result['success']:
            print("\n=== ANALISI CONTENT GAP ===")
            print(f"Titolo: {result['title']}")
            print(f"Copertura: {result['gap_analysis']['coverage_percentage']}%")
            print(f"Argomenti mancanti: {len(result['gap_analysis']['missing_topics'])}")
            print("\nRaccomandazioni:")
            for rec in result['gap_analysis']['recommendations']:
                print(f"- {rec}")
        else:
            print(f"Errore nell'analisi: {result['error']}")


if __name__ == "__main__":
    main()