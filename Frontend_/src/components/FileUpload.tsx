'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploadProps {
  onProcess: (file: File | null, driveLink: string) => void;
}

export default function FileUpload({ onProcess }: FileUploadProps) {
  const [driveLink, setDriveLink] = useState('');
  const [file, setFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFile(acceptedFiles[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv']
    }
  });

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl mx-auto">
      <div className="space-y-6">
        <div 
          {...getRootProps()}
          className={`border-2 border-dashed p-8 text-center cursor-pointer transition-colors
            ${isDragActive ? 
              'border-[#364957] bg-[#364957]/10' : 
              'border-gray-300'} hover:scale-105 transition-transform duration-200`}
        >
          <input {...getInputProps()} />
          <p className={`${isDragActive ? 'text-[#364957]' : 'text-gray-600'}`}>
            {isDragActive ? 'Drop CSV here' : 'Drag & drop CSV file, or click to select'}
          </p>
        </div>
        {file && (
          <div className="mt-2 p-2 bg-[#FF8A00]/20 text-[#FF8A00] rounded-md inline-block animate-fadeIn animate-pulse transition-opacity duration-500">
            {file.name}
          </div>
        )}

        <div className="relative">
          <div className="absolute inset-0 flex items-center" aria-hidden="true">
            <div className="w-full border-t border-[#364957]/30" />
          </div>
          <div className="relative flex justify-center">
            <span className="bg-white px-2 text-[#364957]">OR</span>
          </div>
        </div>

        <div className="space-y-4">
          <input
            type="text"
            value={driveLink}
            onChange={(e) => setDriveLink(e.target.value)}
            placeholder="Paste Google Drive link here"
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-[#FF8A00] focus:border-[#FF8A00] outline-none transition-shadow duration-300 hover:shadow-lg"
          />
        </div>
        {driveLink && (
          <div className="mt-2 p-2 bg-blue-100 text-blue-600 rounded-md inline-block animate-fadeIn animate-pulse transition-opacity duration-500">
            {driveLink}
          </div>
        )}

        <button
          onClick={() => onProcess(file, driveLink)}
          className="w-full bg-[#FF8A00] text-white py-3 px-6 rounded-lg hover:bg-[#E67A00] transition-colors font-medium"
          disabled={!file && !driveLink}
        >
          Process
        </button>
      </div>
    </div>
  );
}