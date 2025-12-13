"use client";
import { useState } from "react";
import axios from "axios";
import { UploadCloud, Sparkles, Image as ImageIcon, Zap, Lock, Info } from "lucide-react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFile = (e) => {
    const f = e.target.files[0];
    if (f) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResult(null);
    }
  };

  const handleColorize = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("https://pixelreviveai.onrender.com/colorize", formData, { 
      responseType: 'blob',
});      setResult(URL.createObjectURL(res.data));
    } catch (err) {
      alert("Error: Is the Backend Running?");
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-[#0f172a] text-slate-200 font-sans selection:bg-indigo-500/30">
      
      {/* NAVBAR */}
      <nav className="border-b border-indigo-500/10 bg-[#0f172a]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
            <Sparkles className="text-indigo-400" size={24} />
            <span className="text-white">Pixel<span className="text-indigo-400">Revive</span></span>
          </div>
          <div className="text-xs font-mono text-indigo-300 bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20">
            v2.0 AI ENGINE
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-6 py-12">
        
        {/* HERO HEADER */}
        <div className="text-center mb-16 space-y-4">
          <h1 className="text-5xl md:text-6xl font-extrabold text-white tracking-tight">
            Bring History to <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">Life</span>
          </h1>
          <p className="text-slate-400 text-lg max-w-2xl mx-auto leading-relaxed">
            Our Deep Learning model analyzes luminance patterns in black & white photos 
            and hallucinates mathematically accurate colors using a Convolutional Neural Network (CNN).
          </p>
        </div>

        {/* UPLOAD AREA */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
            
            {/* INPUT CARD */}
            <div className={`relative group border-2 border-dashed rounded-3xl h-96 flex flex-col items-center justify-center transition-all duration-300 ${file ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-slate-700 hover:border-slate-500 bg-slate-800/50'}`}>
                <input type="file" id="upload" className="hidden" onChange={handleFile} accept="image/*"/>
                
                {preview ? (
                    <img src={preview} className="absolute inset-0 w-full h-full object-cover rounded-[22px] opacity-60" />
                ) : null}

                <label htmlFor="upload" className="relative z-10 cursor-pointer flex flex-col items-center gap-4 p-8 w-full h-full justify-center">
                    {!file && (
                        <>
                            <div className="p-4 bg-slate-800 rounded-full group-hover:scale-110 transition duration-300 shadow-xl">
                                <UploadCloud size={32} className="text-indigo-400" />
                            </div>
                            <div className="text-center">
                                <p className="text-lg font-semibold text-white">Upload B&W Photo</p>
                                <p className="text-sm text-slate-500 mt-1">JPG or PNG supported</p>
                            </div>
                        </>
                    )}
                </label>
            </div>

            {/* OUTPUT CARD */}
            <div className="relative border border-slate-700 bg-black rounded-3xl h-96 flex flex-col items-center justify-center overflow-hidden shadow-2xl">
                {result ? (
                    <img src={result} className="w-full h-full object-cover animate-in fade-in duration-1000" />
                ) : (
                    <div className="text-center p-8">
                        {loading ? (
                             <div className="flex flex-col items-center gap-4">
                                <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                                <p className="text-indigo-400 animate-pulse font-mono text-sm">RUNNING NEURAL NET...</p>
                             </div>
                        ) : (
                            <>
                                <ImageIcon size={48} className="text-slate-800 mx-auto mb-4" />
                                <p className="text-slate-600 font-medium">Colorized result will appear here</p>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>

        {/* ACTION BUTTON */}
        <div className="text-center mb-24">
            <button 
                onClick={handleColorize} 
                disabled={!file || loading}
                className="group relative inline-flex items-center justify-center px-8 py-4 font-bold text-white transition-all duration-200 bg-indigo-600 font-lg rounded-full hover:bg-indigo-700 hover:shadow-lg hover:shadow-indigo-500/30 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {loading ? "Processing..." : (
                    <>
                        Start Colorization <Zap className="ml-2 group-hover:text-yellow-300 transition-colors" size={20} fill="currentColor" />
                    </>
                )}
            </button>
        </div>

        {/* HOW IT WORKS SECTION */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 border-t border-slate-800 pt-16">
            <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50">
                <div className="w-10 h-10 bg-indigo-500/20 rounded-lg flex items-center justify-center mb-4">
                    <Info size={20} className="text-indigo-400"/>
                </div>
                <h3 className="text-white font-bold mb-2">1. Analysis</h3>
                <p className="text-sm text-slate-400 leading-relaxed">
                    The AI scans the image in the LAB color space, separating Lightness (L) from Color (A/B).
                </p>
            </div>
            <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50">
                <div className="w-10 h-10 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
                    <Sparkles size={20} className="text-purple-400"/>
                </div>
                <h3 className="text-white font-bold mb-2">2. Hallucination</h3>
                <p className="text-sm text-slate-400 leading-relaxed">
                    Using 1M+ training images, the model predicts the most probable colors for each texture (grass=green, sky=blue).
                </p>
            </div>
            <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700/50">
                <div className="w-10 h-10 bg-pink-500/20 rounded-lg flex items-center justify-center mb-4">
                    <Lock size={20} className="text-pink-400"/>
                </div>
                <h3 className="text-white font-bold mb-2">3. Reconstruction</h3>
                <p className="text-sm text-slate-400 leading-relaxed">
                    It merges the original sharp Lightness channel with the new colors to preserve 100% of the detail.
                </p>
            </div>
        </div>

      </div>
    </main>
  );
}