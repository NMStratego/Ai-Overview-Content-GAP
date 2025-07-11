import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Download, Trash2, Loader2, CheckCircle, AlertCircle, Globe, Clock, FileText, ExternalLink } from 'lucide-react';

interface AIOverviewData {
  query?: string;
  ai_overview?: string;
  full_content?: string;
  found?: boolean;
  extraction_time?: string;
  sources?: Array<{
    title: string;
    url: string;
  }>;
  timestamp?: string;
}

interface AIOverviewExtractorProps {
  onExtractionComplete: (data: AIOverviewData) => void;
  aiOverviewData: AIOverviewData | null;
  onClearAiOverview: () => void;
}

const AIOverviewExtractor: React.FC<AIOverviewExtractorProps> = ({
  onExtractionComplete,
  aiOverviewData,
  onClearAiOverview
}) => {
  const [query, setQuery] = useState('');
  const [isExtracting, setIsExtracting] = useState(false);
  const [extractionStatus, setExtractionStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [statusMessage, setStatusMessage] = useState('');

  // Funzione che chiama il backend Python (AIOverviewExtractor originale)
  const handleExtraction = async () => {
    if (!query.trim()) {
      setStatusMessage('Inserisci una query di ricerca');
      setExtractionStatus('error');
      return;
    }

    setIsExtracting(true);
    setExtractionStatus('idle');
    setStatusMessage('Estrazione AI Overview in corso...');

    try {
      // Chiama il backend Python reale con AIOverviewExtractor
      const response = await fetch('/api/extract-ai-overview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Errore nella chiamata API');
      }

      const result = await response.json();
      
      if (result.success && result.found) {
        onExtractionComplete(result);
        setExtractionStatus('success');
        setStatusMessage('AI Overview estratto con successo!');
      } else {
        setExtractionStatus('error');
        setStatusMessage(result.message || 'Nessun AI Overview trovato per questa query');
      }
      
    } catch (error) {

      console.error('Errore estrazione:', error);
      setExtractionStatus('error');
      setStatusMessage(`Errore durante l'estrazione: ${error.message}`);
    } finally {
      setIsExtracting(false);
    }
  };

  const downloadAiOverview = () => {
    if (!aiOverviewData) return;
    
    const dataStr = JSON.stringify(aiOverviewData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ai_overview_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8">
      {/* Header sezione */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <div className="glass-card rounded-2xl p-6 hover-lift">
          <h2 className="text-3xl font-bold gradient-text mb-4">
            🤖 Estrazione Intelligente AI Overview
          </h2>
          <p className="text-slate-600 text-lg max-w-3xl mx-auto">
            Estrai automaticamente i contenuti dall'AI Overview di Google per qualsiasi query di ricerca. 
            Il sistema utilizza automazione browser avanzata per ottenere il contenuto completo.
          </p>
        </div>
      </motion.div>

      {/* Form di ricerca */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card rounded-2xl p-6"
      >
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-3">
              🔍 Query di ricerca
            </label>
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Inserisci la tua query di ricerca..."
                className="input-modern w-full pl-12 pr-4 py-4 text-lg"
                onKeyPress={(e) => e.key === 'Enter' && !isExtracting && handleExtraction()}
                disabled={isExtracting}
              />
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleExtraction}
              disabled={isExtracting || !query.trim()}
              className="btn-primary flex-1 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isExtracting ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Estrazione in corso...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Estrai AI Overview
                </>
              )}
            </button>

            {aiOverviewData && (
              <button
                onClick={onClearAiOverview}
                className="btn-secondary flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Cancella
              </button>
            )}
          </div>

          {/* Status Message */}
          <AnimatePresence>
            {statusMessage && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className={`flex items-center gap-3 p-4 rounded-xl ${
                  extractionStatus === 'success' 
                    ? 'status-success' 
                    : extractionStatus === 'error' 
                    ? 'status-error' 
                    : 'bg-blue-50 border border-blue-200 text-blue-800'
                }`}
              >
                {extractionStatus === 'success' && <CheckCircle className="w-5 h-5" />}
                {extractionStatus === 'error' && <AlertCircle className="w-5 h-5" />}
                {extractionStatus === 'idle' && <Loader2 className="w-5 h-5 animate-spin" />}
                <span className="font-medium">{statusMessage}</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Risultati AI Overview */}
      <AnimatePresence>
        {aiOverviewData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-6"
          >
            {/* Header risultati */}
            <div className="glass-card rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-2xl font-bold gradient-text flex items-center gap-3">
                  <FileText className="w-6 h-6" />
                  Risultato AI Overview
                </h3>
                <button
                  onClick={downloadAiOverview}
                  className="btn-secondary flex items-center gap-2"
                >
                  <Download className="w-4 h-4" />
                  Scarica JSON
                </button>
              </div>

              {/* Query utilizzata */}
              <div className="bg-slate-50 rounded-xl p-4 mb-4">
                <div className="flex items-center gap-2 mb-2">
                  <Search className="w-4 h-4 text-slate-500" />
                  <span className="text-sm font-semibold text-slate-600">Query:</span>
                </div>
                <p className="text-lg font-medium text-slate-800">{aiOverviewData.query}</p>
              </div>

              {/* Timestamp */}
              {aiOverviewData.extraction_time && (
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <Clock className="w-4 h-4" />
                  <span>Estratto il: {aiOverviewData.extraction_time}</span>
                </div>
              )}
            </div>

            {/* Contenuto AI Overview */}
            <div className="glass-card rounded-2xl p-6">
              <h4 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Globe className="w-5 h-5 text-blue-600" />
                Contenuto AI Overview
              </h4>
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
                <p className="text-slate-700 leading-relaxed text-lg">
                  {aiOverviewData.full_content || aiOverviewData.ai_overview}
                </p>
              </div>
            </div>

            {/* Fonti */}
            {aiOverviewData.sources && aiOverviewData.sources.length > 0 && (
              <div className="glass-card rounded-2xl p-6">
                <h4 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
                  <ExternalLink className="w-5 h-5 text-purple-600" />
                  Fonti ({aiOverviewData.sources.length})
                </h4>
                <div className="space-y-3">
                  {aiOverviewData.sources.map((source, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-slate-200 hover:border-purple-300 transition-colors"
                    >
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                          <span className="text-purple-600 font-bold text-sm">{index + 1}</span>
                        </div>
                        <div className="flex-1">
                          <h5 className="font-semibold text-slate-800 mb-1">{source.title}</h5>
                          <a
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-purple-600 hover:text-purple-700 text-sm flex items-center gap-1 transition-colors"
                          >
                            {source.url}
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AIOverviewExtractor;