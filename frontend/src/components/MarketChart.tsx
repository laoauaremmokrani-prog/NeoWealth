/**
 * Market Trend Chart Component
 * Displays historical and forecasted market trends
 */
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Badge } from './ui/Badge';
import { motion } from 'framer-motion';
import type { FullPredictionResponse } from '../types/api';

interface MarketChartProps {
  prediction: FullPredictionResponse | null;
}

// Generate mock historical data (deterministic for demo mode)
// In production, this would come from the backend
const generateChartData = (direction: 'UP' | 'DOWN' | null) => {
  const baseValue = 4500;
  const trend = direction === 'UP' ? 1 : direction === 'DOWN' ? -1 : 0;
  
  // Deterministic pattern: use index-based pseudo-random pattern instead of Math.random()
  const deterministicVariation = (index: number) => {
    // Simple deterministic pattern based on index
    return Math.sin(index * 0.5) * 50 + Math.cos(index * 0.3) * 30;
  };
  
  return Array.from({ length: 30 }, (_, i) => ({
    date: `Day ${i + 1}`,
    value: baseValue + deterministicVariation(i) + (i * 10 * trend),
  }));
};

export function MarketChart({ prediction }: MarketChartProps) {
  const direction = prediction?.tier3_prediction?.sp500_direction || prediction?.direction || null;
  const probabilityUp = prediction?.tier3_prediction?.probability_up ?? prediction?.probability_up ?? 0;
  const confidence = Math.max(probabilityUp, 1 - probabilityUp) * 100;
  const data = generateChartData(direction);
  const isBullish = direction === 'UP';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <Card className="chart-card">
        <CardHeader>
          <div>
            <CardTitle>Market Trend Analysis</CardTitle>
            <p className="muted subtle">30-Day Historical &amp; Forecast</p>
          </div>
          <div className="badge-row">
            <Badge variant={isBullish ? 'success' : 'danger'}>
              {isBullish ? 'Bullish Signal' : 'Bearish Signal'}
            </Badge>
            <Badge variant="outline">AI Confidence: {confidence.toFixed(0)}%</Badge>
          </div>
        </CardHeader>
        <CardContent className="chart-content">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor={isBullish ? '#00ffa3' : '#ff3366'}
                    stopOpacity={0.3}
                  />
                  <stop
                    offset="95%"
                    stopColor={isBullish ? '#00ffa3' : '#ff3366'}
                    stopOpacity={0}
                  />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis
                dataKey="date"
                stroke="#666"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                interval="preserveStartEnd"
              />
              <YAxis
                stroke="#666"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                domain={['auto', 'auto']}
                tickFormatter={(value) => `$${value.toFixed(0)}`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.9)',
                  borderColor: '#333',
                  borderRadius: '8px',
                  color: '#fff',
                  backdropFilter: 'blur(10px)',
                }}
                itemStyle={{ color: isBullish ? '#00ffa3' : '#ff3366' }}
              />
              <Area
                type="monotone"
                dataKey="value"
                stroke={isBullish ? '#00ffa3' : '#ff3366'}
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorValue)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </motion.div>
  );
}
