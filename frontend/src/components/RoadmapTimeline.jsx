export default function RoadmapTimeline({ roadmap }) {
  return (
    <div className="relative border-l border-slate-700 ml-4 mt-6">
      {roadmap.map((step, index) => (
        <div key={index} className="mb-10 ml-6 relative">
          {/* Timeline Node */}
          <span className={`absolute flex items-center justify-center w-8 h-8 rounded-full -left-10 ring-4 ring-slate-800 ${step.priority === 'Must-Have' ? 'bg-red-500/20 text-red-400 border border-red-500/50' : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/50'}`}>
            <span className="text-xs font-bold">{step.week}</span>
          </span>
          
          <div className="bg-slate-750 rounded-xl p-5 border border-slate-700 shadow-md hover:border-slate-600 transition-colors">
            <h4 className="flex items-center mb-1 text-lg font-semibold text-white">
              Learn {step.skill}
              {step.priority === 'Must-Have' && (
                <span className="bg-red-900/40 text-red-300 text-xs font-medium mr-2 px-2.5 py-0.5 rounded ml-3 border border-red-800">Critical</span>
              )}
            </h4>
            <p className="mb-4 text-sm font-normal text-slate-400">{step.description}</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              {/* Courses */}
              <div className="bg-slate-800 p-3 rounded-lg border border-slate-700">
                <h5 className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2 flex items-center">
                  <svg className="w-4 h-4 mr-1 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                  Recommended Courses
                </h5>
                <ul className="space-y-2">
                  {step.courses.map((course, i) => (
                    <li key={i}>
                      <a href={course.url} target="_blank" rel="noreferrer" className="text-sm text-blue-400 hover:text-blue-300 hover:underline flex items-start">
                        <span className="mr-1 mt-0.5 text-xs text-slate-500">[{course.platform}]</span>
                        {course.title}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
              
              {/* Projects */}
              <div className="bg-slate-800 p-3 rounded-lg border border-slate-700">
                <h5 className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2 flex items-center">
                  <svg className="w-4 h-4 mr-1 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
                  Practice Projects
                </h5>
                <ul className="space-y-2">
                  {step.projects.map((project, i) => (
                    <li key={i} className="text-sm text-slate-300 flex items-start">
                      <span className="text-emerald-500 mr-2">•</span>
                      {project}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
