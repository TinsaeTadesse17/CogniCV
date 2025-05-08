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

  const handleProcess = async (file: File | null, driveLink: string) => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      if (file) {
        // Batch CSV processing
        const formData = new FormData();
        formData.append('csv_file', file);
        const uploadRes = await fetch('http://localhost:8000/batch_upload', { method: 'POST', body: formData });
        const { csv_id } = await uploadRes.json();
        let status = '';
        let csvLink = '';
        // Poll status until done
        while (status !== 'Done') {
          await new Promise(r => setTimeout(r, 1000));
          const statusRes = await fetch(`http://localhost:8000/status/${csv_id}`);
          const data = await statusRes.json();
          if (statusRes.status === 200 && data.csv_drive_url) {
            status = 'Done';
            csvLink = data.csv_drive_url;
          } else {
            status = data.status;
          }
        }
        setResult({ csvLink, pdfLink: '' });
      } else if (driveLink) {
        // Single CV processing
        const formData = new FormData();
        formData.append('drive_link', driveLink);
        const uploadRes = await fetch('http://localhost:8000/upload', { method: 'POST', body: formData });
        const data = await uploadRes.json();
        setResult({ csvLink: '', pdfLink: data.drive_url });
      }
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