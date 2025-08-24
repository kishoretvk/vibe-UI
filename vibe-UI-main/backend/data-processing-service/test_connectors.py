"""
Test script for data connectors
"""
import os
import json
from data_connectors import create_connector

def test_csv_connector():
    """Test CSV connector"""
    print("Testing CSV Connector...")
    
    # Create connector
    file_path = os.path.join(os.path.dirname(__file__), 'sample_data.csv')
    connector = create_connector('csv', file_path=file_path)
    
    # Test connection
    if connector.connect():
        print("✓ CSV connection successful")
        
        # Test data fetching
        try:
            data = connector.fetch_data()
            print(f"✓ Fetched {len(data)} records from CSV")
            print(f"  First record: {data[0] if data else 'No data'}")
            return True
        except Exception as e:
            print(f"✗ Error fetching data from CSV: {e}")
            return False
    else:
        print("✗ CSV connection failed")
        return False

def test_mysql_connector():
    """Test MySQL connector (if available)"""
    print("\nTesting MySQL Connector...")
    
    try:
        connector = create_connector(
            'mysql',
            host='localhost',
            port=3306,
            username='test',
            password='test',
            database='test'
        )
        print("✓ MySQL connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ MySQL connector not available (pymysql not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating MySQL connector: {e}")
        return False

def test_postgresql_connector():
    """Test PostgreSQL connector (if available)"""
    print("\nTesting PostgreSQL Connector...")
    
    try:
        connector = create_connector(
            'postgresql',
            host='localhost',
            port=5432,
            username='test',
            password='test',
            database='test'
        )
        print("✓ PostgreSQL connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ PostgreSQL connector not available (psycopg2 not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating PostgreSQL connector: {e}")
        return False

def test_mssql_connector():
    """Test Microsoft SQL Server connector (if available)"""
    print("\nTesting Microsoft SQL Server Connector...")
    
    try:
        connector = create_connector(
            'mssql',
            host='localhost',
            port=1433,
            username='test',
            password='test',
            database='test'
        )
        print("✓ Microsoft SQL Server connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ Microsoft SQL Server connector not available (pyodbc not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating Microsoft SQL Server connector: {e}")
        return False

def test_mongodb_connector():
    """Test MongoDB connector (if available)"""
    print("\nTesting MongoDB Connector...")
    
    try:
        connector = create_connector(
            'mongodb',
            host='localhost',
            port=27017,
            username='test',
            password='test',
            database='test'
        )
        print("✓ MongoDB connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ MongoDB connector not available (pymongo not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating MongoDB connector: {e}")
        return False

def test_oracle_connector():
    """Test Oracle connector (if available)"""
    print("\nTesting Oracle Connector...")
    
    try:
        connector = create_connector(
            'oracle',
            host='localhost',
            port=1521,
            username='test',
            password='test',
            database='test'
        )
        print("✓ Oracle connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ Oracle connector not available (cx_Oracle not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating Oracle connector: {e}")
        return False

def test_redis_connector():
    """Test Redis connector (if available)"""
    print("\nTesting Redis Connector...")
    
    try:
        connector = create_connector(
            'redis',
            host='localhost',
            port=6379,
            username='',
            password='',
            database='0'
        )
        print("✓ Redis connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ Redis connector not available (redis not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating Redis connector: {e}")
        return False

def test_excel_connector():
    """Test Excel connector (if available)"""
    print("\nTesting Excel Connector...")
    
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'sample_data.xlsx')
        connector = create_connector('excel', file_path=file_path)
        print("✓ Excel connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ Excel connector not available (openpyxl not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating Excel connector: {e}")
        return False

def test_json_connector():
    """Test JSON connector"""
    print("\nTesting JSON Connector...")
    
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'sample_data.json')
        connector = create_connector('json', file_path=file_path)
        print("✓ JSON connector created (not testing actual connection)")
        return True
    except Exception as e:
        print(f"✗ Error creating JSON connector: {e}")
        return False

def test_parquet_connector():
    """Test Parquet connector (if available)"""
    print("\nTesting Parquet Connector...")
    
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'sample_data.parquet')
        connector = create_connector('parquet', file_path=file_path)
        print("✓ Parquet connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ Parquet connector not available (pyarrow not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating Parquet connector: {e}")
        return False

def test_avro_connector():
    """Test Avro connector (if available)"""
    print("\nTesting Avro Connector...")
    
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'sample_data.avro')
        connector = create_connector('avro', file_path=file_path)
        print("✓ Avro connector created (not testing actual connection)")
        return True
    except ImportError:
        print("⚠ Avro connector not available (avro not installed)")
        return True
    except Exception as e:
        print(f"✗ Error creating Avro connector: {e}")
        return False

def main():
    """Main test function"""
    print("Data Connectors Test")
    print("=" * 20)
    
    results = []
    results.append(test_csv_connector())
    results.append(test_mysql_connector())
    results.append(test_postgresql_connector())
    results.append(test_mssql_connector())
    results.append(test_mongodb_connector())
    results.append(test_oracle_connector())
    results.append(test_redis_connector())
    results.append(test_excel_connector())
    results.append(test_json_connector())
    results.append(test_parquet_connector())
    results.append(test_avro_connector())
    
    print("\nTest Summary:")
    print("=" * 20)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed.")

if __name__ == "__main__":
    main()