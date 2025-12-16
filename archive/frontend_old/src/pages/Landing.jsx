function Landing({ onNavigate }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="max-w-4xl text-center animate-fade-in">
        <h1 className="text-6xl md:text-7xl font-bold mb-6">
          <span className="gradient-text">Tier 3 AI</span>
        </h1>
        <p className="text-2xl md:text-3xl text-gray-400 mb-4">
          Market Intelligence Engine
        </p>
        <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto">
          Advanced hybrid AI system combining MLP neural networks and OpenAI GPT-4o-mini LLM 
          to deliver precise market predictions, sector analysis, and investment recommendations.
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="card">
            <div className="text-4xl mb-4">🧠</div>
            <h3 className="text-xl font-semibold mb-2">MLP Neural Network</h3>
            <p className="text-gray-400 text-sm">
              Analyzes macroeconomic indicators to predict market trends with high accuracy.
            </p>
          </div>
          
          <div className="card">
            <div className="text-4xl mb-4">💬</div>
            <h3 className="text-xl font-semibold mb-2">OpenAI GPT-4o-mini</h3>
            <p className="text-gray-400 text-sm">
              Processes sentiment and geopolitical data for comprehensive market analysis using advanced AI.
            </p>
          </div>
          
          <div className="card">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold mb-2">Hybrid Intelligence</h3>
            <p className="text-gray-400 text-sm">
              Combines numerical and textual analysis for superior prediction accuracy.
            </p>
          </div>
        </div>
        
        <button
          onClick={onNavigate}
          className="btn-primary text-lg px-8 py-4"
        >
          Launch Dashboard →
        </button>
      </div>
    </div>
  )
}

export default Landing

