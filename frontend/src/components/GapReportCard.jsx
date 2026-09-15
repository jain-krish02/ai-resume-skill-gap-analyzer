export default function GapReportCard({ gapReport }) {
  return (
    <div className="bg-slate-800 rounded-2xl border border-slate-700 shadow-lg overflow-hidden flex flex-col h-full">
      <div className="p-4 bg-slate-750 border-b border-slate-700">
        <h3 className="text-lg font-bold text-white flex items-center">
          <svg className="w-5 h-5 mr-2 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
          Skill Gap Summary
        </h3>
      </div>
      
      <div className="p-6 space-y-6 flex-grow">
        {/* Missing Must-Have */}
        <div>
          <h4 className="text-sm uppercase tracking-wider font-semibold text-red-400 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            Critical Missing Skills
          </h4>
          {gapReport.missing_must_have.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {gapReport.missing_must_have.map((skill, i) => (
                <span key={i} className="px-3 py-1 bg-red-900/30 text-red-300 border border-red-800 rounded-full text-sm font-medium">
                  {skill.skill_name}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400 italic">None! You have all the critical skills.</p>
          )}
        </div>
        
        {/* Missing Good-To-Have */}
        <div>
          <h4 className="text-sm uppercase tracking-wider font-semibold text-yellow-400 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            Good-To-Have Missing
          </h4>
          {gapReport.missing_good_to_have.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {gapReport.missing_good_to_have.map((skill, i) => (
                <span key={i} className="px-3 py-1 bg-yellow-900/30 text-yellow-300 border border-yellow-800 rounded-full text-sm font-medium">
                  {skill.skill_name}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400 italic">None missing.</p>
          )}
        </div>
        
        {/* Overlapping */}
        <div>
          <h4 className="text-sm uppercase tracking-wider font-semibold text-green-400 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
            Matching Skills
          </h4>
          {gapReport.overlapping.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {gapReport.overlapping.map((skill, i) => (
                <span key={i} className="px-3 py-1 bg-green-900/30 text-green-300 border border-green-800 rounded-full text-sm font-medium">
                  {skill.skill_name}
                </span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400 italic">No exact matches found.</p>
          )}
        </div>
      </div>
    </div>
  );
}
