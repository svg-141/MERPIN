import React from 'react'

const JobsSection = () => {
    const jobsData = [
        {
            position: "PHP Development Engineer",
            posted: "24/01/2012",
            education: "Undergraduate",
            location: "Finland",
            experience: "Yes"
        },
        {
            position: "UI Designer",
            posted: "24/01/2012",
            education: "Undergraduate",
            location: "Italy",
            experience: "Yes"
        },
        {
            position: "Java Senior R&D Engineer",
            posted: "20/01/2012",
            education: "Postgraduate",
            location: "Japan",
            experience: "No"
        }
    ]

    return (
        <div className="jobs-section">
            {/* Job Summary */}
            <div className="job-summary-card">
                <h3>Job Summary</h3>
                <div className="summary-content">
                    <div className="summary-chart">
                        <div className="chart-circle">
                            <div className="chart-progress" style={{ '--progress': '32%' }}></div>
                            <span>32%</span>
                        </div>
                    </div>
                    <div className="summary-stats">
                        <div className="stat">
                            <span className="stat-label">Job Posted</span>
                            <span className="stat-value">32%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Jobs List */}
            <div className="jobs-list-card">
                <h3>List of Posted Jobs</h3>
                <div className="jobs-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Position</th>
                                <th>Posted</th>
                                <th>Education</th>
                                <th>Location</th>
                                <th>Experience</th>
                            </tr>
                        </thead>
                        <tbody>
                            {jobsData.map((job, index) => (
                                <tr key={index}>
                                    <td>{job.position}</td>
                                    <td>{job.posted}</td>
                                    <td>{job.education}</td>
                                    <td>{job.location}</td>
                                    <td>{job.experience}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}

export default JobsSection
