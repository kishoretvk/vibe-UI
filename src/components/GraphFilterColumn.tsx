import React from 'react';
import styles from './GraphFilterColumn.module.css';

interface GraphFilterColumnProps {
  activeFilters: string[];
  availableColumns: string[];
  onFilterChange: (column: string, checked: boolean) => void;
}

const GraphFilterColumn: React.FC<GraphFilterColumnProps> = ({ 
  activeFilters, 
  availableColumns,
  onFilterChange 
}) => {
  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h3>Graph Filters</h3>
        {activeFilters.length > 0 && (
          <span className={styles.badge}>{activeFilters.length}</span>
        )}
      </div>
      <div className={styles.filterList}>
        {availableColumns.map(column => (
          <label key={column} className={styles.filterItem}>
            <input
              type="checkbox"
              checked={activeFilters.includes(column)}
              onChange={(e) => onFilterChange(column, e.target.checked)}
            />
            {column}
          </label>
        ))}
      </div>
    </div>
  );
};

export default GraphFilterColumn;
