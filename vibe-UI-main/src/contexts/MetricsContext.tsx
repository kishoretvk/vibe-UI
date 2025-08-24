import React, { createContext, useState, ReactNode, useMemo } from 'react';
import { ChartTypeRegistry } from 'chart.js'; // Import ChartTypeRegistry

interface ChartConfig {
  id: string;
  chartType: keyof ChartTypeRegistry; // Use keyof ChartTypeRegistry
  title: string;
  isLoading: boolean;
  error: string | null;
  isExpanded: boolean;
  data: Record<string, unknown>[];
}

const CHART_TYPES = [
  'bar',
  'line', 
  'pie',
  'doughnut',
  // 'area', // Area charts are typically line charts with fill: true
  'radar',
  'polarArea',
  'scatter',
  'bubble'
] as const satisfies ReadonlyArray<keyof ChartTypeRegistry>; // Ensure types are valid keys ('area' removed)

interface MetricsContextType {
  charts: ChartConfig[];
  toggleExpand: (id: string) => void;
  refreshChart: (id: string) => void;
  loading: boolean;
}

const createDefaultCharts = async () => {
  try {
    const response = await fetch('http://localhost:5001/api/data');
    if (!response.ok) throw new Error('Failed to fetch initial data');
    const data = await response.json();
    
    return CHART_TYPES.map((type, index) => ({
      id: `${type}${index+1}`,
      chartType: type,
      title: `${type.charAt(0).toUpperCase() + type.slice(1)} Chart ${index+1}`,
      isExpanded: true,
      isLoading: false,
      error: null,
      data: data
    }));
  } catch (error) {
    console.error("Error loading initial chart data:", error);
    return CHART_TYPES.map((type, index) => ({
      id: `${type}${index+1}`,
      chartType: type,
      title: `${type.charAt(0).toUpperCase() + type.slice(1)} Chart ${index+1}`,
      isExpanded: true,
      isLoading: false,
      error: error instanceof Error ? error.message : 'Failed to load data',
      data: []
    }));
  }
};

const MetricsContext = createContext<MetricsContextType>({
  charts: [],
  toggleExpand: () => {},
  refreshChart: () => {},
  loading: true
});

export const MetricsProvider: React.FC<{children: ReactNode}> = ({ children }) => {
  const [charts, setCharts] = useState<ChartConfig[]>([]);
  const [loading, setLoading] = useState(true);

  // Initialize charts from API
  React.useEffect(() => {
    const initializeCharts = async () => {
      try {
        const savedCharts = localStorage.getItem('metricsCharts');
        const savedLayout = localStorage.getItem('metricsLayoutPositions');
        
        if (savedCharts && savedLayout) {
          const parsedCharts = JSON.parse(savedCharts);
          const parsedLayout = JSON.parse(savedLayout);
          setCharts(parsedCharts);
        } else {
          const initialCharts = await createDefaultCharts();
          setCharts(initialCharts);
        }
      } catch (error) {
        console.error("Error initializing charts:", error);
      } finally {
        setLoading(false);
      }
    };

    initializeCharts();
  }, []);

  const toggleExpand = (id: string) => {
    setCharts(prev => {
      const updated = prev.map(chart => 
        chart.id === id ? {...chart, isExpanded: !chart.isExpanded} : chart
      );
      
      // Save both charts data and layout positions
      localStorage.setItem('metricsCharts', JSON.stringify(updated));
      
      const layoutPositions = prev.reduce((acc, chart) => ({
        ...acc,
        [chart.id]: {
          isExpanded: chart.id === id ? !chart.isExpanded : chart.isExpanded
        }
      }), {});
      
      localStorage.setItem('metricsLayoutPositions', JSON.stringify(layoutPositions));
      return updated;
    });
  };

  const refreshChart = async (id: string) => {
    setCharts(prev => {
      const updated = prev.map(chart => 
        chart.id === id ? {...chart, isLoading: true, error: null} : chart
      );
      localStorage.setItem('metricsLayout', JSON.stringify(updated));
      return updated;
    });

    try {
      const response = await fetch(`http://localhost:5001/api/data`);
      if (!response.ok) throw new Error('Failed to fetch data');
      
      const data = await response.json();
      setCharts(prev => prev.map(chart => 
        chart.id === id ? {
          ...chart,
          isLoading: false,
          data: data
        } : chart
      ));
    } catch (error) {
      setCharts(prev => prev.map(chart => 
        chart.id === id ? {
          ...chart,
          isLoading: false,
          error: 'Failed to load data'
        } : chart
      ));
    }
  };

  const value = useMemo(() => ({
    charts,
    toggleExpand,
    refreshChart,
    loading
  }), [charts, loading]);

  return (
    <MetricsContext.Provider value={value}>
      {children}
    </MetricsContext.Provider>
  );
};

export default MetricsContext;
