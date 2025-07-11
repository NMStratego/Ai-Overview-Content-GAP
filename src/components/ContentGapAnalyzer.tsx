import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, Send, Upload, Download, Trash2, Bot, User, FileText, Sparkles, AlertCircle } from 'lucide-react';

interface AIOverviewData {
  query?: string;
  ai_overview?: string;
  full_content?: string;
  found?: boolean;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ContentGapAnalyzerProps {
  aiOverviewData: AIOverviewData | null;
  chatHistory: ChatMessage[];
  onChatMessage: (message: ChatMessage) => void;
  onClearChat: () => void;
  onAnalysisComplete: (data: any) => void;
}

const ContentGapAnalyzer: React.FC<ContentGapAnalyzerProps> = ({
  aiOverviewData,
  chatHistory,
  onChatMessage,
  onClearChat,
  onAnalysisComplete
}) => {
  const [userQuestion, setUserQuestion] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  // Funzione che chiama il backend Python (SemanticAnalyzer originale)
  const handleSendMessage = async () => {
    if (!userQuestion.trim()) return;

    const userMessage: ChatMessage = { role: 'user', content: userQuestion };
    onChatMessage(userMessage);
    setUserQuestion('');
    setIsAnalyzing(true);

    try {
      // Chiama il backend Python reale con SemanticAnalyzer
      const response = await fetch('http://localhost:5000/api/semantic-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userMessage.content,
          ai_overview_content: aiOverviewData?.full_content || aiOverviewData?.ai_overview,
          chat_history: chatHistory
        }),
      });

      if (!response.ok) {
        throw new Error('Errore nella chiamata API');
      }

      const result = await response.json();
      
      if (result.success) {
        const aiMessage: ChatMessage = { role: 'assistant', content: result.response };
        onChatMessage(aiMessage);
      } else {
        throw new Error(result.error || 'Errore nella risposta');
      }
      
    } catch (error) {
      console.error('Errore chat:', error);
      const aiMessage: ChatMessage = { 
        role: 'assistant', 
        content: `Mi dispiace, si è verificato un errore: ${error.message}. Assicurati che il backend Python sia in esecuzione.` 
      };
      onChatMessage(aiMessage);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/json') {
      setUploadedFile(file);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target?.result as string);
          if (data.ai_overview || data.full_content) {
            // Simula il caricamento dell'AI Overview
            const welcomeMessage: ChatMessage = {
              role: 'assistant',
              content: `Ho caricato l'AI Overview dal file "${file.name}". Contiene ${(data.ai_overview || data.full_content).split(' ').length} parole. Cosa vorresti sapere sull'analisi del content gap?`
            };
            onChatMessage(welcomeMessage);
          }
        } catch (error) {
          console.error('Errore nel parsing del file JSON:', error);
        }
      };
      reader.readAsText(file);
    }
  };

  const exportChat = () => {
    if (chatHistory.length === 0) return;
    
    const chatContent = chatHistory.map((msg, index) => 
      `${msg.role === 'user' ? '👤 Utente' : '🤖 AI Assistant'}: ${msg.content}`
    ).join('\n\n---\n\n');
    
    const fullContent = `# Conversazione Content Gap Analyzer\n\n**Data:** ${new Date().toLocaleString('it-IT')}\n\n${chatContent}`;
    
    const blob = new Blob([fullContent], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chat_content_gap_${new Date().toISOString().split('T')[0]}.md`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <div className="glass-card rounded-2xl p-6 hover-lift">
          <h2 className="text-3xl font-bold gradient-text mb-4">
            💬 Content Gap Analyzer
          </h2>
          <p className="text-slate-600 text-lg max-w-3xl mx-auto">
            Analizza il gap di contenuto con l'intelligenza artificiale avanzata. 
            Chat interattiva per insights approfonditi basati su Google Gemini AI.
          </p>
        </div>
      </motion.div>

      {/* File Upload */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card rounded-2xl p-6"
      >
        <h3 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
          <Upload className="w-5 h-5 text-blue-600" />
          Carica AI Overview JSON
        </h3>
        
        <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:border-blue-400 transition-colors">
          <input
            type="file"
            accept=".json"
            onChange={handleFileUpload}
            className="hidden"
            id="json-upload"
          />
          <label htmlFor="json-upload" className="cursor-pointer">
            <FileText className="w-12 h-12 text-slate-400 mx-auto mb-3" />
            <p className="text-slate-600 font-medium mb-2">
              Carica il file JSON con l'AI Overview estratto
            </p>
            <p className="text-sm text-slate-500">
              Clicca qui o trascina il file JSON per iniziare l'analisi
            </p>
          </label>
        </div>

        {uploadedFile && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800 font-medium">
              ✅ File caricato: {uploadedFile.name}
            </p>
          </div>
        )}

        {!aiOverviewData && (
          <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-amber-800 font-medium">AI Overview non caricato</p>
              <p className="text-amber-700 text-sm">
                Carica un file JSON con l'AI Overview per iniziare l'analisi del content gap.
              </p>
            </div>
          </div>
        )}
      </motion.div>

      {/* Chat Interface */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="glass-card rounded-2xl p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <MessageCircle className="w-5 h-5 text-purple-600" />
            Chat Interattiva
          </h3>
          
          <div className="flex gap-2">
            {chatHistory.length > 0 && (
              <>
                <button
                  onClick={exportChat}
                  className="btn-secondary flex items-center gap-2 text-sm"
                >
                  <Download className="w-4 h-4" />
                  Esporta
                </button>
                <button
                  onClick={onClearChat}
                  className="btn-secondary flex items-center gap-2 text-sm"
                >
                  <Trash2 className="w-4 h-4" />
                  Pulisci
                </button>
              </>
            )}
          </div>
        </div>

        {/* Chat History */}
        <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
          <AnimatePresence>
            {chatHistory.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex items-start gap-3 max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse' : ''}`}>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    message.role === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-purple-600 text-white'
                  }`}>
                    {message.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </div>
                  
                  <div className={`rounded-2xl p-4 ${
                    message.role === 'user'
                      ? 'chat-bubble-user'
                      : 'chat-bubble-ai'
                  }`}>
                    <div className="whitespace-pre-wrap text-sm leading-relaxed">
                      {message.content}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="flex items-start gap-3 max-w-[80%]">
                <div className="w-8 h-8 rounded-full bg-purple-600 text-white flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="chat-bubble-ai">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 animate-pulse" />
                    <span className="text-sm">Analizzando...</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Input Area */}
        <div className="space-y-4">
          <div className="relative">
            <textarea
              value={userQuestion}
              onChange={(e) => setUserQuestion(e.target.value)}
              placeholder="Fai una domanda sull'analisi del content gap..."
              className="input-modern w-full pr-12 py-4 resize-none"
              rows={3}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              disabled={isAnalyzing}
            />
            <button
              onClick={handleSendMessage}
              disabled={isAnalyzing || !userQuestion.trim()}
              className="absolute right-3 bottom-3 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          
          <div className="text-xs text-slate-500 text-center">
            Premi Enter per inviare, Shift+Enter per andare a capo
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ContentGapAnalyzer;