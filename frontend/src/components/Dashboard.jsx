import axios from 'axios';
import { useState } from 'react';
import GapReportCard from './GapReportCard';
import RoadmapTimeline from './RoadmapTimeline';

export default function Dashboard({ resumeData, candidateSkills, targetRole, gapReport, roadmap }) {
  const [exporting, setExporting] = useState(false);

  const getScoreColor = (score) => {
    if (score >= 80) return "text-green-400";
    if (score >= 50) return "text-yellow-400";
    return "text-red-400";
  };

  const getScoreRing = (score) => {
    if (score >= 80) return "border-green-500";
    if (score >= 50) return "border-yellow-500";
    return "border-red-500";
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const payload = {
        target_role: targetRole?.role_title || "Custom Role",
        match_score: gapReport.match_score,
        missing_must_have: gapReport.missing_must_have,
        missing_good_to_have: gapReport.missing_good_to_have,
        overlapping: gapReport.overlapping,
        roadmap: roadmap
      };
      
      const response = await axios.post('http://localhost:8000/api/export/', payload, {
        responseType: 'blob', // Important for file download
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'AI_Skill_Gap_Report.pdf');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      alert("Failed to export PDF.");
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="animate-fade-in space-y-8">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row justify-between items-center bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-lg">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Analysis Results</h2>
          <p className="text-slate-400">Target Role: <span className="text-indigo-400 font-semibold">{targetRole?.role_title}</span></p>
        </div>
        
        <div className="mt-4 md:mt-0 flex items-center space-x-6">
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm text-slate-400">Match Score</p>
              <p className={`text-3xl font-black ${getScoreColor(gapReport.match_score)}`}>{gapReport.match_score}%</p>
            </div>
            <div className={`w-16 h-16 rounded-full border-4 flex items-center justify-center bg-slate-900 ${getScoreRing(gapReport.match_score)}`}>
              <span className={`text-xl font-bold ${getScoreColor(gapReport.match_score)}`}>{Math.round(gapReport.match_score)}</span>
            </div>
          </div>
          
          <button 
            onClick={handleExport}
            disabled={exporting}
            className="flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white rounded-lg transition-colors font-medium text-sm"
          >
            {exporting ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                Exporting...
              </>
            ) : (
              <>
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Export PDF
              </>
            )}
          </button>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Gap Report */}
        <div className="lg:col-span-1 space-y-6">
          <GapReportCard gapReport={gapReport} />
        </div>
        
        {/* Right Column: Roadmap */}
        <div className="lg:col-span-2">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 shadow-lg p-6">
            <h3 className="text-xl font-bold text-white mb-6 border-b border-slate-700 pb-3 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
              Your Personalized Roadmap
            </h3>
            
            {roadmap.length > 0 ? (
              <RoadmapTimeline roadmap={roadmap} />
            ) : (
              <div className="text-center py-12">
                <div className="inline-block p-4 bg-green-900/30 rounded-full mb-4">
                  <svg className="w-10 h-10 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <h4 className="text-xl font-bold text-white mb-2">You're fully qualified!</h4>
                <p className="text-slate-400">Your resume already covers all the skills required for this role.</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
