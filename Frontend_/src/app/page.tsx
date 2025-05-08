'use client';

import { useState } from 'react';
import Header from '../components/Header';
import FileUpload from '../components/FileUpload';
import ResultDisplay from '../components/ResultDisplay';

interface ProcessResult {
  csvLink: string;
  pdfLink: string;
}

export default function Home() {
  const [result, setResult] = useState<ProcessResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleProcess = async (file: File) => {
    setLoading(true);
    try {
      // Mock response
      const mockResponse = {
        csvLink: '/processed.csv',
        pdfLink: '/report.pdf'
      };
      setResult(mockResponse);
      setError('');
    } catch (err) {
      setError('Processing failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 pt-24">
        <div className="max-w-3xl mx-auto">
          {error && (
            <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">{error}</div>
          )}
          {!result ? (
            <FileUpload onProcess={handleProcess} />
          ) : (
            <ResultDisplay {...result} />
          )}
          {loading && (
            <div className="mt-4 text-center text-[#364957]">Processing...</div>
          )}
        </div>
      </main>
    </div>
  );
}