import React from 'react';

const Textarea = ({ label, className = '', ...props }) => {
  return (
    <div className="mb-4">
      {label && (
        <label className="block text-sm font-medium text-gray-300 mb-2">
          {label}
        </label>
      )}
      <textarea
        className={`input-field resize-none ${className}`}
        {...props}
      />
    </div>
  );
};

export default Textarea;
