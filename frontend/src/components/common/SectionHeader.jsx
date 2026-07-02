import React from 'react';

const SectionHeader = ({ icon: Icon, title, className = '' }) => {
  return (
    <div className={`card-header ${className}`}>
      <div className="card-icon">
        <Icon className="w-5 h-5 text-accent-primary" />
      </div>
      <h3 className="text-2xl font-semibold text-text-primary">{title}</h3>
    </div>
  );
};

export default SectionHeader;
