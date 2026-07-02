import React from 'react';
import { Shield } from 'lucide-react';
import Card from './Card';
import Button from './Button';
import SectionHeader from '../common/SectionHeader';

const ActionCard = ({ 
  onClick, 
  disabled, 
  isProcessing, 
  buttonText, 
  processingText, 
  icon: Icon,
  error = null 
}) => {
  return (
    <Card className="flex h-full flex-col justify-center p-6">
      {error && (
        <div className="mb-3 p-2 rounded-lg bg-danger/10 border border-danger/30">
          <p className="text-danger text-xs">{error}</p>
        </div>
      )}
      
      <Button
        onClick={onClick}
        disabled={disabled}
        className="w-full flex-1 text-lg"
      >
        {isProcessing ? (
          <>
            <div className="animate-spin mr-3">
              <Icon className="w-6 h-6" />
            </div>
            {processingText}
          </>
        ) : (
          <>
            <Icon className="w-6 h-6 mr-3" />
            {buttonText}
          </>
        )}
      </Button>
    </Card>
  );
};

export default ActionCard;
