import React from 'react';
import { Lock } from 'lucide-react';
import Card from './Card';
import PasswordInput from './PasswordInput';
import SectionHeader from '../common/SectionHeader';

const PasswordCard = ({ password, onChange, placeholder, showStrength = false, strength = null }) => {
  return (
    <Card className="flex h-full flex-col justify-center">
      <SectionHeader icon={Lock} title="Password" />
      
      <div className="flex flex-col">
        <PasswordInput
          label=""
          value={password}
          onChange={onChange}
          placeholder={placeholder}
        />
        
        {showStrength && strength && (
          <div className="mt-3">
            <div className="flex justify-between items-center mb-1.5">
              <span className="text-xs text-text-muted">Password Strength</span>
              <span className={`text-xs font-medium ${
                strength.score >= 3 ? 'text-success' : 
                strength.score >= 2 ? 'text-warning' : 
                strength.score >= 1 ? 'text-danger' : 'text-text-muted'
              }`}>
                {strength.label}
              </span>
            </div>
            <div className="flex space-x-1">
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className={`h-1.5 flex-1 rounded-full transition-all duration-300 ${
                    i <= strength.score
                      ? strength.score >= 3 ? 'bg-success' : 
                        strength.score >= 2 ? 'bg-warning' : 'bg-danger'
                      : 'bg-border-primary'
                  }`}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};

export default PasswordCard;
