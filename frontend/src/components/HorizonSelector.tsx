/**
 * Investment Horizon Selector Component
 */
import { motion } from 'framer-motion';
import { Clock, Calendar, TrendingUp } from 'lucide-react';
import type { InvestmentHorizon } from '../types/api';

interface HorizonSelectorProps {
  value: InvestmentHorizon;
  onChange: (horizon: InvestmentHorizon) => void;
  disabled?: boolean;
}

const HORIZON_OPTIONS: Array<{ value: InvestmentHorizon; label: string; icon: typeof Clock; description: string }> = [
  { value: 'Short', label: 'Short Term', icon: Clock, description: '1-3 months' },
  { value: 'Mid', label: 'Mid Term', icon: Calendar, description: '3-12 months' },
  { value: 'Long', label: 'Long Term', icon: TrendingUp, description: '1+ years' },
];

export function HorizonSelector({ value, onChange, disabled = false }: HorizonSelectorProps) {
  return (
    <div className="selector-group">
      <label className="label">Investment Horizon</label>
      <div className="selector-grid">
        {HORIZON_OPTIONS.map((option) => {
          const Icon = option.icon;
          const isSelected = value === option.value;
          
          return (
            <motion.button
              key={option.value}
              type="button"
              disabled={disabled}
              onClick={() => onChange(option.value)}
              whileHover={{ scale: disabled ? 1 : 1.02 }}
              whileTap={{ scale: disabled ? 1 : 0.98 }}
              className={`selector-card ${isSelected ? 'selected' : ''} ${disabled ? 'disabled' : ''}`}
            >
              {isSelected && (
                <motion.div
                  layoutId="horizonSelector"
                  className="selector-highlight"
                  initial={false}
                  transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                />
              )}
              <div className="selector-column">
                <div className="selector-row">
                  <Icon size={18} color="#5cb8ff" />
                  <span className="selector-label">{option.label}</span>
                </div>
                <span className="selector-subtext">{option.description}</span>
              </div>
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}



