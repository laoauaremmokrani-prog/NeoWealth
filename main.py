"""
Main Orchestration Script
Runs Tier 1 → Tier 2 → Tier 3 pipeline.
"""

from tier1 import get_static_test_data
from tier2 import MockTier2Processor
from tier3 import generate_prediction
import json
from datetime import datetime


def run_pipeline(risk_level: str = "medium", investment_horizon: str = "Mid") -> dict:
    """
    Run the complete prediction pipeline.
    
    Args:
        risk_level: "low", "medium", or "high"
        investment_horizon: "Short", "Mid", or "Long"
        
    Returns:
        Complete prediction result
    """
    print("=" * 60)
    print("Stock Market Prediction Pipeline")
    print("=" * 60)
    
    # Tier 1: Get static test data
    print("\n[Tier 1] Loading static test data...")
    tier1_data = get_static_test_data()
    print(f"  ✓ Loaded macroeconomic indicators")
    print(f"  ✓ Loaded {len(tier1_data['sentiment'])} sentiment texts")
    print(f"  ✓ Loaded {len(tier1_data['geopolitical'])} geopolitical texts")
    
    # Tier 2: Mock processing
    print(f"\n[Tier 2] Processing data (risk_level: {risk_level})...")
    processor = MockTier2Processor(risk_level=risk_level)
    tier2_data = processor.process(tier1_data)
    print(f"  ✓ Processed numerical features: {len(tier2_data['numerical_features'])}")
    print(f"  ✓ Combined text input: {len(tier2_data['text_input'])} chars")
    
    # Tier 3: Hybrid prediction
    print(f"\n[Tier 3] Running hybrid prediction (horizon: {investment_horizon})...")
    prediction = generate_prediction(
        numerical_features=tier2_data["numerical_features"],
        text_input=tier2_data["text_input"],
        risk_level=risk_level,
        investment_horizon=investment_horizon
    )
    print(f"  ✓ S&P 500 Direction: {prediction['sp500_direction']}")
    print(f"  ✓ Recommended Sectors: {', '.join(prediction['recommended_sectors'])}")
    print(f"  ✓ Top Companies: {', '.join(prediction['top_companies'][:5])}")
    
    # Combine all results
    final_result = {
        "timestamp": datetime.now().isoformat(),
        "tier1_snapshot": tier1_data["macroeconomic"],
        "tier2_risk_level": risk_level,
        "tier2_horizon": investment_horizon,
        "tier3_prediction": prediction
    }
    
    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
    
    return final_result


def save_result(result: dict, filename: str = "prediction_result.json"):
    """Save prediction result to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nResult saved to {filename}")


if __name__ == "__main__":
    # Run pipeline with default settings
    result = run_pipeline(risk_level="medium", investment_horizon="Mid")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PREDICTION SUMMARY")
    print("=" * 60)
    pred = result["tier3_prediction"]
    print(f"\nS&P 500 Direction: {pred['sp500_direction']}")
    print(f"Probability UP: {pred['probability_up']:.1%}")
    print(f"Probability DOWN: {pred['probability_down']:.1%}")
    print(f"\nRecommended Sectors:")
    for sector in pred['recommended_sectors']:
        print(f"  • {sector}")
    print(f"\nTop Companies:")
    for company in pred['top_companies'][:10]:
        print(f"  • {company}")
    print(f"\nReasoning:")
    print(f"  {pred['reasoning']}")
    
    # Save result
    save_result(result)

