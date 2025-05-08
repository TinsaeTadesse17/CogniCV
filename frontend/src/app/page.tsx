'use client';

import { useState, useEffect } from 'react';
import Header from '../components/Header';
import FileUpload from '../components/FileUpload';
import ResultDisplay from '../components/ResultDisplay';
import Spinner from '../components/Spinner';

interface ProcessResult {
  csvLink: string;
  pdfLink: string;
}

export default function Home() {
  const [result, setResult] = useState<ProcessResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isQueued, setIsQueued] = useState(false);

  const handleProcess = async (file: File | null, driveLink: string) => {
    setLoading(true);
    setError('');
    setResult(null);
    setIsQueued(false);
    try {
      if (file) {
        // Batch CSV processing
        setIsQueued(true);
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

  // request notification permission on mount
  useEffect(() => {
    if ('Notification' in window) Notification.requestPermission();
  }, []);

  // play a short beep
  const playSound = () => {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    osc.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.2);
  };

  // trigger notification when CSV is ready
  useEffect(() => {
    if (result?.csvLink) {
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('CSV Processing Complete', { body: 'Your CSV is ready to view' });
      }
      playSound();
    }
  }, [result?.csvLink]);

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
          {isQueued && loading && !result && (
            <div className="mt-4 p-2 bg-blue-100 text-blue-800 rounded-md animate-fadeIn">
              The CSV is being processed in the background. You will be notified when it's ready.
            </div>
          )}
          {loading && (
            <div className="mt-4 flex flex-col items-center animate-fadeIn">
              <Spinner className="w-12 h-12 mb-2" />
              <p className="text-[#364957] animate-pulse">Processing...</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}