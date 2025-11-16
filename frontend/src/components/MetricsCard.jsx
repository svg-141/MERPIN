import React from 'react'

const MetricsCard = ({ title, value, change, changeType, icon }) => {
    return (
        <div className="metrics-card">
            <div className="metrics-header">
                <div className="metrics-icon">{icon}</div>
                <div className="metrics-trend">
                    <span className={`trend ${changeType}`}>
                        {change}
                    </span>
                    <span className="trend-label">last month</span>
                </div>
            </div>
            <div className="metrics-content">
                <h2 className="metrics-value">{value}</h2>
                <p className="metrics-title">{title}</p>
            </div>
        </div>
    )
}

export default MetricsCard
