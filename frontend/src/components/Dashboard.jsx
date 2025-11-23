import React, { useState, useMemo } from 'react'
import SalesChart from './SalesChart'
import ProductChart from './ProductChart'
import TimeSeriesChart from './TimeSeriesChart'
import MetricsCard from './MetricsCard'
import JobsSection from './JobsSection'
import FileUpload from './FileUpload' // Import the new component
import { salesData } from '../data/salesData'

const Dashboard = () => {
  const [selectedView, setSelectedView] = useState('overview')

  const handleExport = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/export/');
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'sales_report.xlsx';
        document.body.appendChild(a);
        a.click();
        a.remove();
      } else {
        console.error('Export failed');
      }
    } catch (error) {
      console.error('Error exporting data:', error);
    }
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <h1>Electronics Store Dashboard</h1>
        <div className="header-actions">
          <button className="btn-primary" onClick={handleExport}>Export Report</button>
        </div>
      </header>

      {/* File Upload Section */}
      <div className="upload-section">
        <FileUpload />
      </div>

      {/* Métricas principales */}
      <div className="metrics-grid">
        <MetricsCard
          title="Total Revenue"
          value="$125,430"
          change="+15.95%"
          changeType="positive"
          icon="💰"
        />
        <MetricsCard
          title="Total Orders"
          value="1,847"
          change="+3.13%"
          changeType="positive"
          icon="📦"
        />
        <MetricsCard
          title="Products Sold"
          value="4,592"
          change="+5.37%"
          changeType="positive"
          icon="📱"
        />
        <MetricsCard
          title="Avg Order Value"
          value="$67.89"
          change="+2.45%"
          changeType="positive"
          icon="📊"
        />
      </div>

      {/* Sección principal con gráficos y jobs */}
      <div className="main-content">
        <div className="charts-section">
          {/* Navegación */}
          <div className="view-navigation">
            <button 
              className={`nav-btn ${selectedView === 'overview' ? 'active' : ''}`}
              onClick={() => setSelectedView('overview')}
            >
              📈 Sales Overview
            </button>
            <button 
              className={`nav-btn ${selectedView === 'products' ? 'active' : ''}`}
              onClick={() => setSelectedView('products')}
            >
              📱 Products Analysis
            </button>
            <button 
              className={`nav-btn ${selectedView === 'timeline' ? 'active' : ''}`}
              onClick={() => setSelectedView('timeline')}
            >
              ⏰ Sales Timeline
            </button>
          </div>

          {/* Gráficos */}
          <div className="charts-container">
            {selectedView === 'overview' && (
              <div className="chart-row">
                <SalesChart data={[
                  { product: "iPhone", revenue: 12000 },
                  { product: "Samsung Galaxy", revenue: 8000 },
                  { product: "MacBook Pro", revenue: 25000 },
                  { product: "iPad", revenue: 6000 },
                  { product: "AirPods", revenue: 3000 }
                ]} />
                <ProductChart data={[
                  { product: "iPhone", revenue: 12000 },
                  { product: "Samsung", revenue: 8000 },
                  { product: "MacBook", revenue: 25000 },
                  { product: "iPad", revenue: 6000 },
                  { product: "AirPods", revenue: 3000 }
                ]} />
              </div>
            )}
            
            {selectedView === 'products' && (
              <div className="chart-full">
                <SalesChart data={[
                  { product: "iPhone 13", revenue: 12000 },
                  { product: "Samsung Galaxy S21", revenue: 8000 },
                  { product: "MacBook Pro M1", revenue: 25000 },
                  { product: "iPad Air", revenue: 6000 },
                  { product: "AirPods Pro", revenue: 3000 },
                  { product: "Apple Watch", revenue: 4500 },
                  { product: "Google Pixel", revenue: 3500 },
                  { product: "Surface Laptop", revenue: 18000 }
                ]} />
              </div>
            )}
            
            {selectedView === 'timeline' && (
              <div className="chart-full">
                <TimeSeriesChart data={[
                  { date: "04/01", revenue: 1500 },
                  { date: "04/02", revenue: 2300 },
                  { date: "04/03", revenue: 1800 },
                  { date: "04/04", revenue: 3200 },
                  { date: "04/05", revenue: 2800 },
                  { date: "04/06", revenue: 1900 },
                  { date: "04/07", revenue: 2600 }
                ]} />
              </div>
            )}
          </div>
        </div>

        {/* Sección Jobs (sidebar) */}
        <JobsSection />
      </div>
    </div>
  )
}

export default Dashboard
