import React, { useContext } from 'react';
import GenericGraph from './GenericGraph';
import DataTable from './DataTable';
import GraphFilterColumn from './GraphFilterColumn';
import ErrorBoundary from './ErrorBoundary';
import ThemeToggle from './ThemeToggle';
import { DataContext } from '../contexts/DataContext';
import styles from '../App.module.css'; // Reuse App styles for now

// This component now holds the content previously in AppContent
const DashboardView: React.FC = () => {
  const { 
    loading, 
    error, 
    processedData,
    graphGroupBy,
    setGraphGroupBy,
    allColumns
  } = useContext(DataContext);

  // Handle Loading and Error States centrally for the dashboard
  if (loading) {
    return <div className={styles.loadingState}>Loading Dashboard Data...</div>;
  }

  if (error) {
    return <div className={styles.errorState} role="alert">Failed to load dashboard data: {error}</div>;
  }

  if (!processedData || processedData.length === 0) {
      return <div className={styles.loadingState}>No data available for dashboard.</div>;
  }

  // TODO: Implement ChartGrid and independent fetching later
  // For now, render a single graph and the table as before, but using processedData

  return (
    <div className={styles.dashboardContainer}>
      <div className={styles.dashboardHeader}>
        <h2>Data Dashboard</h2>
        <ThemeToggle />
      </div>

      <div className={styles.dashboardContent}>
        <ErrorBoundary>
          <div className={styles.visualizationSection}>
            <GenericGraph
              title="Data Overview"
              data={processedData}
            />
          </div>
        </ErrorBoundary>

        <ErrorBoundary>
          <div className={styles.dataSection}>
            <DataTable 
              data={processedData}
              showFilters={true}
              showGroupBy={true}
              showGraphFilters={true}
            />
          </div>
        </ErrorBoundary>
      </div>
    </div>
  );
};

export default DashboardView;
