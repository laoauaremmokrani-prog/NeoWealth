function PredictionResults({ data }) {
  const { direction, sectors, companies, reasoning, probability_up, probability_down } = data

  return (
    <div className="space-y-6">
      {/* Market Direction */}
      <div className="card">
        <h2 className="text-2xl font-semibold mb-4">Market Direction</h2>
        <div className="flex items-center gap-4">
          <div className={`text-6xl ${direction === 'UP' ? 'text-green-400' : 'text-red-400'}`}>
            {direction === 'UP' ? '▲' : '▼'}
          </div>
          <div>
            <div className="text-3xl font-bold mb-2">
              {direction === 'UP' ? 'Bullish' : 'Bearish'} Trend
            </div>
            <div className="flex gap-6 text-sm text-gray-400">
              <span>UP: {(probability_up * 100).toFixed(1)}%</span>
              <span>DOWN: {(probability_down * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Sectors */}
      <div className="card">
        <h2 className="text-2xl font-semibold mb-4">Recommended Sectors</h2>
        <div className="flex flex-wrap gap-3">
          {sectors.map((sector, idx) => (
            <span
              key={idx}
              className="px-4 py-2 bg-indigo-500/20 border border-indigo-500/50 rounded-lg text-indigo-300"
            >
              {sector}
            </span>
          ))}
        </div>
      </div>

      {/* Companies */}
      <div className="card">
        <h2 className="text-2xl font-semibold mb-4">Top Company Recommendations</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {companies.slice(0, 10).map((company, idx) => (
            <div
              key={idx}
              className="px-4 py-2 bg-purple-500/20 border border-purple-500/50 rounded-lg text-center text-purple-300"
            >
              {company}
            </div>
          ))}
        </div>
      </div>

      {/* Reasoning */}
      <div className="card">
        <h2 className="text-2xl font-semibold mb-4">Prediction Reasoning</h2>
        <p className="text-gray-300 leading-relaxed">{reasoning}</p>
      </div>
    </div>
  )
}

export default PredictionResults







