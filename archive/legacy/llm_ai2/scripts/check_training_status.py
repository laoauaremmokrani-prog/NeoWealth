#!/usr/bin/env python3
"""
Check Training Status for Original MLP Model

This script checks if the MLP model and associated files exist.
"""

import os
from pathlib import Path
from datetime import datetime

def main():
    """Check the status of MLP model files."""
    print("MLP Model Training Status Check")
    print("=" * 40)
    
    # Check model files
    model_path = Path('models/mlp_model.keras')
    scaler_path = Path('models/mlp_model_scaler.pkl')
    
    print(f"Model file: {model_path}")
    if model_path.exists():
        size = model_path.stat().st_size / 1024  # KB
        mtime = datetime.fromtimestamp(model_path.stat().st_mtime)
        print(f"  ✅ Exists ({size:.1f} KB, modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print("  ❌ Missing")
    
    print(f"\nScaler file: {scaler_path}")
    if scaler_path.exists():
        size = scaler_path.stat().st_size / 1024  # KB
        mtime = datetime.fromtimestamp(scaler_path.stat().st_mtime)
        print(f"  ✅ Exists ({size:.1f} KB, modified: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print("  ❌ Missing")
    
    # Overall status
    print("\n" + "=" * 40)
    if model_path.exists() and scaler_path.exists():
        print("🎯 MLP Model is ready for use!")
        print("   - Model file: ✅")
        print("   - Scaler file: ✅")
        print("   - Ready for predictions")
    else:
        print("⚠️  MLP Model needs training!")
        print("   - Run: python scripts/train_mlp.py")
        print("   - This will create the required model files")

if __name__ == "__main__":
    main()
