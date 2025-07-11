#!/usr/bin/env python3
"""
Backend Flask per AI Analyzer
Integra le funzioni Python originali con API REST
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sys
import traceback
from datetime import datetime

# Importa le classi originali
from ai_overview_extractor import AIOverviewExtractor
from content_gap_analyzer import ContentGapAnalyzer
from semantic_analyzer import SemanticAnalyzer

app = Flask(__name__)
CORS(app)

# Configurazione
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'

# Crea le cartelle se non esistono
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Istanze globali
extractor = None
analyzer = None
semantic_analyzer = None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'ai_overview_extractor': 'available',
            'content_gap_analyzer': 'available',
            'semantic_analyzer': 'available'
        }
    })

@app.route('/api/extract-ai-overview', methods=['POST'])
def extract_ai_overview():
    """
    Estrae AI Overview usando la classe AIOverviewExtractor originale
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        headless = data.get('headless', True)
        
        if not query:
            return jsonify({'error': 'Query richiesta'}), 400
        
        print(f"🔍 Estrazione AI Overview per: {query}")
        
        # Usa la classe originale AIOverviewExtractor
        global extractor
        extractor = AIOverviewExtractor(headless=headless)
        
        try:
            # Chiama il metodo originale
            result = extractor.extract_ai_overview_from_query(query)
            
            if result and result.get('found', False):
                # Salva il risultato usando il metodo originale
                filename = f"ai_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                filepath = os.path.join(RESULTS_FOLDER, filename)
                extractor.save_to_file(result, filepath)
                
                print(f"✅ AI Overview estratto e salvato: {filename}")
                
                return jsonify({
                    'success': True,
                    'found': True,
                    'query': query,
                    'ai_overview': result.get('text', ''),
                    'full_content': result.get('full_content', ''),
                    'expanded_text': result.get('expanded_text', ''),
                    'extraction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'filename': filename
                })
            else:
                return jsonify({
                    'success': True,
                    'found': False,
                    'message': 'Nessun AI Overview trovato per questa query'
                })
                
        finally:
            # Chiudi sempre l'extractor
            if extractor:
                extractor.close()
                
    except Exception as e:
        print(f"❌ Errore estrazione AI Overview: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/analyze-content-gap', methods=['POST'])
def analyze_content_gap():
    """
    Analizza content gap usando ContentGapAnalyzer originale
    """
    try:
        data = request.get_json()
        article_url = data.get('article_url', '')
        ai_overview_file = data.get('ai_overview_file', '')
        use_semantic = data.get('use_semantic_analysis', True)
        
        if not article_url:
            return jsonify({'error': 'URL articolo richiesto'}), 400
            
        print(f"📊 Analisi Content Gap per: {article_url}")
        
        # Usa la classe originale ContentGapAnalyzer
        global analyzer
        gemini_api_key = "AIzaSyDXB8Lj2gamg7SEYmxvZ_uEs7JX3RKZ9yY"  # API key integrata
        analyzer = ContentGapAnalyzer(
            gemini_api_key=gemini_api_key,
            use_semantic_analysis=use_semantic
        )
        
        # Carica AI Overview se fornito
        if ai_overview_file:
            ai_overview_path = os.path.join(RESULTS_FOLDER, ai_overview_file)
            if os.path.exists(ai_overview_path):
                analyzer.load_ai_overview_from_file(ai_overview_path)
            else:
                return jsonify({'error': f'File AI Overview non trovato: {ai_overview_file}'}), 404
        
        # Esegui l'analisi usando il metodo originale
        result = analyzer.analyze_article_gap(article_url)
        
        if result.get('success', False):
            # Salva il risultato
            filename = f"content_gap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(RESULTS_FOLDER, filename)
            analyzer.save_analysis_report(result, filepath)
            
            print(f"✅ Analisi completata e salvata: {filename}")
            
            return jsonify({
                'success': True,
                'result': result,
                'filename': filename
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Errore sconosciuto nell\'analisi')
            })
            
    except Exception as e:
        print(f"❌ Errore analisi content gap: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/semantic-chat', methods=['POST'])
def semantic_chat():
    """
    Chat semantica usando SemanticAnalyzer originale
    """
    try:
        data = request.get_json()
        question = data.get('question', '')
        ai_overview_content = data.get('ai_overview_content', '')
        chat_history = data.get('chat_history', [])
        
        if not question:
            return jsonify({'error': 'Domanda richiesta'}), 400
            
        print(f"💬 Chat semantica: {question[:50]}...")
        
        # Usa la classe originale SemanticAnalyzer
        global semantic_analyzer
        if not semantic_analyzer:
            gemini_api_key = "AIzaSyDXB8Lj2gamg7SEYmxvZ_uEs7JX3RKZ9yY"
            semantic_analyzer = SemanticAnalyzer(gemini_api_key=gemini_api_key)
        
        # Prepara il contesto
        context = ""
        if ai_overview_content:
            context = f"AI OVERVIEW:\n{ai_overview_content}\n\n"
        
        # Aggiungi cronologia chat
        if chat_history:
            context += "CRONOLOGIA CHAT:\n"
            for msg in chat_history[-5:]:  # Ultimi 5 messaggi
                role = "Utente" if msg['role'] == 'user' else "Assistant"
                context += f"{role}: {msg['content']}\n"
            context += "\n"
        
        # Genera risposta usando Gemini
        full_prompt = f"""Sei un esperto SEO e content strategist. Rispondi in modo professionale e dettagliato.

{context}DOMANDA: {question}

Fornisci una risposta completa e actionable in italiano:"""
        
        response = semantic_analyzer.model.generate_content(full_prompt)
        
        if response and response.text:
            return jsonify({
                'success': True,
                'response': response.text,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Nessuna risposta generata'
            })
            
    except Exception as e:
        print(f"❌ Errore chat semantica: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/files', methods=['GET'])
def list_files():
    """Lista i file disponibili"""
    try:
        files = []
        
        # Scansiona la cartella results
        if os.path.exists(RESULTS_FOLDER):
            for filename in os.listdir(RESULTS_FOLDER):
                if filename.endswith('.json'):
                    filepath = os.path.join(RESULTS_FOLDER, filename)
                    stat = os.stat(filepath)
                    
                    file_type = 'unknown'
                    if 'ai_overview' in filename:
                        file_type = 'ai_overview'
                    elif 'content_gap' in filename:
                        file_type = 'content_gap'
                    
                    files.append({
                        'name': filename,
                        'type': file_type,
                        'size': f"{stat.st_size / 1024:.1f} KB",
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
        
        return jsonify({
            'success': True,
            'files': files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/files/<filename>', methods=['GET'])
def get_file(filename):
    """Scarica un file specifico"""
    try:
        filepath = os.path.join(RESULTS_FOLDER, filename)
        if os.path.exists(filepath):
            return send_from_directory(RESULTS_FOLDER, filename)
        else:
            return jsonify({'error': 'File non trovato'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload di file JSON"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nessun file fornito'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nessun file selezionato'}), 400
        
        if file and file.filename.endswith('.json'):
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Valida il contenuto JSON
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                file_type = 'unknown'
                if 'ai_overview' in data or 'full_content' in data:
                    file_type = 'ai_overview'
                elif 'gap_analysis' in data:
                    file_type = 'content_gap'
                
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'type': file_type,
                    'message': f'File {filename} caricato con successo'
                })
                
            except json.JSONDecodeError:
                os.remove(filepath)  # Rimuovi file non valido
                return jsonify({'error': 'File JSON non valido'}), 400
        
        return jsonify({'error': 'Solo file JSON sono supportati'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Avvio AI Analyzer Backend...")
    print("📡 Server disponibile su: http://localhost:5000")
    print("🔧 Endpoints disponibili:")
    print("   - GET  /api/health")
    print("   - POST /api/extract-ai-overview")
    print("   - POST /api/analyze-content-gap")
    print("   - POST /api/semantic-chat")
    print("   - GET  /api/files")
    print("   - GET  /api/files/<filename>")
    print("   - POST /api/upload")
    
    app.run(debug=True, host='0.0.0.0', port=5000)