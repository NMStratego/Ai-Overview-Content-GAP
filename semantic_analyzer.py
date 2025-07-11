import google.generativeai as genai
import requests
import json
import time
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

class SemanticAnalyzer:
    """
    Analizzatore semantico avanzato che utilizza Google Gemini 2.5 Pro per migliorare
    l'accuratezza dell'analisi del content gap
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None, use_local_models: bool = True):
        """
        Inizializza l'analizzatore semantico con Google Gemini
        
        Args:
            gemini_api_key: Chiave API Google Gemini (opzionale, usa chiave integrata se None)
            use_local_models: Se utilizzare modelli locali per l'embedding
        """
        # Usa la chiave API integrata se non fornita
        self.gemini_api_key = gemini_api_key or "AIzaSyDXB8Lj2gamg7SEYmxvZ_uEs7JX3RKZ9yY"
        self.use_local_models = use_local_models
        
        # Configura logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Configura Google Gemini con chiave integrata
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-pro')
            self.logger.info("✅ Google Gemini 2.5 Pro configurato")
        except Exception as e:
            self.logger.error(f"❌ Errore nella configurazione di Gemini: {e}")
            self.model = None
    
    def get_embeddings_gemini(self, texts: List[str]) -> List[List[float]]:
        """
        Genera embeddings usando Google Gemini
        
        Args:
            texts: Lista di testi da convertire in embeddings
            
        Returns:
            Lista di embeddings
        """
        if not self.model:
            return []
        
        try:
            embeddings = []
            for text in texts:
                # Usa Gemini per generare embedding semantico
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                    task_type="semantic_similarity"
                )
                embeddings.append(result['embedding'])
            
            return embeddings
            
        except Exception as e:
            self.logger.error(f"❌ Errore nella generazione di embeddings Gemini: {e}")
            return []
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calcola la similarità semantica tra due testi usando Gemini
        
        Args:
            text1: Primo testo
            text2: Secondo testo
            
        Returns:
            Score di similarità (0-1)
        """
        if not self.model:
            return 0.0
        
        try:
            # Genera embeddings per entrambi i testi
            embeddings = self.get_embeddings_gemini([text1, text2])
            
            if len(embeddings) == 2:
                # Calcola similarità coseno
                similarity = cosine_similarity(
                    [embeddings[0]], [embeddings[1]]
                )[0][0]
                return max(0.0, min(1.0, similarity))
            
            return 0.0
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel calcolo della similarità: {e}")
            return 0.0
    
    def find_semantic_matches(self, target_topics: List[str], article_content: str, 
                            threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Trova corrispondenze semantiche tra argomenti target e contenuto articolo
        
        Args:
            target_topics: Lista di argomenti da cercare
            article_content: Contenuto dell'articolo
            threshold: Soglia di similarità minima
            
        Returns:
            Lista di corrispondenze semantiche
        """
        matches = []
        
        if not self.model:
            return matches
        
        try:
            # Dividi l'articolo in paragrafi
            paragraphs = [p.strip() for p in article_content.split('\n') if p.strip()]
            
            for topic in target_topics:
                best_match = {
                    'topic': topic,
                    'similarity': 0.0,
                    'matched_content': '',
                    'match_type': 'none'
                }
                
                # Cerca la migliore corrispondenza nei paragrafi
                for paragraph in paragraphs:
                    if len(paragraph) > 50:  # Solo paragrafi significativi
                        similarity = self.calculate_semantic_similarity(topic, paragraph)
                        
                        if similarity > best_match['similarity']:
                            best_match.update({
                                'similarity': similarity,
                                'matched_content': paragraph[:200] + '...',
                                'match_type': self._classify_match_type(similarity)
                            })
                
                if best_match['similarity'] >= threshold:
                    matches.append(best_match)
            
            return matches
            
        except Exception as e:
            self.logger.error(f"❌ Errore nella ricerca di corrispondenze semantiche: {e}")
            return []
    
    def _classify_match_type(self, similarity: float) -> str:
        """
        Classifica il tipo di corrispondenza basato sulla similarità
        
        Args:
            similarity: Score di similarità
            
        Returns:
            Tipo di corrispondenza
        """
        if similarity >= 0.9:
            return 'exact'
        elif similarity >= 0.7:
            return 'high'
        elif similarity >= 0.5:
            return 'medium'
        elif similarity >= 0.3:
            return 'low'
        else:
            return 'none'
    
    def analyze_topic_relevance(self, missing_topics: List[str], article_content: str) -> List[Dict[str, Any]]:
        """
        Analizza la rilevanza dei topic mancanti rispetto al contenuto dell'articolo
        
        Args:
            missing_topics: Lista di argomenti mancanti
            article_content: Contenuto dell'articolo
            
        Returns:
            Lista di topic con score di rilevanza
        """
        if not self.model:
            return [{'topic': topic, 'relevance_score': 0.5, 'priority': 'medium'} for topic in missing_topics]
        
        try:
            # Analizza ogni topic mancante
            analyzed_topics = []
            
            for topic in missing_topics:
                # Calcola similarità semantica con il contenuto
                similarity = self.calculate_semantic_similarity(topic, article_content[:1000])
                
                # Determina priorità basata sulla similarità
                if similarity > 0.7:
                    priority = 'high'
                elif similarity > 0.4:
                    priority = 'medium'
                else:
                    priority = 'low'
                
                analyzed_topics.append({
                    'topic': topic,
                    'relevance_score': round(similarity, 3),
                    'priority': priority
                })
            
            # Ordina per rilevanza
            analyzed_topics.sort(key=lambda x: x['relevance_score'], reverse=True)
            return analyzed_topics
            
        except Exception as e:
            self.logger.error(f"❌ Errore nell'analisi di rilevanza: {e}")
            return [{'topic': topic, 'relevance_score': 0.5, 'priority': 'medium'} for topic in missing_topics]
    
    def _calculate_priority(self, relevance_score: int) -> str:
        """
        Calcola la priorità basata sul punteggio di rilevanza
        
        Args:
            relevance_score: Punteggio di rilevanza (0-100)
            
        Returns:
            Livello di priorità
        """
        if relevance_score >= 80:
            return 'high'
        elif relevance_score >= 60:
            return 'medium'
        elif relevance_score >= 40:
            return 'low'
        else:
            return 'very_low'
    
    def generate_content_suggestions(self, missing_topics: List[str], 
                                   article_content: str, ai_overview_content: str = "") -> List[Dict[str, Any]]:
        """
        Genera suggerimenti di contenuto dettagliati per i topic mancanti
        
        Args:
            missing_topics: Lista di argomenti mancanti
            article_content: Contenuto dell'articolo esistente
            ai_overview_content: Contenuto dell'AI Overview per contesto
            
        Returns:
            Lista di suggerimenti dettagliati
        """
        if not self.model:
            return self._generate_basic_suggestions(missing_topics)
        
        try:
            suggestions = []
            
            # Genera un'analisi complessiva prima
            overview_prompt = f"""
            Analizza il seguente articolo e l'AI Overview per identificare i gap di contenuto più critici:
            
            ARTICOLO ESISTENTE:
            {article_content[:1200]}
            
            AI OVERVIEW DI RIFERIMENTO:
            {ai_overview_content[:800]}
            
            ARGOMENTI MANCANTI: {', '.join(missing_topics[:10])}
            
            Fornisci un'analisi strutturata in JSON con questo formato:
            {{
                "gap_analysis": "Breve analisi dei gap principali",
                "content_strategy": "Strategia generale per migliorare l'articolo",
                "priority_topics": ["topic1", "topic2", "topic3"]
            }}
            """
            
            overview_response = self.model.generate_content(overview_prompt)
            
            # Genera suggerimenti specifici per i topic più importanti
            for i, topic in enumerate(missing_topics[:8]):  # Aumentato a 8 topic
                prompt = f"""
                CONTESTO ARTICOLO:
                {article_content[:1000]}
                
                AI OVERVIEW RIFERIMENTO:
                {ai_overview_content[:600]}
                
                ARGOMENTO MANCANTE: "{topic}"
                
                Genera una raccomandazione dettagliata per aggiungere contenuto su questo argomento.
                
                La raccomandazione deve includere:
                1. **Cosa aggiungere**: Contenuto specifico da includere
                2. **Dove inserirlo**: Posizione suggerita nell'articolo
                3. **Come svilupparlo**: 2-3 punti chiave da trattare
                4. **Valore aggiunto**: Perché questo contenuto è importante
                
                Formato risposta:
                COSA: [descrizione specifica del contenuto]
                DOVE: [sezione suggerita]
                COME: [punti chiave da sviluppare]
                VALORE: [beneficio per il lettore]
                
                Massimo 150 parole totali.
                """
                
                response = self.model.generate_content(prompt)
                suggestion_text = response.text.strip()
                
                # Analizza rilevanza del topic
                relevance = self.calculate_semantic_similarity(topic, article_content[:1000])
                
                # Determina priorità basata su posizione e rilevanza
                if i < 3 or relevance > 0.7:
                    priority = 'alta'
                    impact = 'Alto impatto sulla completezza del contenuto'
                elif i < 6 or relevance > 0.5:
                    priority = 'media'
                    impact = 'Medio impatto sulla qualità del contenuto'
                else:
                    priority = 'bassa'
                    impact = 'Basso impatto, contenuto opzionale'
                
                suggestions.append({
                    'topic': topic,
                    'suggestion': suggestion_text,
                    'relevance_score': round(relevance, 3),
                    'priority': priority,
                    'impact': impact,
                    'type': 'critica' if i < 3 else 'strutturale' if i < 6 else 'generale'
                })
                
                # Pausa per evitare rate limiting
                time.sleep(0.5)
            
            # Ordina per priorità e rilevanza
            suggestions.sort(key=lambda x: (x['priority'] == 'alta', x['relevance_score']), reverse=True)
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"❌ Errore nella generazione suggerimenti: {e}")
            return self._generate_basic_suggestions(missing_topics)
    
    def _generate_basic_suggestions(self, missing_topics: List[str]) -> List[Dict[str, Any]]:
        """
        Genera suggerimenti di base quando Gemini non è disponibile
        
        Args:
            missing_topics: Lista di argomenti mancanti
            
        Returns:
            Lista di suggerimenti di base
        """
        suggestions = []
        
        for topic in missing_topics:
            suggestions.append({
                'topic': topic,
                'suggestion': f"Considera di aggiungere una sezione dedicata a '{topic}' per migliorare la completezza dell'articolo.",
                'relevance_score': 0.5,
                'priority': 'medium'
            })
        
        return suggestions
    
    def _categorize_topic(self, topic: str) -> str:
        """
        Categorizza un argomento
        
        Args:
            topic: Argomento da categorizzare
            
        Returns:
            Categoria dell'argomento
        """
        # Validazione del tipo di input
        if isinstance(topic, dict):
            topic = topic.get('topic', str(topic))
        elif not isinstance(topic, str):
            topic = str(topic)
            
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['come', 'guida', 'tutorial', 'passo']):
            return 'tutorial'
        elif any(word in topic_lower for word in ['cos\'è', 'definizione', 'significato']):
            return 'definizione'
        elif any(word in topic_lower for word in ['vantaggi', 'benefici', 'pro']):
            return 'vantaggi'
        elif any(word in topic_lower for word in ['esempio', 'caso', 'pratico']):
            return 'esempi'
        elif any(word in topic_lower for word in ['problema', 'errore', 'soluzione']):
            return 'problemi'
        else:
            return 'generale'
    
    def batch_similarity_analysis(self, topics: List[str], 
                                content_chunks: List[str]) -> Dict[str, Any]:
        """
        Esegue un'analisi di similarità in batch
        
        Args:
            topics: Lista di argomenti
            content_chunks: Lista di chunk di contenuto
            
        Returns:
            Risultati dell'analisi batch
        """
        if not self.model:
            return {}
        
        try:
            # Genera embeddings per tutti i topics e chunks
            all_texts = topics + content_chunks
            embeddings = self.get_embeddings_gemini(all_texts)
            
            if len(embeddings) != len(all_texts):
                return {}
            
            topic_embeddings = embeddings[:len(topics)]
            content_embeddings = embeddings[len(topics):]
            
            # Calcola matrice di similarità
            similarity_matrix = cosine_similarity(topic_embeddings, content_embeddings)
            
            results = {
                'similarity_matrix': similarity_matrix.tolist(),
                'topics': topics,
                'content_chunks': content_chunks,
                'best_matches': []
            }
            
            # Trova le migliori corrispondenze per ogni topic
            for i, topic in enumerate(topics):
                best_chunk_idx = np.argmax(similarity_matrix[i])
                best_similarity = similarity_matrix[i][best_chunk_idx]
                
                results['best_matches'].append({
                    'topic': topic,
                    'best_chunk': content_chunks[best_chunk_idx],
                    'similarity': float(best_similarity),
                    'match_type': self._classify_match_type(best_similarity)
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Errore nell'analisi batch: {e}")
            return {}
    
    def generate_content_suggestions(self, ai_overview_content: str, article_content: str, missing_topics: List[str]) -> str:
        """
        Genera suggerimenti personalizzati per migliorare il contenuto basandosi sull'AI Overview
        e sui topic mancanti identificati
        
        Args:
            ai_overview_content: Contenuto dell'AI Overview
            article_content: Contenuto dell'articolo analizzato
            missing_topics: Lista degli argomenti mancanti
            
        Returns:
            Suggerimenti personalizzati generati da Gemini AI
        """
        if not self.model:
            return "Gemini AI non disponibile per generare suggerimenti."
        
        try:
            # Limita il numero di topic mancanti per evitare prompt troppo lunghi
            limited_topics = missing_topics[:10] if len(missing_topics) > 10 else missing_topics
            
            prompt = f"""
            Sei un esperto SEO e content strategist. Analizza il seguente scenario:
            
            **AI OVERVIEW (contenuto di riferimento):**
            {ai_overview_content[:2000]}...
            
            **ARTICOLO ANALIZZATO (estratto):**
            {article_content[:1500]}...
            
            **ARGOMENTI MANCANTI IDENTIFICATI:**
            {', '.join(limited_topics)}
            
            Basandoti su questa analisi, fornisci suggerimenti specifici e actionable per migliorare l'articolo.
            I suggerimenti devono essere:
            
            1. **Specifici e pratici** - Non generici ma mirati agli argomenti mancanti
            2. **SEO-oriented** - Che migliorino il ranking e la visibilità
            3. **User-focused** - Che aggiungano valore reale per i lettori
            4. **Implementabili** - Con indicazioni concrete su come procedere
            
            Struttura la risposta in modo chiaro e professionale, evidenziando:
            - Le opportunità principali identificate
            - Suggerimenti specifici per ogni area di miglioramento
            - Raccomandazioni per l'ottimizzazione SEO
            - Strategie per colmare i gap di contenuto
            
            Rispondi in italiano e mantieni un tono professionale ma accessibile.
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "Non è stato possibile generare suggerimenti in questo momento."
                
        except Exception as e:
            self.logger.error(f"❌ Errore nella generazione di suggerimenti: {e}")
            return f"Errore nella generazione di suggerimenti: {str(e)}"