/**
 * Top Companies Panel
 */
import { motion } from 'framer-motion';
import { TrendingUp, ArrowUpRight } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { Badge } from './ui/Badge';
import type { FullPredictionResponse } from '../types/api';

interface CompaniesPanelProps {
  prediction: FullPredictionResponse | null;
}

export function CompaniesPanel({ prediction }: CompaniesPanelProps) {
  const companies = prediction?.tier3_prediction?.top_companies || prediction?.companies || [];

  if (companies.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="title-inline">
            <TrendingUp size={18} color="#4deca3" />
            Top Stock Picks
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="center-note">No companies available</p>
        </CardContent>
      </Card>
    );
  }

  // Display top 10 companies
  const displayCompanies = companies.slice(0, 10);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="title-inline">
          <TrendingUp size={18} color="#4deca3" />
          Top Stock Picks
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="stacked">
          {displayCompanies.map((ticker, index) => (
            <motion.div
              key={ticker}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="tile"
            >
              <div className="tile-left">
                <div className="tile-icon circle green">
                  {ticker[0]}
                </div>
                <div className="tile-meta">
                  <div className="tile-title mono">{ticker}</div>
                  <div className="tile-subtitle">AI Recommended</div>
                </div>
              </div>
              <div className="tile-actions">
                <Badge variant="success" className="mono-badge">
                  #{index + 1}
                </Badge>
                <ArrowUpRight size={16} color="#4deca3" />
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}



