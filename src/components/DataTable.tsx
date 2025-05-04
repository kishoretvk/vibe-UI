import React, { useState, useContext } from 'react';
import { DataContext } from '../contexts/DataContext';
import type { DataItem } from '../contexts/DataContext';
import styles from './DataTable.module.css';
import GraphFilterColumn from './GraphFilterColumn';

interface DataTableProps {
  data: DataItem[];
  showFilters?: boolean;
  showGroupBy?: boolean;
  showGraphFilters?: boolean;
}

const DataTable: React.FC<DataTableProps> = ({ 
  data, 
  showFilters = true, 
  showGroupBy = true,
  showGraphFilters = false 
}) => {
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [groupBy, setGroupBy] = useState<string[]>([]);
  const [showControls, setShowControls] = useState(false);
  const { graphGroupBy, setGraphGroupBy, allColumns } = useContext(DataContext);

  if (!data || data.length === 0) {
    return <div className={styles.tableContainer}>No data available</div>;
  }

  // Filter out ID column and apply filters
  const columns = Object.keys(data[0]).filter(col => col !== 'id');
  const filteredData = data.filter(row => 
    Object.entries(filters).every(([key, value]) => 
      !value || String(row[key]).toLowerCase().includes(value.toLowerCase())
    )
  );

  // Group data if groupBy is specified
  const groupedData = groupBy.length > 0 
    ? filteredData.reduce((acc, row) => {
        const groupKey = groupBy.map(col => row[col]).join('|');
        if (!acc[groupKey]) {
          acc[groupKey] = { ...row, _count: 0 };
        }
        acc[groupKey]._count++;
        return acc;
      }, {} as Record<string, any>)
    : null;

  const displayData = groupedData ? Object.values(groupedData) : filteredData;
  const displayColumns = [...columns, ...(groupedData ? ['_count'] : [])];

  return (
    <div className={styles.tableContainer}>
      <div className={styles.controlToggle}>
        <button 
          onClick={() => setShowControls(!showControls)}
          className={styles.toggleButton}
        >
          {showControls ? '▼ Hide Controls' : '► Show Filters & Grouping'}
        </button>
      </div>

      {showControls && (
        <div className={styles.controls}>
          {showFilters && (
            <div className={styles.filterGroup}>
              <h4>Filters</h4>
              {columns.map(col => (
                <div key={`filter-${col}`} className={styles.filterInput}>
                  <label>{col}:</label>
                  <input
                    type="text"
                    value={filters[col] || ''}
                    onChange={e => setFilters({...filters, [col]: e.target.value})}
                    placeholder={`Filter ${col}...`}
                  />
                </div>
              ))}
            </div>
          )}

          {showGroupBy && (
            <div className={styles.groupBy}>
              <h4>Group By</h4>
              {columns.map(col => (
                <label key={`group-${col}`}>
                  <input
                    type="checkbox"
                    checked={groupBy.includes(col)}
                    onChange={e => {
                      if (e.target.checked) {
                        setGroupBy([...groupBy, col]);
                      } else {
                        setGroupBy(groupBy.filter(g => g !== col));
                      }
                    }}
                  />
                  {col}
                </label>
              ))}
            </div>
          )}

          {showGraphFilters && (
            <div className={styles.graphFilters}>
              <h4>Graph Filters</h4>
              <GraphFilterColumn
                activeFilters={graphGroupBy}
                availableColumns={allColumns}
                onFilterChange={(column, checked) => {
                  setGraphGroupBy(prev => 
                    checked ? [...prev, column] : prev.filter(c => c !== column)
                  );
                }}
              />
            </div>
          )}
        </div>
      )}

      <table className={styles.table}>
        <thead>
          <tr>
            {displayColumns.map(col => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {displayData.map((row, index) => (
            <tr key={index}>
              {displayColumns.map(col => (
                <td key={`${index}-${col}`}>
                  {row[col] !== null && row[col] !== undefined 
                    ? String(row[col]) 
                    : '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
