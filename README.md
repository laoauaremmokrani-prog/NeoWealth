NeoWealth AI Stock Market Prediction System
Overview

NeoWealth is a modern AI-driven stock market prediction system designed to forecast S&P 500 trends, identify outperforming sectors, and recommend top companies. It integrates macroeconomic, geopolitical, and investor sentiment data using a hybrid AI model combining a Multi-Layer Perceptron (MLP) neural network and a Large Language Model (LLM).

This project is structured into three tiers:

Tier 1 (Data Pipeline): Collects and processes raw financial, geopolitical, and sentiment data. Supports mock data for demo purposes.

Tier 2 (Processing): Cleans, normalizes, and engineers features from raw data, preparing inputs for the AI models.

Tier 3 (Model): Executes the core prediction logic using a hybrid AI model combining MLP for numerical data and an OpenAI-powered LLM for textual sentiment and geopolitical interpretation.

The frontend is a sleek, modern React application featuring a 3D market visualization powered by React Three Fiber, designed for an impressive, premium fintech user experience.

Features

Accurate Market Predictions: Targeting 70–80% accuracy on S&P 500 directional movement.

Sector and Company Recommendations: Identifies sectors and top companies likely to outperform.

Hybrid AI System: Combines numerical and textual data modeling for nuanced predictions.

Realistic Mock Data: Demo mode for frontend with deterministic mock predictions.

Modern Frontend: React 18, Vite, TypeScript, and React Three Fiber for 3D visuals without Tailwind CSS.

Database Integration: Uses Supabase for data storage and ingestion.

Comprehensive Documentation: Architecture diagrams, API endpoints, testing reports included.

Installation

Clone the repository:

git clone https://github.com/laoauaremmokrani-prog/NeoWealth.git
cd NeoWealth


Setup environment variables:

Create a .env file in the Tier 3 directory for your OpenAI API key (if backend integration is enabled):


For demo mode, .env is optional.

Install dependencies:

Backend tiers (Tier 1, 2, 3) - Python dependencies:

pip install -r requirements.txt


Frontend dependencies:

cd frontend
npm install

Usage
Running the Backend (demo mode)

You can run Tier 1 scheduler to ingest mock data:

python tier1_data_pipeline/scheduler.py


Run the Tier 3 prediction script with mock data or real data if configured.

Running the Frontend

Start the React app with:

cd frontend
npm run dev


Open http://localhost:5173
 in your browser.

Project Structure
NeoWealth/
├── tier1_data_pipeline/    # Data fetching and ingestion (mock or real)
├── tier2_processing/       # Data cleaning, normalization, and feature engineering
├── tier3_model/            # AI prediction models (MLP + LLM hybrid)
├── database/               # Supabase client and database scripts
├── frontend/               # React 3D frontend without Tailwind CSS
├── docs/                   # Documentation files (architecture, API, testing)
├── .gitignore
├── README.md
└── requirements.txt

Technologies Used

Python (Pandas, PyTorch, OpenAI API)

React 18 + TypeScript + Vite

React Three Fiber (Three.js integration)

Supabase (PostgreSQL backend)

PostCSS removed; custom CSS styles only

Mock data for frontend demo mode

Contributors
Islem Mehdi Laouarem

NIzar Mokrani


Notes

Backend integration currently optional; frontend supports fully mocked predictions.

All sensitive data (API keys) must be excluded from the repository.

For deployment, configure Supabase credentials and OpenAI API keys securely.

Focused on making the project impressive for university admissions and fintech showcases.

License

MIT License
