'use client';

interface ResultDisplayProps {
  csvLink: string;
  pdfLink: string;
}

export default function ResultDisplay({ csvLink, pdfLink }: ResultDisplayProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-lg space-y-6">
      <h2 className="text-2xl font-semibold text-[#364957]">Processing Complete!</h2>
      <div className="space-y-4">
        <div className="p-4 border-2 border-[#364957]/10 rounded-lg">
          <h3 className="text-lg font-medium text-[#364957]">Processed CSV</h3>
          <a
            href={csvLink}
            className="mt-2 inline-block bg-[#FF8A00] text-white px-6 py-2 rounded-md hover:bg-[#E67A00] transition-colors"
            download
          >
            Download CSV
          </a>
        </div>
        <div className="p-4 border-2 border-[#364957]/10 rounded-lg">
          <h3 className="text-lg font-medium text-[#364957]">Generated PDF Report</h3>
          <a
            href={pdfLink}
            className="mt-2 inline-block bg-[#FF8A00] text-white px-6 py-2 rounded-md hover:bg-[#E67A00] transition-colors"
            target="_blank"
            rel="noopener noreferrer"
          >
            View PDF
          </a>
        </div>
      </div>
    </div>
  );
}