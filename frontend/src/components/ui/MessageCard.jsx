import React from 'react';
import { MessageSquare } from 'lucide-react';
import Card from './Card';
import SectionHeader from '../common/SectionHeader';

const MessageCard = ({ message, onChange, placeholder, maxLength = 10000, showCapacity = false, capacityText = '' }) => {
  return (
    <Card className="flex h-full flex-col">
      <SectionHeader icon={MessageSquare} title="Secret Message" />
      
      <div className="flex flex-1 flex-col">
        <textarea
          value={message}
          onChange={onChange}
          placeholder={placeholder}
          maxLength={maxLength}
          className="flex-1 w-full bg-card-secondary border border-border-primary rounded-xl px-4 py-3 text-text-primary placeholder-text-muted focus:outline-none focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 transition-all duration-300 resize-none"
        />
        <div className="flex justify-between items-center mt-3">
          <span className="text-xs text-text-muted">
            {message.length} / {maxLength} characters
          </span>
          {showCapacity && (
            <span className="text-xs text-text-secondary">
              {capacityText}
            </span>
          )}
        </div>
      </div>
    </Card>
  );
};

export default MessageCard;
