import React from 'react';

const TwoColumnLayout = ({ leftColumn, rightColumn, className = '' }) => {
  return (
    <div className={`grid grid-cols-1 lg:grid-cols-2 gap-4 ${className}`}>
      <div className="space-y-4">
        {leftColumn}
      </div>
      <div className="space-y-4">
        {rightColumn}
      </div>
    </div>
  );
};

export default TwoColumnLayout;
