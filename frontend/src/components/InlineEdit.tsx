import React, { useState, useRef, useEffect } from 'react';
import { Check, X, Pencil } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface InlineEditProps {
  value: string;
  onSave: (value: string) => Promise<void>;
  type?: 'text' | 'textarea' | 'number';
  className?: string;
  placeholder?: string;
  multiline?: boolean;
  rows?: number;
}

export const InlineEdit: React.FC<InlineEditProps> = ({
  value,
  onSave,
  type = 'text',
  className = '',
  placeholder = '',
  multiline = false,
  rows = 3,
}) => {
  const { isEditMode } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(value);
  const [isSaving, setIsSaving] = useState(false);
  const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isEditing]);

  useEffect(() => {
    setEditValue(value);
  }, [value]);

  const handleSave = async () => {
    if (editValue === value) {
      setIsEditing(false);
      return;
    }

    setIsSaving(true);
    try {
      await onSave(editValue);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to save:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setEditValue(value);
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !multiline) {
      e.preventDefault();
      handleSave();
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  if (!isEditMode) {
    return <span className={className}>{value || placeholder}</span>;
  }

  if (isEditing) {
    const inputClasses = `
      w-full px-2 py-1 border-2 border-primary-500 rounded-lg
      bg-white dark:bg-dark-card text-slate-900 dark:text-slate-100
      focus:outline-none focus:ring-2 focus:ring-primary-500/50
      ${className}
    `;

    return (
      <div className="inline-flex items-start gap-2 w-full">
        {multiline ? (
          <textarea
            ref={inputRef as React.RefObject<HTMLTextAreaElement>}
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className={inputClasses}
            rows={rows}
            disabled={isSaving}
          />
        ) : (
          <input
            ref={inputRef as React.RefObject<HTMLInputElement>}
            type={type}
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className={inputClasses}
            disabled={isSaving}
          />
        )}
        <div className="flex gap-1">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="p-1 text-green-600 hover:bg-green-100 dark:hover:bg-green-900/30 rounded"
            title="Save"
          >
            <Check className="w-4 h-4" />
          </button>
          <button
            onClick={handleCancel}
            disabled={isSaving}
            className="p-1 text-red-600 hover:bg-red-100 dark:hover:bg-red-900/30 rounded"
            title="Cancel"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <span
      onClick={() => setIsEditing(true)}
      className={`
        inline-flex items-center gap-1 cursor-pointer group
        hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded px-1 -mx-1
        ${className}
      `}
    >
      {value || <span className="text-slate-400 italic">{placeholder}</span>}
      <Pencil className="w-3 h-3 text-primary-500 opacity-0 group-hover:opacity-100 transition-opacity" />
    </span>
  );
};
