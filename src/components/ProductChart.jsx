import React from 'react'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const ProductChart = ({ data }) => {
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D']

    // Asegurarse de que hay datos
    const chartData = data && data.length > 0 ? data : [
        { product: "Category A", revenue: 4000 },
        { product: "Category B", revenue: 3000 },
        { product: "Category C", revenue: 2000 },
        { product: "Category D", revenue: 1000 }
    ]

    return (
        <div className="chart-card">
            <h3>Sales Distribution</h3>
            <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                        <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ product, percent }) =>
                                `${product.substring(0, 12)}${product.length > 12 ? '...' : ''} (${(percent * 100).toFixed(0)}%)`
                            }
                            outerRadius={100}
                            fill="#8884d8"
                            dataKey="revenue"
                            nameKey="product"
                        >
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']} />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default ProductChart
