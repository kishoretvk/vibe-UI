import React, { useContext, useState } from 'react';
import { WidthProvider, Responsive } from 'react-grid-layout';
import MetricsContext from '../contexts/MetricsContext';
import GenericGraph from './GenericGraph';
import DataTable from './DataTable';
import styles from './MetricsExplorerView.module.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const MetricsExplorerView: React.FC = () => {
  const { charts, toggleExpand, refreshChart } = useContext(MetricsContext);

  const [layouts, setLayouts] = useState(() => {
    const savedLayout = localStorage.getItem('metricsGridLayout');
    if (savedLayout) {
      return JSON.parse(savedLayout);
    }
    return {
      lg: charts.map((chart, i) => ({
        i: chart.id,
        x: (i % 4) * 3,
        y: Math.floor(i / 4) * 2,
        w: 3,
        h: chart.isExpanded ? 2 : 1,
        minW: 2,
        minH: 1
      }))
    };
  });

  const onLayoutChange = (currentLayout: any, allLayouts: any) => {
    setLayouts(allLayouts);
    localStorage.setItem('metricsGridLayout', JSON.stringify(allLayouts));
  };

  return (
    <div className={styles.explorerContainer}>
      <ResponsiveGridLayout
        className="layout"
        layouts={layouts}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480 }}
        cols={{ lg: 12, md: 10, sm: 6, xs: 4 }}
        rowHeight={180}
        margin={[15, 15]}
        containerPadding={[15, 15]}
        compactType={null}
        isDraggable={true}
        isResizable={true}
        onLayoutChange={onLayoutChange}
      >
        {charts.map((chart) => (
          <div 
            key={chart.id}
            className={`${styles.chartTile} ${chart.isExpanded ? styles.expanded : ''}`}
            data-grid={{
              x: (charts.findIndex(c => c.id === chart.id) % 4) * 3,
              y: Math.floor(charts.findIndex(c => c.id === chart.id) / 4) * 2,
              w: 3,
              h: chart.isExpanded ? 2 : 1,
              minW: 2,
              minH: 1
            }}
          >
            <div 
              className={styles.tileHeader}
              onClick={() => toggleExpand(chart.id)}
            >
              <span className={styles.expandIndicator}>
                {chart.isExpanded ? '▼' : '►'}
              </span>
            </div>

            {chart.isExpanded && (
              <div className={styles.tileContent}>
                {chart.isLoading ? (
                  <div className={styles.loading}>Loading chart...</div>
                ) : chart.error ? (
                  <div className={styles.error}>{chart.error}</div>
                ) : (
                  <>
                    <div className={styles.chartContainer}>
                      <GenericGraph
                        initialChartType={chart.chartType}
                        title={chart.title}
                        data={chart.data}
                      />
                    </div>
                    <div className={styles.tableContainer}>
                      <DataTable data={[]} />
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        ))}
      </ResponsiveGridLayout>
    </div>
  );
};

export default MetricsExplorerView;
