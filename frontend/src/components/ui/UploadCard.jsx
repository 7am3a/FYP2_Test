import React, { useState } from 'react';
import { Upload, X, FileImage, Film } from 'lucide-react';
import Card from './Card';
import SectionHeader from '../common/SectionHeader';

const UploadCard = ({ onFileSelect, file, onRemove, label }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      onFileSelect?.(droppedFile);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      onFileSelect?.(selectedFile);
    }
  };

  const handleRemove = () => {
    onRemove?.();
  };

  const isVideo = file?.type.startsWith('video/');

  return (
    <Card className="flex h-full flex-col">
      <SectionHeader icon={Upload} title="Upload File" />
      
      <div className="flex flex-1">
        {file ? (
          <div className="flex flex-1 flex-col justify-center items-center p-6 bg-success/5 rounded-xl border border-success/20">
            <div className="flex justify-center mb-4">
              {isVideo ? (
                <Film className="w-12 h-12 text-success" />
              ) : (
                <FileImage className="w-12 h-12 text-success" />
              )}
            </div>
            <p className="text-success font-semibold text-sm text-center mb-1 truncate w-full px-4">
              {file.name}
            </p>
            <p className="text-text-muted text-xs mb-4">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
            <button
              onClick={handleRemove}
              className="flex items-center space-x-2 px-4 py-2 bg-danger/10 hover:bg-danger/20 border border-danger/30 rounded-xl text-danger text-xs transition-all duration-300"
            >
              <X className="w-3.5 h-3.5" />
              <span>Remove</span>
            </button>
          </div>
        ) : (
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`
              flex flex-1 flex-col justify-center items-center p-8 rounded-xl border-2 border-dashed transition-all duration-300 cursor-pointer relative
              ${isDragging ? 'border-accent-primary bg-accent-primary/10' : 'border-border-primary hover:border-border-secondary hover:bg-white/5'}
            `}
          >
            <input
              type="file"
              accept="image/*,video/*"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <div className="flex justify-center mb-4">
              <Upload className="w-16 h-16 text-accent-primary" />
            </div>
            <p className="text-text-primary text-base text-center mb-2 font-medium">
              Drag & drop or click to browse
            </p>
            <p className="text-text-muted text-xs">
              Images & videos
            </p>
          </div>
        )}
      </div>
    </Card>
  );
};

export default UploadCard;
