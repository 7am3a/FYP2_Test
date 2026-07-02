import React from 'react';
import { Shield, Lock, Eye, FileText, CheckCircle } from 'lucide-react';

const SecurityInfoBar = () => {
  const sections = [
    {
      icon: Shield,
      title: 'AES-256-GCM',
      subtitle: 'Military Grade',
    },
    {
      icon: Lock,
      title: 'Argon2id',
      subtitle: 'Key Derivation',
    },
    {
      icon: Eye,
      title: 'Steganography',
      subtitle: 'Data Hiding',
    },
    {
      icon: FileText,
      title: 'Undetectable',
      subtitle: 'Secure Transmission',
    },
    {
      icon: CheckCircle,
      title: 'Verified Platform',
      subtitle: 'Authentic & Safe',
    },
  ];

  return (
    <div className="w-full py-4">
      <div className="glass-card p-5">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-0 divide-y md:divide-y-0 md:divide-x divide-border-primary">
          {sections.map((section, index) => (
            <div key={index} className="flex flex-col items-center justify-center text-center px-3 py-2 md:py-0">
              <div className="w-10 h-10 rounded-lg bg-card-secondary border border-border-primary flex items-center justify-center mb-2">
                <section.icon className="w-5 h-5 text-accent-primary" />
              </div>
              <h4 className="text-xs font-semibold text-text-primary mb-0.5">
                {section.title}
              </h4>
              <p className="text-[10px] text-text-muted">
                {section.subtitle}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SecurityInfoBar;
