import { ChartOptions, ChartTypeRegistry } from 'chart.js';

interface ChartConfig {
  defaultConfig: ChartOptions;
  displayName: string;
  chartJsType: keyof ChartTypeRegistry;
}

const chartConfigs: Record<string, ChartConfig> = {
  bar: {
    displayName: 'Bar Chart',
    chartJsType: 'bar',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Bar Chart' }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  },
  line: { // Example: Add line config if missing
    displayName: 'Line Chart',
    chartJsType: 'line',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Line Chart' }
      },
      scales: {
        y: { beginAtZero: true }
      }
      // tension: 0.1 // Removed tension for now to fix type error
    }
  },
  pie: { // Example: Add pie config if missing
    displayName: 'Pie Chart',
    chartJsType: 'pie',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Pie Chart' }
      }
    }
  },
  doughnut: { // Example: Add doughnut config if missing
    displayName: 'Doughnut Chart',
    chartJsType: 'doughnut',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Doughnut Chart' }
      }
    }
  },
  radar: { // Example: Add radar config if missing
    displayName: 'Radar Chart',
    chartJsType: 'radar',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Radar Chart' }
      }
    }
  },
  polarArea: { // Example: Add polarArea config if missing
    displayName: 'Polar Area Chart',
    chartJsType: 'polarArea',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Polar Area Chart' }
      }
    }
  },
  bubble: { // Example: Add bubble config if missing
    displayName: 'Bubble Chart',
    chartJsType: 'bubble',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Bubble Chart' }
      },
       scales: { // Bubble needs specific scales
         x: { type: 'linear', position: 'bottom' },
         y: { type: 'linear' }
       }
    }
  },
  scatter: { // Example: Add scatter config if missing
    displayName: 'Scatter Chart',
    chartJsType: 'scatter',
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Scatter Chart' }
      },
       scales: { // Scatter needs specific scales
         x: { type: 'linear', position: 'bottom' },
         y: { type: 'linear' }
       }
    }
  },
  horizontalBar: { // Add horizontalBar config
    displayName: 'Horizontal Bar',
    chartJsType: 'bar', // Base type is 'bar'
    defaultConfig: {
      indexAxis: 'y', // Key difference for horizontal
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Horizontal Bar Chart' }
      },
      scales: {
        x: { beginAtZero: true } // Typically x-axis starts at zero
      }
    }
  },
  stackedBar: { // Add stackedBar config
    displayName: 'Stacked Bar',
    chartJsType: 'bar', // Base type is 'bar'
    defaultConfig: {
      responsive: true,
      plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Stacked Bar Chart' }
      },
      scales: {
        x: { stacked: true }, // Key difference for stacked
        y: { stacked: true, beginAtZero: true } // Key difference for stacked
      }
    }
  }
  // Ensure all types in CHART_TYPES have a corresponding config
};

// Updated getChartConfig to handle potential missing keys more gracefully
export const getChartConfig = (chartType: string): ChartConfig | undefined => {
  // First, check if the direct type exists (e.g., 'bar', 'line')
  if (chartConfigs[chartType]) {
    return chartConfigs[chartType];
  }
  // Handle custom types like 'horizontalBar', 'stackedBar'
  // This part might need adjustment based on how you want to handle unknown types
  // For now, returning undefined if not found directly. GenericGraph handles undefined config.
  return chartConfigs[chartType]; // Return the found config or undefined
};

// Keep only one definition of CHART_TYPES
export const CHART_TYPES = [
  'bar',
  'line',
  'pie',
  'doughnut',
  // 'area', // Area charts are line charts with fill: true, handle in component logic or add specific config
  'radar',
  'polarArea', // Added polarArea if needed
  'scatter', // Added scatter if needed
  'bubble',
  'horizontalBar',
  'stackedBar'
] as const;

export type ChartType = typeof CHART_TYPES[number];

export const CHART_CONFIGS: Record<ChartType, {displayName: string}> = {
  bar: {displayName: 'Bar Chart'},
  line: {displayName: 'Line Chart'},
  pie: {displayName: 'Pie Chart'},
  doughnut: {displayName: 'Doughnut Chart'},
  // area: {displayName: 'Area Chart'}, // Removed area as it's not a direct type
  radar: {displayName: 'Radar Chart'},
  polarArea: {displayName: 'Polar Area Chart'}, // Added polarArea
  scatter: {displayName: 'Scatter Chart'}, // Added scatter
  bubble: {displayName: 'Bubble Chart'},
  horizontalBar: {displayName: 'Horizontal Bar'},
  stackedBar: {displayName: 'Stacked Bar'}
};

export const getSupportedCharts = (): {value: ChartType, label: string, chartJsType: string}[] => {
  return CHART_TYPES.map(type => ({
    value: type,
    label: CHART_CONFIGS[type].displayName,
    chartJsType: type === 'horizontalBar' || type === 'stackedBar' ? 'bar' : type
  }));
};
