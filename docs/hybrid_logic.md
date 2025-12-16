
# Hybrid Intelligence Model Logic

The core advantage of this system is the **Hybrid Approach**, combining quantitative rigor with qualitative insight.

## 1. Quantitative Engine (MLP)
- **Model**: Feed-forward Neural Network (TensorFlow/Keras).
- **Inputs**: 
  - Inflation Rate
  - Interest Rate
  - Unemployment Rate
  - GDP Growth
  - S&P 500 Index Level
- **Output**: Probability score (0.0 - 1.0) of the market trending UP.
- **Logic**: Learns historical correlations between macro indicators and market performance.

## 2. Qualitative Engine (LLM)
- **Model**: OpenAI GPT-4o-mini (or similar).
- **Inputs**:
  - Daily headlines
  - Geopolitical event summaries
- **Output**:
  - Sentiment Score (-1.0 to +1.0)
  - Geopolitical Risk Level (Low/Med/High)
  - Recommended Sectors (e.g., "Defense", "Energy")
- **Logic**: Understands nuance, panic, optimism, and second-order effects of news that numbers miss.

## 3. Fusion Logic (Hybrid Core)
The final prediction is derived as follows:

1. **Baseline**: Start with MLP Probability ($P_{mlp}$).
2. **Adjustment**: Calculate adjustment factor based on LLM Sentiment ($S_{llm}$).
   $$ P_{final} = P_{mlp} + (S_{llm} \times 0.2) $$
   *The 0.2 weight represents the influence of sentiment on shifting the technical baseline.*
3. **Clamping**: Ensure result stays within [0.0, 1.0].
4. **Decision**:
   - If $P_{final} \ge 0.5 \rightarrow \textbf{UP}$
   - If $P_{final} < 0.5 \rightarrow \textbf{DOWN}$
5. **Sector Overlay**: The trend applies generally, but the **LLM's recommended sectors** are provided as specific opportunities regardless of the broad market direction (alpha generation).

This approach mitigates the weakness of each individual method:
- Prevents the MLP from missing "black swan" news events.
- Prevents the LLM from hallucinating trends without numerical backing.
