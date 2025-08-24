export const CHART_TYPES = [
  'bar',
  'line',
  'pie',
  'doughnut',
  'area',
  'radar',
  'bubble',
  'horizontalBar',
  'stackedBar'
] as const;

export type ChartType = typeof CHART_TYPES[number];

export interface ChartConfig {
  displayName: string;
  icon: string;
}

export const CHART_CONFIGS: Record<ChartType, ChartConfig> = {
  bar: { displayName: 'Bar Chart', icon: 'bar_chart' },
  line: { displayName: 'Line Chart', icon: 'show_chart' },
  pie: { displayName: 'Pie Chart', icon: 'bar_chart' },
  doughnut: { displayName: 'Doughnut Chart', icon: 'donut_small' },
  area: { displayName: 'Area Chart', icon: 'area_chart' },
  radar: { displayName: 'Radar Chart', icon: 'radar' },
  bubble: { displayName: 'Bubble Chart', icon: 'bubble_chart' },
  horizontalBar: { displayName: 'Horizontal Bar', icon: 'horizontal_bar' },
  stackedBar: { displayName: 'Stacked Bar', icon: 'stacked_bar' }
};

export function getSupportedCharts(): ChartType[] {
  return [...CHART_TYPES];
