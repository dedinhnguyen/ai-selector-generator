"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Code, TerminalSquare, AlertCircle, Copy, Check } from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

interface SelectorResult {
  target: string;
  xpath: string;
  cssSelector: string;
  playwright: string;
  selenium: string;
  cypress: string;
  confidence: number;
}

interface GenerateResponse {
  status: string;
  error_message?: string;
  cleaned_html?: string;
  selectors?: SelectorResult;
  explanation?: string;
  confidence?: number;
}

export default function Home() {
  const [rawHtml, setRawHtml] = useState("");
  const [targetDesc, setTargetDesc] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [copied, setCopied] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!rawHtml.trim() || !targetDesc.trim()) return;
    
    setIsLoading(true);
    setResult(null);
    try {
      const res = await fetch("http://192.168.188.24:8080/api/v1/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          raw_html: rawHtml,
          target_description: targetDesc
        })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ status: "error", error_message: "Không thể kết nối Backend Server (Vui lòng bật uvicorn trước)." });
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <main className="min-h-screen p-6 md:p-12 lg:p-24 flex flex-col items-center">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-5xl space-y-8"
      >
        <div className="text-center space-y-4">
          <motion.div 
            initial={{ scale: 0.8 }} animate={{ scale: 1 }}
            className="inline-flex items-center justify-center p-4 rounded-full glass-panel mb-4"
          >
            <Code className="w-8 h-8 text-blue-400" />
          </motion.div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
            AI Selector Generator
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto text-lg">
            Dán HTML snippet vào đây, AI sẽ tự động phân tích và trích xuất locator xịn xò nhất cho Automation Testing.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          {/* Input Section */}
          <motion.div 
            className="glass-panel p-6 rounded-2xl space-y-6 flex flex-col"
            initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.1 }}
          >
            <div className="space-y-2 flex-grow">
              <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                <Code className="w-4 h-4" /> Raw HTML Snippet
              </label>
              <textarea 
                value={rawHtml}
                onChange={(e) => setRawHtml(e.target.value)}
                placeholder='<button id="login" class="btn btn-primary" data-testid="login-btn">Login</button>'
                className="w-full h-[250px] glass-input rounded-xl p-4 text-sm font-mono text-slate-300 resize-none transition-all"
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                <TerminalSquare className="w-4 h-4" /> Target Element
              </label>
              <input 
                type="text"
                value={targetDesc}
                onChange={(e) => setTargetDesc(e.target.value)}
                placeholder="VD: Nút Login / Input email"
                className="w-full glass-input rounded-xl p-4 text-sm text-slate-200 transition-all"
              />
            </div>

            <button 
              onClick={handleGenerate}
              disabled={isLoading || !rawHtml || !targetDesc}
              className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold py-4 px-6 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_20px_rgba(79,70,229,0.3)]"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                <Send className="w-5 h-5" />
              )}
              {isLoading ? "Đang phân tích..." : "Generate Selectors"}
            </button>
          </motion.div>

          {/* Output Section */}
          <motion.div 
            className="glass-panel p-6 rounded-2xl flex flex-col overflow-hidden h-full min-h-[500px]"
            initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}
          >
            <h3 className="text-lg font-semibold text-white mb-6 border-b border-white/10 pb-4">
              Kết quả & Đánh giá
            </h3>

            <div className="flex-grow overflow-y-auto pr-2 custom-scrollbar space-y-6">
              <AnimatePresence mode="wait">
                {!result && !isLoading && (
                  <motion.div 
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                    className="flex flex-col items-center justify-center h-full text-slate-500 space-y-4 pt-20"
                  >
                    <TerminalSquare className="w-12 h-12 opacity-20" />
                    <p>Kết quả locator sẽ xuất hiện tại đây...</p>
                  </motion.div>
                )}

                {isLoading && (
                  <motion.div 
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                    className="flex flex-col items-center justify-center h-full space-y-6 pt-20"
                  >
                    <div className="relative w-16 h-16">
                      <div className="absolute inset-0 rounded-full border-t-2 border-blue-500 animate-spin"></div>
                      <div className="absolute inset-2 rounded-full border-r-2 border-indigo-400 animate-spin" style={{ animationDirection: 'reverse' }}></div>
                      <div className="absolute inset-4 rounded-full border-b-2 border-emerald-400 animate-spin"></div>
                    </div>
                    <p className="text-slate-400 animate-pulse text-sm">LLM đang phân tích HTML và sinh xpath...</p>
                  </motion.div>
                )}

                {result && result.status === "error" && (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
                    className="bg-red-500/10 border border-red-500/20 p-4 rounded-xl text-red-400 flex gap-3"
                  >
                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold">Lỗi xảy ra</p>
                      <p className="text-sm mt-1">{result.error_message}</p>
                    </div>
                  </motion.div>
                )}

                {result && result.status === "success" && result.selectors && (
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                    className="space-y-6"
                  >
                    <div className="flex items-center justify-between">
                      <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-sm font-medium border border-emerald-500/20">
                        {result.selectors.target}
                      </span>
                      <span className="px-3 py-1 bg-blue-500/10 text-blue-400 rounded-full text-sm font-medium border border-blue-500/20">
                        Confidence: {(result.selectors.confidence * 100).toFixed(0)}%
                      </span>
                    </div>

                    <div className="space-y-4">
                      {["xpath", "cssSelector", "playwright", "cypress"].map((key) => (
                        <div key={key} className="space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                              {key === 'cssSelector' ? 'CSS' : key}
                            </span>
                            <button 
                              onClick={() => copyToClipboard(result.selectors![key as keyof SelectorResult] as string, key)}
                              className="text-slate-400 hover:text-white transition-colors p-1"
                              title="Copy to clipboard"
                            >
                              {copied === key ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                            </button>
                          </div>
                          <div className="rounded-lg overflow-hidden border border-white/5">
                            <SyntaxHighlighter 
                              language={key === "xpath" || key === "cssSelector" ? "markup" : "javascript"} 
                              style={vscDarkPlus}
                              customStyle={{ margin: 0, padding: '1rem', background: 'rgba(0,0,0,0.4)' }}
                            >
                              {result.selectors![key as keyof SelectorResult] as string}
                            </SyntaxHighlighter>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="mt-8 pt-6 border-t border-white/10">
                      <h4 className="text-sm font-semibold text-slate-300 mb-3 flex items-center gap-2">
                        <TerminalSquare className="w-4 h-4" /> Tại sao nên dùng locators này?
                      </h4>
                      <div className="text-sm text-slate-300 leading-relaxed bg-black/20 p-4 rounded-xl border border-white/5 whitespace-pre-wrap">
                        {result.explanation}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </main>
  );
}
