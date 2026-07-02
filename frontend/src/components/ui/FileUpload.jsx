import React, { useState } from 'react';
import { Upload, FileImage, Film } from 'lucide-react';
import { motion } from 'framer-motion';

const FileUpload = ({ onFileSelect, accept = 'image/*,video/*,audio/*', label }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

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
    const file = e.dataTransfer.files[0];
    if (file) {
      setSelectedFile(file);
      onFileSelect?.(file);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      onFileSelect?.(file);
    }
  };

  const isVideo = selectedFile?.type.startsWith('video/');

  return (
    <div className="mb-2">
      {label && (
        <label className="block text-xs font-medium text-gray-400 mb-2">
          {label}
        </label>
      )}
      <motion.div
        whileHover={{ scale: 1.01 }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-4 text-center transition-all duration-300
          ${isDragging ? 'border-cyber-accent bg-cyber-accent/10' : 'border-white/20 hover:border-cyber-accent/50'}
          ${selectedFile ? 'border-cyber-green/50 bg-cyber-green/5' : ''}
        `}
      >
        <input
          type="file"
          accept={accept}
          onChange={handleFileChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        {selectedFile ? (
          <div className="space-y-2">
            <div className="flex justify-center">
              {isVideo ? (
                <Film className="w-8 h-8 text-cyber-green" />
              ) : (
                <FileImage className="w-8 h-8 text-cyber-green" />
              )}
            </div>
            <p className="text-cyber-green text-sm font-medium truncate px-2">{selectedFile.name}</p>
            <p className="text-gray-400 text-xs">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="flex justify-center">
              <Upload className="w-8 h-8 text-cyber-accent" />
            </div>
            <p className="text-gray-300 text-sm">
              Drag & drop or click to browse
            </p>
            <p className="text-gray-500 text-xs">
              Images & videos
            </p>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default FileUpload;
