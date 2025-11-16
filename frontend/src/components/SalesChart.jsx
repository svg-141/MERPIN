import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const SalesChart = ({ data }) => {
    // Asegurarse de que hay datos
    const chartData = data && data.length > 0 ? data : [
        { product: "Product A", revenue: 1000 },
        { product: "Product B", revenue: 2000 },
        { product: "Product C", revenue: 1500 }
    ]

    return (
        <div className="chart-card">
            <h3>Revenue by Product</h3>
            <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="product"
                            angle={-45}
                            textAnchor="end"
                            height={60}
                            fontSize={12}
                        />
                        <YAxis />
                        <Tooltip
                            formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']}
                        />
                        <Legend />
                        <Bar
                            dataKey="revenue"
                            fill="#8884d8"
                            name="Revenue"
                            radius={[4, 4, 0, 0]}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default SalesChart
