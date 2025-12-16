# AI Market Intelligence Frontend

Modern, production-grade React frontend for the AI Stock Market Prediction System.

## Features

- 🎨 **Premium UI/UX**: Dark theme with glassmorphism, smooth animations, and modern design
- 📊 **Real-time Data**: Live market predictions with animated charts and tickers
- 🎯 **Interactive Controls**: Risk level and investment horizon selectors
- ⚡ **Fast & Responsive**: Built with Vite, React 18, and TypeScript
- 🎭 **Smooth Animations**: Framer Motion for fluid transitions
- 📈 **Data Visualization**: Recharts for beautiful market trend charts

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Plain CSS** - Custom gradients, grids, and typography
- **Framer Motion** - Animations
- **Recharts** - Chart library
- **Axios** - HTTP client
- **Lucide React** - Icons

## Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Configuration

The frontend connects to the backend API. By default, it expects the backend to run on `http://localhost:5000`.

You can configure the API URL by setting the environment variable:

```bash
# Create .env file
VITE_API_URL=http://localhost:5000
```

## Development

The development server runs on `http://localhost:5173` with hot module replacement.

The Vite proxy is configured to forward `/api/*` requests to the backend server at `http://localhost:5000`.

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Dashboard.tsx    # Main dashboard
│   │   ├── PredictionPanel.tsx
│   │   ├── MarketChart.tsx
│   │   ├── MarketTicker.tsx
│   │   ├── RiskSelector.tsx
│   │   ├── HorizonSelector.tsx
│   │   ├── SectorsPanel.tsx
│   │   ├── CompaniesPanel.tsx
│   │   ├── ReasoningPanel.tsx
│   │   ├── AnimatedBackground.tsx
│   │   ├── Sidebar.tsx
│   │   └── ui/              # Reusable UI components
│   ├── services/           # API services
│   │   └── api.ts          # Backend API client
│   ├── types/              # TypeScript types
│   │   └── api.ts          # API type definitions
│   ├── App.tsx             # Root component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── index.html              # HTML template
├── vite.config.ts          # Vite configuration
└── package.json            # Dependencies
```

## Usage

1. **Start the backend server** (on port 5000)
2. **Start the frontend**:
   ```bash
   npm run dev
   ```
3. **Open your browser** to `http://localhost:5173`
4. **Select parameters**:
   - Risk Level: Low, Medium, or High
   - Investment Horizon: Short, Mid, or Long
5. **Click "Run Prediction"** to get AI-powered market insights

## Components

### Dashboard
Main orchestrator component that manages state and API calls.

### PredictionPanel
Displays the core prediction: S&P 500 direction, confidence, and key metrics.

### MarketChart
Shows 30-day historical and forecasted market trends with animated area chart.

### MarketTicker
Animated ticker showing real-time market indices and stock prices.

### RiskSelector & HorizonSelector
Interactive selectors for prediction parameters with smooth animations.

### SectorsPanel & CompaniesPanel
Display recommended sectors and top stock picks from the AI model.

### ReasoningPanel
Shows the AI's reasoning behind the prediction.

## API Integration

The frontend communicates with the backend via the `/predict` endpoint:

**Request:**
```json
{
  "risk_level": "low" | "medium" | "high",
  "investment_horizon": "Short" | "Mid" | "Long"
}
```

**Response:**
```json
{
  "direction": "UP" | "DOWN",
  "sectors": ["Technology", "Healthcare", ...],
  "companies": ["AAPL", "MSFT", ...],
  "reasoning": "...",
  "probability_up": 0.75,
  "probability_down": 0.25
}
```

## Styling

Styling uses handcrafted CSS (no Tailwind/PostCSS) with:
- Radial gradients for the hero background
- Glass panels, soft glows, and premium typography
- Custom grids for cards and selectors
- Motion polish via Framer Motion classes

## Production Build

```bash
npm run build
```

The build output is in the `dist/` directory, ready for deployment.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Part of the AI Stock Market Prediction System.



