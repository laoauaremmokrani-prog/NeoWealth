/**
 * Risk Level Selector Component
 */
import { motion } from 'framer-motion';
import { Shield, AlertTriangle, Zap } from 'lucide-react';
import type { RiskLevel } from '../types/api';

interface RiskSelectorProps {
  value: RiskLevel;
  onChange: (risk: RiskLevel) => void;
  disabled?: boolean;
}

const RISK_OPTIONS: Array<{ value: RiskLevel; label: string; icon: typeof Shield }> = [
  { value: 'low', label: 'Low Risk', icon: Shield },
  { value: 'medium', label: 'Medium Risk', icon: AlertTriangle },
  { value: 'high', label: 'High Risk', icon: Zap },
];

const RISK_COLORS: Record<RiskLevel, string> = {
  low: '#4deca3',
  medium: '#f5c26b',
  high: '#ff7f9a',
};

export function RiskSelector({ value, onChange, disabled = false }: RiskSelectorProps) {
  return (
    <div className="selector-group">
      <label className="label">Risk Level</label>
      <div className="selector-grid">
        {RISK_OPTIONS.map((option) => {
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
                  layoutId="riskSelector"
                  className="selector-highlight"
                  initial={false}
                  transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                />
              )}
              <div className="selector-column center">
                <Icon size={18} style={{ color: RISK_COLORS[option.value] }} />
                <span className="selector-label">{option.label}</span>
              </div>
            </motion.button>
          );
        })}
      </div>
    </div>
  );
}



