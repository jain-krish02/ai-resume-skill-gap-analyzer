import { useState } from 'react';
import axios from 'axios';
import UploadForm from './components/UploadForm';
import JobSelection from './components/JobSelection';
import Dashboard from './components/Dashboard';

function App() {
  const [resumeData, setResumeData] = useState(null);
  const [candidateSkills, setCandidateSkills] = useState([]);
  const [targetRoleId, setTargetRoleId] = useState(null);
  const [targetRoleData, setTargetRoleData] = useState(null);
  const [gapReport, setGapReport] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState('');

  const handleUploadSuccess = async (data) => {
    setResumeData(data);
    setLoadingStep('Extracting skills from resume...');
    try {
      const response = await axios.post('/api/extract/', {
        text: data.raw_text,
        type: 'resume'
      });
      const extractedData = response.data.data;
      const allSkills = [
        ...(extractedData.skills || []),
        ...(extractedData.tools || []),
        ...(extractedData.education || []).map(edu => ({ name: edu, category: 'Education' }))
      ];
      setCandidateSkills(allSkills);
    } catch (err) {
      setError("Failed to extract skills from resume.");
    } finally {
      setLoadingStep('');
    }
  };

  const handleJobSelected = async (roleId) => {
    setTargetRoleId(roleId);
    setLoadingStep('Fetching role requirements...');
    try {
      // Fetch role skills
      const roleResponse = await axios.get(`/api/job/${roleId}/skills`);
      await processAnalysis(roleResponse.data.data, roleId);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred during analysis.");
      setLoadingStep('');
    }
  };

  const handleCustomJobParsed = async (customRoleData) => {
    setTargetRoleId('custom');
    await processAnalysis(customRoleData, 'custom');
  };

  const processAnalysis = async (roleData, roleId) => {
    try {
      setTargetRoleData(roleData);
      
      setLoadingStep('Analyzing skill gap...');
      // Gap Analysis
      const gapResponse = await axios.post('/api/gap/', {
        candidate_skills: candidateSkills,
        target_role_id: roleData.role_title === "Custom Role" ? "custom" : roleId,
        custom_requirements: roleData.role_title === "Custom Role" ? roleData.required_skills : null
      });
      const gapData = gapResponse.data.data;
      setGapReport(gapData);
      
      setLoadingStep('Generating learning roadmap...');
      // Roadmap Generation
      const roadmapResponse = await axios.post('/api/roadmap/', {
        missing_must_have: gapData.missing_must_have,
        missing_good_to_have: gapData.missing_good_to_have
      });
      setRoadmap(roadmapResponse.data.data);

    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred during analysis.");
    } finally {
      setLoadingStep('');
    }
  };

  const resetSession = () => {
    setResumeData(null);
    setCandidateSkills([]);
    setTargetRoleId(null);
    setTargetRoleData(null);
    setGapReport(null);
    setRoadmap(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 font-sans">
      <header className="bg-slate-800 border-b border-slate-700 py-4 shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 flex justify-between items-center">
          <h1 className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
            AI Resume Skill Gap Analyzer
          </h1>
          {resumeData && (
            <button 
              onClick={resetSession}
              className="text-sm px-4 py-2 text-slate-300 hover:text-white bg-slate-700 hover:bg-slate-600 rounded transition-colors"
            >
              Start Over
            </button>
          )}
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-900/40 border border-red-700 rounded-lg text-red-200">
            <p className="font-semibold">Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}
        
        {loadingStep && (
          <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-2xl flex flex-col items-center">
              <div className="w-12 h-12 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mb-4"></div>
              <p className="text-lg font-medium text-slate-200 animate-pulse">{loadingStep}</p>
            </div>
          </div>
        )}

        {!resumeData ? (
          <div className="flex flex-col items-center justify-center mt-12 animate-fade-in">
            <div className="text-center mb-10 max-w-2xl">
              <h2 className="text-4xl font-bold mb-4 text-white tracking-tight">Find your missing skills</h2>
              <p className="text-slate-400 text-lg">Upload your resume and compare it against your dream job to generate a personalized learning roadmap.</p>
            </div>
            <UploadForm onUploadSuccess={handleUploadSuccess} />
          </div>
        ) : !targetRoleId ? (
          <div className="animate-fade-in max-w-2xl mx-auto">
             <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-md mb-8">
              <div className="flex items-center space-x-3 text-green-400 mb-2">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <h2 className="text-xl font-bold">Resume Uploaded Successfully</h2>
              </div>
              <p className="text-slate-300 text-sm">Extracted {candidateSkills.length} skills from your resume.</p>
            </div>
            <JobSelection onJobSelected={handleJobSelected} onCustomJobParsed={handleCustomJobParsed} />
          </div>
        ) : (gapReport && roadmap) ? (
          <Dashboard 
            resumeData={resumeData} 
            candidateSkills={candidateSkills}
            targetRole={targetRoleData}
            gapReport={gapReport}
            roadmap={roadmap}
          />
        ) : null}
      </main>
    </div>
  );
}

export default App;
