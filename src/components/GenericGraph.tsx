import React, { useContext, useState, useMemo } from 'react';
import { Chart as ChartJS, registerables, ChartOptions, ChartTypeRegistry, ChartData } from 'chart.js';
import { DataContext } from '../contexts/DataContext';
import { ThemeContext } from '../contexts/ThemeContext';
import { getChartConfig, getSupportedCharts } from '../services/ChartRegistry';
import GenericChart from './GenericChart'; // Import the new component
import styles from './GenericGraph.module.css';

// Define ChartDataPoint interface if not already defined globally
interface ChartDataPoint {
  x: number;
  y: number;
  r?: number;
}

ChartJS.register(...registerables);

// Define color palettes
const lightThemePalette = ['#3b82f6', '#10b981', '#ef4444', '#f97316'];
const darkThemePalette = ['#60a5fa', '#34d399', '#f87171', '#fb923c'];

const getChartColors = (theme: string, count: number) => {
  const palette = theme === 'dark' ? darkThemePalette : lightThemePalette;
  return {
    backgroundColors: Array(count).fill(0).map((_, i) => palette[i % palette.length]),
    borderColors: Array(count).fill(0).map((_, i) => palette[i % palette.length])
  };
};

interface GenericGraphProps {
  initialChartType?: keyof ChartTypeRegistry; // Use keyof ChartTypeRegistry
  title?: string;
  data?: Record<string, unknown>[];
}

const GenericGraph: React.FC<GenericGraphProps> = ({
  initialChartType = 'bar',
  title,
  data
}) => {
  const [chartType, setChartType] = useState<keyof ChartTypeRegistry>(initialChartType); // Use keyof ChartTypeRegistry
  const { graphProcessedData, loading, error, graphGroupBy, xLabelKey } = useContext(DataContext);
  const { theme } = useContext(ThemeContext);

  // Use props data if provided, otherwise use context data
  const displayData = data || graphProcessedData || [];

  // Type the return value of useMemo explicitly
  const { chartData, options }: { chartData: ChartData<keyof ChartTypeRegistry>, options: ChartOptions<keyof ChartTypeRegistry> } = useMemo(() => {
    const config = getChartConfig(chartType); // Get config first

    // Handle case where config might be null/undefined if chartType is invalid
    if (!config) {
       // Return default empty chart data/options
       return {
         chartData: { labels: [], datasets: [] } as ChartData<keyof ChartTypeRegistry>, // Cast for type safety
         options: { responsive: true } as ChartOptions<keyof ChartTypeRegistry> // Cast for type safety
       };
    }

    // Define base options using optional chaining for safety
    const baseOptions: ChartOptions<keyof ChartTypeRegistry> = {
      responsive: true, // Default responsive
      ...(config.defaultConfig || {}), // Spread default config if exists
       plugins: {
        legend: { position: 'top' as const }, // Default legend position
        ...(config.defaultConfig?.plugins || {}), // Spread default plugins if exist
        title: { display: !!title, text: title || config.displayName || 'Chart' } // Use provided title or config display name
      },
      scales: {
        ...(config.defaultConfig?.scales || {}), // Spread default scales if exist
      }
    };
    // Removed stray defaultConfig block here

    // Special handling for bubble charts
    if (chartType === 'bubble') {
      const bubbleData = displayData.map((item: any) => ({ // Add type 'any' for now, refine if possible
        x: Number(item.x) || 0,
        y: Number(item.y) || 0,
        r: Number(item.r) || 5 // Default radius if 'r' is missing
      }));

      const bubbleChartData: ChartData<'bubble'> = {
        datasets: [{
          label: title || 'Bubble Dataset',
          data: bubbleData,
          backgroundColor: getChartColors(theme, 1).backgroundColors[0] // Use a single theme color
        }]
      };

      // Merge base options with bubble-specific options
      const bubbleOptions: ChartOptions<'bubble'> = {
        ...baseOptions, // Start with base options
        scales: { // Define scales specifically for bubble, overriding base if necessary
          x: {
            // ...(baseOptions.scales?.x || {}), // Don't spread base x if overriding type
            type: 'linear' as 'linear', // Explicitly set type as 'linear' for bubble
            position: 'bottom',
            title: { display: true, text: xLabelKey || 'X Axis' }
          },
          y: {
            // ...(baseOptions.scales?.y || {}), // Don't spread base y if overriding type
            type: 'linear' as 'linear', // Explicitly set type as 'linear' for bubble
            title: { display: true, text: 'Y Axis' }
          }
        },
         plugins: { // Ensure plugins are merged correctly
          ...(baseOptions.plugins || {}),
          title: { display: !!title, text: title || 'Bubble Chart' } // Override title if needed
        }
      };
      // Cast the return type for bubble chart specifically
      return { chartData: bubbleChartData as ChartData<keyof ChartTypeRegistry>, options: bubbleOptions as ChartOptions<keyof ChartTypeRegistry> };
    }

    // --- Logic for non-bubble charts ---
    const { backgroundColors, borderColors } = getChartColors(theme, displayData.length);

    // Find a key holding numeric data, excluding common non-data keys
    const numericKey = displayData.length > 0 ?
      Object.keys(displayData[0]).find(k => typeof displayData[0][k] === 'number' && !['id', 'year'].includes(k.toLowerCase())) :
      undefined; // Use undefined if no suitable key found

    // Prepare data for standard charts
    const standardChartData: ChartData<keyof ChartTypeRegistry> = {
      labels: displayData.map((item: any) => { // Add type 'any' for now
        if (xLabelKey && item[xLabelKey]) return String(item[xLabelKey]);
        if (item.label) return String(item.label); // Ensure label is string
        if (graphGroupBy?.length) {
          return graphGroupBy
            .filter((g: string) => g in item) // Add type 'string' to g
            .map((g: string) => String(item[g])) // Add type 'string' to g
            .join(' - ');
        }
        return 'Item'; // Default label
      }),
      datasets: [{
        label: title || (numericKey ? String(numericKey) : 'Value'), // Use numericKey if found, else 'Value'
        // Map data, using numericKey if found, otherwise try 'value', default to 0
        data: displayData.map((item: any) => { // Add type 'any' for now
          const keyToUse = numericKey || 'value'; // Prioritize numericKey, fallback to 'value'
          const value = Number(item[keyToUse]);
          return isNaN(value) ? 0 : value; // Default to 0 if not a number
        }),
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 1,
        // Example: Add fill property for line charts to make them area charts
        // fill: chartType === 'line' ? true : false, // Uncomment and adjust if needed
      }]
    };

    // Prepare options for standard charts, merging base and specific options
    const standardOptions: ChartOptions<keyof ChartTypeRegistry> = {
      ...baseOptions, // Start with base options
      // Determine indexAxis based on chart type (e.g., for horizontal bar)
      indexAxis: config.chartJsType === 'bar' && chartType.toLowerCase().includes('horizontal') ? 'y' : 'x',
      scales: {
        ...(baseOptions.scales || {}), // Keep existing base scales
        x: {
          ...(baseOptions.scales?.x || {}), // Keep existing x scale config
          // Apply stacking if it's a bar chart and type includes 'stacked'
          stacked: config.chartJsType === 'bar' && chartType.toLowerCase().includes('stacked'),
        },
        y: {
          ...(baseOptions.scales?.y || {}), // Keep existing y scale config
          // Apply stacking if it's a bar chart and type includes 'stacked'
          stacked: config.chartJsType === 'bar' && chartType.toLowerCase().includes('stacked'),
          // Example: Don't force y-axis to start at zero for horizontal bars
          beginAtZero: !(config.chartJsType === 'bar' && chartType.toLowerCase().includes('horizontal')),
        }
      },
       plugins: { // Ensure plugins are merged correctly
         ...(baseOptions.plugins || {}), // Keep base plugins
         title: { display: !!title, text: title || config.displayName || 'Chart' } // Ensure title is set
       }
    };

    return { chartData: standardChartData, options: standardOptions };

  }, [chartType, displayData, theme, title, xLabelKey, graphGroupBy]); // Ensure all dependencies are listed

  if (loading) return <div className={styles.loading}>Loading...</div>;
  if (error) return <div className={styles.error}>Error: {error}</div>;
  if (!displayData.length) return <div className={styles.error}>No data available</div>;

  const chartTypes = getSupportedCharts();
  // Get the config again here to access chartJsType for the GenericChart component
  const currentConfig = getChartConfig(chartType);
  // Determine the actual Chart.js type to pass down. Fallback to 'bar' if config is somehow undefined.
  const actualChartJsType = currentConfig?.chartJsType || 'bar';

  return (
    <div className={styles.container}>
      <div className={styles.controls}>
        <select
          value={chartType}
          // Ensure value is cast to the correct type
          onChange={e => setChartType(e.target.value as keyof ChartTypeRegistry)}
          className={styles.select}
        >
          {/* Ensure chartTypes includes the necessary info */}
          {chartTypes.map(typeInfo => (
            <option key={typeInfo.value} value={typeInfo.value}>{typeInfo.label}</option>
          ))}
        </select>
      </div>
      <div className={styles.chartWrapper}>
        {/* Use the new GenericChart component */}
        <GenericChart
          type={actualChartJsType} // Pass the correct Chart.js type
          data={chartData}
          options={options}
        />
      </div>
    </div>
  );
};

export default GenericGraph;
