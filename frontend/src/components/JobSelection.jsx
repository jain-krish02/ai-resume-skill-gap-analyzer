import { useState, useEffect } from 'react';
import axios from 'axios';

export default function JobSelection({ onJobSelected, onCustomJobParsed }) {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState('predefined'); // 'predefined' or 'custom'
  const [customJD, setCustomJD] = useState('');
  const [processingCustom, setProcessingCustom] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const response = await axios.get('/api/job/');
        setRoles(response.data.data);
      } catch (err) {
        console.error("Failed to fetch roles:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRoles();
  }, []);

  const handlePredefinedSubmit = (e) => {
    e.preventDefault();
    if (selectedRole) {
      onJobSelected(selectedRole);
    }
  };

  const handleCustomSubmit = async (e) => {
    e.preventDefault();
    if (!customJD.trim()) return;
    
    setProcessingCustom(true);
    setError('');
    
    try {
      const response = await axios.post('/api/extract/', {
        text: customJD,
        type: 'job_description'
      });
      
      const extractedSkills = response.data?.data?.required_skills;
      if (!extractedSkills || !Array.isArray(extractedSkills) || extractedSkills.length === 0) {
        setError('Could not extract any skills from this description.');
        setProcessingCustom(false);
        return;
      }
      
      const customRoleData = {
        role_title: "Custom Role",
        required_skills: extractedSkills
      };
      
      onCustomJobParsed(customRoleData);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to process custom job description.");
    } finally {
      setProcessingCustom(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-slate-800 rounded-xl shadow-lg border border-slate-700 mt-6">
      <div className="flex mb-6 bg-slate-700 p-1 rounded-lg">
        <button 
          onClick={() => setMode('predefined')}
          className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${mode === 'predefined' ? 'bg-indigo-600 text-white shadow' : 'text-slate-300 hover:text-white'}`}
        >
          Select Role
        </button>
        <button 
          onClick={() => setMode('custom')}
          className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${mode === 'custom' ? 'bg-indigo-600 text-white shadow' : 'text-slate-300 hover:text-white'}`}
        >
          Paste Custom JD
        </button>
      </div>

      {mode === 'predefined' ? (
        loading ? (
          <div className="text-center text-slate-400 py-4">Loading roles...</div>
        ) : (
          <form onSubmit={handlePredefinedSubmit} className="space-y-4">
            <div>
              <label htmlFor="role" className="block mb-2 text-sm font-medium text-slate-300">Choose a Dream Job</label>
              <select
                id="role"
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="bg-slate-700 border border-slate-600 text-slate-200 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 outline-none"
                required
              >
                <option value="" disabled>Select a role...</option>
                {roles.map(role => (
                  <option key={role.role_id} value={role.role_id}>{role.role_title}</option>
                ))}
              </select>
            </div>
            
            <button 
              type="submit" 
              disabled={!selectedRole}
              className="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:outline-none focus:ring-indigo-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Compare with Resume
            </button>
          </form>
        )
      ) : (
        <form onSubmit={handleCustomSubmit} className="space-y-4">
          <div>
            <label htmlFor="customJD" className="block mb-2 text-sm font-medium text-slate-300">Paste Job Description</label>
            <textarea
              id="customJD"
              rows="5"
              value={customJD}
              onChange={(e) => setCustomJD(e.target.value)}
              placeholder="Paste the full text of the job posting here..."
              className="bg-slate-700 border border-slate-600 text-slate-200 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 outline-none"
              required
            ></textarea>
          </div>
          
          {error && <div className="text-red-400 text-xs">{error}</div>}
          
          <button 
            type="submit" 
            disabled={!customJD.trim() || processingCustom}
            className="w-full text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-4 focus:outline-none focus:ring-indigo-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {processingCustom ? 'Analyzing Description...' : 'Extract & Compare'}
          </button>
        </form>
      )}
    </div>
  );
}
