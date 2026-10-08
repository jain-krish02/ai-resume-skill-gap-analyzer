import { useState } from 'react';
import axios from 'axios';

export default function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      const ext = selected.name.split('.').pop().toLowerCase();
      if (ext !== 'pdf' && ext !== 'docx') {
        setError('Only PDF and DOCX files are allowed.');
        setFile(null);
        return;
      }
      if (selected.size > 5 * 1024 * 1024) {
        setError('File size exceeds 5MB limit.');
        setFile(null);
        return;
      }
      setError('');
      setFile(selected);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onUploadSuccess(response.data.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during upload.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-slate-800 rounded-xl shadow-lg border border-slate-700">
      <h2 className="text-2xl font-bold mb-4 text-center text-blue-400">Upload Your Resume</h2>
      <form onSubmit={handleUpload} className="space-y-4">
        <div className="flex items-center justify-center w-full">
          <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-slate-600 border-dashed rounded-lg cursor-pointer bg-slate-700 hover:bg-slate-600 hover:border-blue-500 transition-all">
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <svg className="w-8 h-8 mb-3 text-slate-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
              </svg>
              <p className="mb-2 text-sm text-slate-400"><span className="font-semibold">Click to upload</span> or drag and drop</p>
              <p className="text-xs text-slate-500">PDF or DOCX (MAX. 5MB)</p>
            </div>
            <input id="dropzone-file" type="file" className="hidden" accept=".pdf,.docx" onChange={handleFileChange} />
          </label>
        </div>
        
        {file && (
          <div className="text-sm text-green-400 text-center">
            Selected: {file.name}
          </div>
        )}
        
        {error && (
          <div className="text-sm text-red-400 text-center p-2 bg-red-900/30 rounded">
            {error}
          </div>
        )}

        <button 
          type="submit" 
          disabled={!file || uploading}
          className="w-full text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {uploading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </form>
    </div>
  );
}
