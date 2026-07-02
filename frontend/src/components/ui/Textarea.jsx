import React from 'react';

const Textarea = ({ label, className = '', ...props }) => {
  return (
    <div className="mb-2">
      {label && (
        <label className="block text-xs font-medium text-text-secondary mb-2">
          {label}
        </label>
      )}
      <textarea
        className={`input-field resize-y ${className}`}
        {...props}
      />
    </div>
  );
};

export default Textarea;
