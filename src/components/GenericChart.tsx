import React, { useEffect, useRef } from 'react';
import { Chart as ChartJS, ChartData, ChartOptions, ChartTypeRegistry } from 'chart.js';

interface ChartProps {
  data: ChartData;
  options?: ChartOptions;
  type: keyof ChartTypeRegistry;
}

const GenericChart: React.FC<ChartProps> = ({ data, options, type }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstanceRef = useRef<ChartJS | null>(null);

  useEffect(() => {
    if (chartRef.current) {
      // Destroy previous chart instance if it exists
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }

      // Create new chart instance
      chartInstanceRef.current = new ChartJS(chartRef.current, {
        type,
        data,
        options
      });
    }

    // Cleanup function to destroy chart on unmount
    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
    };
  }, [data, options, type]);

  return <canvas ref={chartRef} />;
};


export default GenericChart;
