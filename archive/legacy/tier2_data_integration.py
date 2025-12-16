#!/usr/bin/env python3
"""
Tier 2: Data Integration and Preparation
Integrates structured numerical data with unstructured text data and user risk preferences.
Prepares dataset for Tier 3 consumption.
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import argparse
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import nltk
from textblob import TextBlob
import re
import sys

class Tier2DataProcessor:
    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir
        self.output_dir = data_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Download required NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            print("Warning: Could not download NLTK data. Text processing may be limited.")
        
        # Initialize scalers
        self.numerical_scaler = StandardScaler()
        self.text_scaler = MinMaxScaler()
        
    def read_input_data(self):
        """Read input CSV data files from current directory"""
        print("Reading input data...")
        
        # Read macro data from generated CSV files
        macro_data = {}
        
        # Unemployment data
        unemployment_file = 'unemployment_data.csv'
        if os.path.exists(unemployment_file):
            unemployment_df = pd.read_csv(unemployment_file)
            macro_data['unemployment_rate'] = unemployment_df['UnemploymentRate'].iloc[-1] if len(unemployment_df) > 0 else 4.2
            print(f"  Loaded unemployment rate: {macro_data['unemployment_rate']}%")
        
        # Inflation data
        inflation_file = 'inflation_data.csv'
        if os.path.exists(inflation_file):
            inflation_df = pd.read_csv(inflation_file)
            macro_data['inflation_rate'] = inflation_df['inflation_pct'].iloc[-1] if len(inflation_df) > 0 else 2.7
            print(f"  Loaded inflation rate: {macro_data['inflation_rate']}%")
        
        # Interest rates data
        fed_rates_file = 'fed_rates.csv'
        if os.path.exists(fed_rates_file):
            fed_rates_df = pd.read_csv(fed_rates_file)
            if len(fed_rates_df) > 0:
                macro_data['interest_rate'] = fed_rates_df['Effective Rate'].iloc[-1]
                print(f"  Loaded interest rate: {macro_data['interest_rate']}%")
        
        # GDP data
        gdp_file = 'gdp_data.csv'
        if os.path.exists(gdp_file):
            gdp_df = pd.read_csv(gdp_file)
            if len(gdp_df) > 0:
                macro_data['GDP_growth'] = gdp_df['GDP_Growth'].iloc[-1]
                print(f"  Loaded GDP growth: {macro_data['GDP_growth']}%")
        
        # S&P 500 data
        sp500_file = 'sp500_data.csv'
        if os.path.exists(sp500_file):
            sp500_df = pd.read_csv(sp500_file)
            if len(sp500_df) > 0:
                value = sp500_df['Close'].iloc[-1]
                try:
                    macro_data['sp500_index'] = float(value)
                except Exception:
                    print("  Warning: Non-numeric S&P 500 value encountered; using 0.0")
                    macro_data['sp500_index'] = 0.0
                print(f"  Loaded S&P 500 index: {macro_data['sp500_index']}")
        
        # Create macro DataFrame
        if macro_data:
            macro_df = pd.DataFrame([macro_data])
            print(f"  Created macro data: {len(macro_df)} records")
        else:
            print("  Warning: No macro data found. Creating sample data.")
            macro_df = self._create_sample_macro_data()
        
        # Read news headlines from Al Jazeera
        headlines_file = None
        for file in os.listdir('.'):
            if file.startswith('aljazeera_economic_news_') and file.endswith('.csv'):
                headlines_file = file
                break
        
        if headlines_file:
            headlines_df = pd.read_csv(headlines_file)
            print(f"  Loaded headlines: {len(headlines_df)} records")
        else:
            print("  Warning: No headlines found. Creating sample data.")
            headlines_df = self._create_sample_headlines()
        
        return macro_df, headlines_df
    
    def _create_sample_macro_data(self):
        """Create sample macro data for testing when input data is not available"""
        sample_data = {
            'inflation_rate': [2.5, 3.1, 2.8, 2.9, 3.2],
            'interest_rate': [0.25, 0.5, 1.0, 1.5, 2.0],
            'unemployment_rate': [4.5, 4.2, 4.0, 3.8, 3.6],
            'GDP_growth': [2.1, 2.8, 3.2, 2.9, 2.7],
            'sp500_index': [4200, 4300, 4400, 4500, 4600],
            'timestamp': [
                '2024-01-01T00:00:00',
                '2024-02-01T00:00:00',
                '2024-03-01T00:00:00',
                '2024-04-01T00:00:00',
                '2024-05-01T00:00:00'
            ]
        }
        return pd.DataFrame(sample_data)
    
    def _create_sample_headlines(self):
        """Create sample headlines for testing when input data is not available"""
        sample_headlines = [
            {'source': 'Al Jazeera', 'headline': 'Federal Reserve signals potential rate cuts amid economic uncertainty', 'timestamp': '2024-05-01T00:00:00'},
            {'source': 'BBC', 'headline': 'US inflation shows signs of cooling, markets respond positively', 'timestamp': '2024-05-01T00:00:00'},
            {'source': 'Al Jazeera', 'headline': 'Global markets react to new economic policy announcements', 'timestamp': '2024-05-01T00:00:00'},
            {'source': 'BBC', 'headline': 'Tech stocks lead market rally as earnings exceed expectations', 'timestamp': '2024-05-01T00:00:00'},
            {'source': 'Al Jazeera', 'headline': 'Oil prices stabilize as supply concerns ease', 'timestamp': '2024-05-01T00:00:00'}
        ]
        return pd.DataFrame(sample_headlines)
    
    def get_user_risk_preference(self):
        """Get user risk level without interactive prompts (server-safe)."""
        env_risk = os.environ.get('RISK_LEVEL', '').lower()
        if env_risk in ['low', 'medium', 'high']:
            print(f"Using risk level from environment: {env_risk}")
            return env_risk
        print("RISK_LEVEL not set; defaulting to 'medium'.")
        return 'medium'
    
    def clean_and_normalize_numerical_data(self, macro_df):
        """Clean and normalize numerical data for MLP input"""
        print("Cleaning and normalizing numerical data...")
        
        # Select numerical columns (only those that exist)
        available_cols = []
        for col in ['inflation_rate', 'interest_rate', 'unemployment_rate', 'GDP_growth', 'sp500_index']:
            if col in macro_df.columns:
                available_cols.append(col)
        
        if not available_cols:
            print("  Warning: No numerical columns found")
            return pd.DataFrame()
        
        # Remove any rows with missing values
        macro_df_clean = macro_df[available_cols].dropna()
        
        if len(macro_df_clean) == 0:
            print("  Warning: No valid numerical data found")
            return macro_df[available_cols].fillna(0)
        
        # Coerce to numeric to avoid strings sneaking in
        macro_df_clean = macro_df_clean.apply(pd.to_numeric, errors='coerce').fillna(0.0)
        # Normalize numerical data
        normalized_data = self.numerical_scaler.fit_transform(macro_df_clean)
        
        # Create normalized DataFrame
        normalized_df = pd.DataFrame(
            normalized_data, 
            columns=available_cols,
            index=macro_df_clean.index
        )
        
        print(f"  Normalized {len(available_cols)} numerical features: {available_cols}")
        return normalized_df
    
    def process_text_headlines(self, headlines_df):
        """Organize text headlines for LLM processing"""
        print("Processing text headlines...")
        
        processed_headlines = []
        
        for _, row in headlines_df.iterrows():
            headline = str(row['headline'])
            source = str(row.get('source', 'Al Jazeera'))
            
            # Basic text cleaning
            cleaned_headline = re.sub(r'[^\w\s]', '', headline)
            cleaned_headline = re.sub(r'\s+', ' ', cleaned_headline).strip()
            
            # Extract keywords (simple approach)
            words = cleaned_headline.lower().split()
            keywords = [word for word in words if len(word) > 3][:5]  # Top 5 keywords
            
            # Basic sentiment analysis
            try:
                blob = TextBlob(headline)
                sentiment = blob.sentiment.polarity
            except:
                sentiment = 0.0
            
            processed_headlines.append({
                'original_headline': headline,
                'cleaned_headline': cleaned_headline,
                'keywords': keywords,
                'sentiment_score': sentiment,
                'source': source,
                'timestamp': row.get('timestamp', datetime.now().isoformat()),
                'relevance_score': row.get('relevance_score', 0)
            })
        
        print(f"  Processed {len(processed_headlines)} headlines")
        return processed_headlines
    
    def combine_data_for_output(self, normalized_macro_df, processed_headlines, risk_level):
        """Combine structured and unstructured inputs into integrated dataset"""
        print("Combining data for output...")
        
        # Create the integrated dataset
        integrated_data = {
            'timestamp': datetime.now().isoformat(),
            'risk_level': risk_level,
            'numerical_features': normalized_macro_df.to_dict('records') if not normalized_macro_df.empty else [],
            'text_features': processed_headlines,
            'metadata': {
                'macro_features_count': len(normalized_macro_df.columns) if not normalized_macro_df.empty else 0,
                'headlines_count': len(processed_headlines),
                'processing_timestamp': datetime.now().isoformat()
            }
        }
        
        return integrated_data
    
    def save_tier2_dataset(self, tier2_data):
        """Save the integrated dataset for consumption"""
        print("Saving Tier 2 dataset...")
        
        # Save as JSON for easy consumption
        json_file = os.path.join(self.output_dir, 'integrated_dataset.json')
        with open(json_file, 'w') as f:
            json.dump(tier2_data, f, indent=2, default=str)
        
        # Save as CSV for numerical analysis
        csv_file = os.path.join(self.output_dir, 'integrated_dataset.csv')
        
        # Flatten the data for CSV
        csv_data = []
        for i, macro_record in enumerate(tier2_data['numerical_features']):
            row = {
                'record_id': i,
                'risk_level': tier2_data['risk_level'],
                'timestamp': tier2_data['timestamp']
            }
            row.update(macro_record)
            
            # Add text features (first headline for this record)
            if i < len(tier2_data['text_features']):
                headline_data = tier2_data['text_features'][i]
                row.update({
                    'headline': headline_data['cleaned_headline'],
                    'sentiment_score': headline_data['sentiment_score'],
                    'source': headline_data['source'],
                    'relevance_score': headline_data.get('relevance_score', 0)
                })
            
            csv_data.append(row)
        
        csv_df = pd.DataFrame(csv_data)
        csv_df.to_csv(csv_file, index=False)
        
        print(f"  Dataset saved as JSON: {json_file}")
        print(f"  Dataset saved as CSV: {csv_file}")
        
        return json_file, csv_file
    
    def run(self, risk_level=None):
        """Main execution method"""
        print("=== Tier 2: Data Integration Started ===")
        print(f"Timestamp: {datetime.now()}")
        
        # Read input data
        macro_df, headlines_df = self.read_input_data()
        
        # Get user risk preference
        if risk_level is None:
            risk_level = self.get_user_risk_preference()
        
        # Process numerical data
        normalized_macro_df = self.clean_and_normalize_numerical_data(macro_df)
        
        # Process text data
        processed_headlines = self.process_text_headlines(headlines_df)
        
        # Combine data
        integrated_data = self.combine_data_for_output(normalized_macro_df, processed_headlines, risk_level)
        
        # Save dataset
        json_file, csv_file = self.save_tier2_dataset(integrated_data)
        
        print("=== Tier 2: Data Integration Completed ===")
        print(f"Risk level: {risk_level}")
        print(f"Numerical features: {len(normalized_macro_df.columns) if not normalized_macro_df.empty else 0}")
        print(f"Text features: {len(processed_headlines)}")
        print(f"Output files: {json_file}, {csv_file}")
        
        return integrated_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tier 2: Data Integration and Preparation')
    parser.add_argument('--risk-level', choices=['low', 'medium', 'high'], 
                       help='User risk preference level')
    parser.add_argument('--data-dir', default='./data', 
                       help='Directory containing input data')
    
    args = parser.parse_args()
    
    processor = Tier2DataProcessor(data_dir=args.data_dir)
    processor.run(risk_level=args.risk_level)
