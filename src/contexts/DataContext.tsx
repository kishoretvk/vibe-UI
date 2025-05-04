import React, { createContext, useState, useEffect, useCallback, ReactNode, Dispatch, SetStateAction, useMemo } from 'react';

export type DataItem = Record<string, any>;
type Filters = Record<string, string | undefined>; // Allow undefined to clear filter
type GroupBy = string[]; // Array of column names to group by

interface IDataContext {
  data: DataItem[];
  loading: boolean;
  error: string | null;
  filters: Filters;
  groupBy: GroupBy;
  graphGroupBy: GroupBy; // New graph-specific filters
  allColumns: string[];
  processedData: DataItem[];
  graphProcessedData: DataItem[]; // Processed data for graph
  setFilters: Dispatch<SetStateAction<Filters>>;
  setGroupBy: Dispatch<SetStateAction<GroupBy>>;
  setGraphGroupBy: Dispatch<SetStateAction<GroupBy>>;
  refetchData: () => void;
  xLabelKey: string;
  yLabelKey: string;
}

// Provide default values matching the interface
const defaultState: IDataContext = {
  data: [],
  loading: true,
  error: null,
  filters: {},
  groupBy: [],
  graphGroupBy: [],
  allColumns: [],
  processedData: [],
  graphProcessedData: [],
  setFilters: () => {},
  setGroupBy: () => {},
  setGraphGroupBy: () => {},
  refetchData: () => {},
  xLabelKey: '',
  yLabelKey: '',
};

export const DataContext = createContext<IDataContext>(defaultState);

interface DataProviderProps {
  children: ReactNode;
  xLabelKey: string;
  yLabelKey: string; // Passed in props, but maybe not needed in context if graph is self-sufficient? Keep for now.
}

const API_URL = 'http://localhost:5001/api/data';

// Helper function to get the first numeric key (excluding id/year)
const getNumericKey = (item: DataItem): string | null => {
  if (!item) return null;
  for (const k in item) {
    if (typeof item[k] === 'number' && k !== 'id' && k !== 'year') {
      return k;
    }
  }
  return null; // Or a default like 'value' if guaranteed
};

export const DataProvider: React.FC<DataProviderProps> = ({ children, xLabelKey, yLabelKey }) => {
  const [data, setData] = useState<DataItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>({});
  const [groupBy, setGroupBy] = useState<GroupBy>([]);
  const [graphGroupBy, setGraphGroupBy] = useState<GroupBy>([]);
  const [allColumns, setAllColumns] = useState<string[]>([]);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(API_URL);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result: DataItem[] = await response.json();
      setData(result);
      // Determine all unique columns from the fetched data
      if (result.length > 0) {
        const columns = Object.keys(result[0]);
        setAllColumns(columns);
      } else {
          setAllColumns([]);
      }
    } catch (e: any) {
      console.error("Failed to fetch data:", e);
      setError(e.message || "Failed to fetch data. Is the backend running?");
      setData([]); // Clear data on error
      setAllColumns([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Calculate processed data based on filters and groupBy
  const processedData = useMemo(() => {
    let resultData = [...data]; // Start with raw data

    // Apply filters
    const activeFilters = Object.entries(filters).filter(([, value]) => value !== undefined && value !== '');
    if (activeFilters.length > 0) {
      resultData = resultData.filter(item => {
        return activeFilters.every(([key, filterValue]) => {
          const itemValue = item[key];
          // Basic case-insensitive string filtering
          return String(itemValue).toLowerCase().includes(String(filterValue).toLowerCase());
        });
      });
    }

    // Apply grouping and aggregation
    if (groupBy.length > 0 && resultData.length > 0) {
      const numericKey = getNumericKey(resultData[0]); // Find the key to aggregate
      if (!numericKey) {
        console.warn("Cannot group: No numeric key found for aggregation.");
        return resultData; // Return filtered data if no key to aggregate
      }

      const grouped: Record<string, { groupKeys: Record<string, any>, sum: number, count: number }> = {};

      resultData.forEach(item => {
        const groupKeyString = groupBy.map(key => item[key]).join(' | '); // Create a unique key string for the group
        
        if (!grouped[groupKeyString]) {
          grouped[groupKeyString] = { 
            groupKeys: groupBy.reduce((acc, key) => ({ ...acc, [key]: item[key] }), {}), 
            sum: 0, 
            count: 0 
          };
        }
        
        grouped[groupKeyString].sum += (item[numericKey] as number) || 0;
        grouped[groupKeyString].count += 1;
      });

      // Transform grouped data into DataItem[] format suitable for the graph
      // Using 'label' and 'value' for simplicity in the graph component
      resultData = Object.entries(grouped).map(([keyString, groupData]) => ({
        // Include original group keys for potential tooltips or richer labels
        ...groupData.groupKeys, 
        // Create a combined label for the graph axis
        label: keyString, 
        // Use the aggregated sum as the primary value for the graph
        value: groupData.sum, 
        // Could also include average: groupData.sum / groupData.count
        // Could also include count: groupData.count
      }));
       // Now, the numeric key for the graph will be 'value'
    }

    return resultData;
  }, [data, filters, groupBy]);


  // Process data specifically for graph with graphGroupBy
  const graphProcessedData = useMemo(() => {
    let resultData = [...data];
    
    // Apply filters
    const activeFilters = Object.entries(filters).filter(([, value]) => value !== undefined && value !== '');
    if (activeFilters.length > 0) {
      resultData = resultData.filter(item => {
        return activeFilters.every(([key, filterValue]) => {
          const itemValue = item[key];
          return String(itemValue).toLowerCase().includes(String(filterValue).toLowerCase());
        });
      });
    }

    // Apply graph-specific grouping
    if (graphGroupBy.length > 0 && resultData.length > 0) {
      const numericKey = getNumericKey(resultData[0]);
      if (!numericKey) return resultData;

      const grouped: Record<string, { groupKeys: Record<string, any>, sum: number }> = {};
      
      resultData.forEach(item => {
        const groupKeyString = graphGroupBy.map(key => item[key]).join(' | ');
        if (!grouped[groupKeyString]) {
          grouped[groupKeyString] = { 
            groupKeys: graphGroupBy.reduce((acc, key) => ({ ...acc, [key]: item[key] }), {}),
            sum: 0
          };
        }
        grouped[groupKeyString].sum += (item[numericKey] as number) || 0;
      });

      resultData = Object.entries(grouped).map(([keyString, groupData]) => ({
        ...groupData.groupKeys,
        label: keyString,
        value: groupData.sum
      }));
    }

    return resultData;
  }, [data, filters, graphGroupBy]);

  const contextValue: IDataContext = {
    data,
    loading,
    error,
    filters,
    groupBy,
    graphGroupBy,
    allColumns,
    processedData,
    graphProcessedData,
    setFilters,
    setGroupBy,
    setGraphGroupBy,
    refetchData: fetchData,
    xLabelKey,
    yLabelKey
  };

  return (
    <DataContext.Provider value={contextValue}>
      {children}
    </DataContext.Provider>
  );
};
