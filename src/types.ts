export type ChartType = 
  | 'bar' | 'stackedBar' | 'line' | 'area' | 'stackedArea'
  | 'pie' | 'doughnut' | 'radar' | 'polarArea'
  | 'scatter' | 'bubble' | 'boxPlot' | 'heatmap'
  | 'candlestick' | 'ohlc' | 'choropleth' | 'bubbleMap';

export type FilterType = 
  | 'category' | 'value' | 'group' | 'stack'
  | 'xAxis' | 'yAxis' | 'series' | 'size'
  | 'color' | 'time' | 'range' | 'threshold';

export interface ChartData {
  [key: string]: any;
  id?: string;
}

export interface FilterState {
  activeFilters: string[];
  availableFilters: string[];
  incompatibleFilters: string[];
}
