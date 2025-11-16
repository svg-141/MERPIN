import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const TimeSeriesChart = ({ data }) => {
    // Asegurarse de que hay datos
    const chartData = data && data.length > 0 ? data : [
        { date: "04/01", revenue: 1500 },
        { date: "04/02", revenue: 2300 },
        { date: "04/03", revenue: 1800 },
        { date: "04/04", revenue: 3200 },
        { date: "04/05", revenue: 2800 }
    ]

    return (
        <div className="chart-card">
            <h3>Daily Sales Trend</h3>
            <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip formatter={(value) => [`$${value}`, 'Revenue']} />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="revenue"
                            stroke="#8884d8"
                            strokeWidth={2}
                            name="Daily Revenue"
                            dot={{ fill: '#8884d8', strokeWidth: 2, r: 4 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default TimeSeriesChart
