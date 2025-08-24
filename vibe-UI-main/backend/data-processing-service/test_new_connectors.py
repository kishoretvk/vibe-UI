"""
Test script for new data connectors
"""
import os
import json
from data_connectors import create_connector

def test_json_connector():
    """Test JSON connector with sample data"""
    print("Testing JSON Connector with sample data...")
    
    # Create connector
    file_path = os.path.join(os.path.dirname(__file__), 'sample_data.json')
    connector = create_connector('json', file_path=file_path)
    
    # Test connection
    if connector.connect():
        print("✓ JSON connection successful")
        
        # Test data fetching
        try:
            data = connector.fetch_data()
            print(f"✓ Fetched {len(data)} records from JSON")
            print(f"  First record: {data[0] if data else 'No data'}")
            return True
        except Exception as e:
            print(f"✗ Error fetching data from JSON: {e}")
            return False
    else:
        print("✗ JSON connection failed")
        return False

def test_csv_connector():
    """Test CSV connector with sample data"""
    print("\nTesting CSV Connector with sample data...")
    
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

def main():
    """Main test function"""
    print("New Data Connectors Test")
    print("=" * 25)
    
    results = []
    results.append(test_csv_connector())
    results.append(test_json_connector())
    
    print("\nTest Summary:")
    print("=" * 25)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed.")
        return False

if __name__ == "__main__":
    main()