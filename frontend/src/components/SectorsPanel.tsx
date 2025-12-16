/**
 * Recommended Sectors Panel
 */
import { motion } from 'framer-motion';
import { TrendingUp, Building2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { Badge } from './ui/Badge';
import type { FullPredictionResponse } from '../types/api';

interface SectorsPanelProps {
  prediction: FullPredictionResponse | null;
}

export function SectorsPanel({ prediction }: SectorsPanelProps) {
  const sectors = prediction?.tier3_prediction?.recommended_sectors || prediction?.sectors || [];

  if (sectors.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="title-inline">
            <Building2 size={18} color="#5cb8ff" />
            Recommended Sectors
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="center-note">No sectors available</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="title-inline">
          <Building2 size={18} color="#5cb8ff" />
          Recommended Sectors
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="stacked">
          {sectors.map((sector, index) => (
            <motion.div
              key={sector}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="tile"
            >
              <div className="tile-left">
                <div className="tile-icon">
                  <TrendingUp size={18} color="#5cb8ff" />
                </div>
                <div className="tile-meta">
                  <div className="tile-title">{sector}</div>
                  <div className="tile-subtitle">AI Recommended</div>
                </div>
              </div>
              <Badge variant="success" className="mono-badge">
                #{index + 1}
              </Badge>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}



