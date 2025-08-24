"""
Data connectors for various data sources
"""
import pandas as pd
import json
import csv
from typing import List, Dict, Any, Optional
import sqlite3
try:
    import pymysql
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

try:
    import pyodbc
    MSSQL_AVAILABLE = True
except ImportError:
    MSSQL_AVAILABLE = False

try:
    from pymongo import MongoClient
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False

try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

try:
    import json
    JSON_AVAILABLE = True
except ImportError:
    JSON_AVAILABLE = False

try:
    import pyarrow.parquet as pq
    PARQUET_AVAILABLE = True
except ImportError:
    PARQUET_AVAILABLE = False

try:
    import avro.schema
    import avro.io
    import avro.datafile
    AVRO_AVAILABLE = True
except ImportError:
    AVRO_AVAILABLE = False

class DataConnector:
    """Base class for data connectors"""
    
    def connect(self) -> bool:
        """Establish connection to data source"""
        raise NotImplementedError
    
    def disconnect(self) -> None:
        """Close connection to data source"""
        raise NotImplementedError
    
    def fetch_data(self, query: str) -> List[Dict[str, Any]]:
        """Fetch data from data source"""
        raise NotImplementedError

class CSVConnector(DataConnector):
    """Connector for CSV files"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def connect(self) -> bool:
        """Check if file exists and is readable"""
        try:
            with open(self.file_path, 'r') as f:
                csv.Sniffer().sniff(f.read(1024))
            return True
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """No connection to close for CSV files"""
        pass
    
    def fetch_data(self, query: str = None) -> List[Dict[str, Any]]:
        """Read data from CSV file"""
        try:
            # Read CSV file using pandas
            df = pd.read_csv(self.file_path)
            # Convert to list of dictionaries
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

class MySQLConnector(DataConnector):
    """Connector for MySQL databases"""
    
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        if not MYSQL_AVAILABLE:
            raise ImportError("pymysql is not installed. Please install it to use MySQL connector.")
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """Establish connection to MySQL database"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            return True
        except Exception as e:
            print(f"Error connecting to MySQL: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Close connection to MySQL database"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def fetch_data(self, query: str) -> List[Dict[str, Any]]:
        """Execute query and fetch data from MySQL database"""
        if not self.connection:
            raise Exception("Not connected to database")
        
        try:
            df = pd.read_sql(query, self.connection)
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error executing MySQL query: {str(e)}")

class PostgreSQLConnector(DataConnector):
    """Connector for PostgreSQL databases"""
    
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        if not POSTGRES_AVAILABLE:
            raise ImportError("psycopg2 is not installed. Please install it to use PostgreSQL connector.")
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            return True
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Close connection to PostgreSQL database"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def fetch_data(self, query: str) -> List[Dict[str, Any]]:
        """Execute query and fetch data from PostgreSQL database"""
        if not self.connection:
            raise Exception("Not connected to database")
        
        try:
            df = pd.read_sql(query, self.connection)
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error executing PostgreSQL query: {str(e)}")

class MSSQLConnector(DataConnector):
    """Connector for Microsoft SQL Server databases"""
    
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        if not MSSQL_AVAILABLE:
            raise ImportError("pyodbc is not installed. Please install it to use Microsoft SQL Server connector.")
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """Establish connection to Microsoft SQL Server database"""
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.host},{self.port};DATABASE={self.database};UID={self.username};PWD={self.password}"
            self.connection = pyodbc.connect(connection_string)
            return True
        except Exception as e:
            print(f"Error connecting to Microsoft SQL Server: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Close connection to Microsoft SQL Server database"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def fetch_data(self, query: str) -> List[Dict[str, Any]]:
        """Execute query and fetch data from Microsoft SQL Server database"""
        if not self.connection:
            raise Exception("Not connected to database")
        
        try:
            df = pd.read_sql(query, self.connection)
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error executing Microsoft SQL Server query: {str(e)}")

class MongoDBConnector(DataConnector):
    """Connector for MongoDB databases"""
    
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        if not MONGO_AVAILABLE:
            raise ImportError("pymongo is not installed. Please install it to use MongoDB connector.")
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.client = None
        self.db = None
    
    def connect(self) -> bool:
        """Establish connection to MongoDB database"""
        try:
            connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/"
            self.client = MongoClient(connection_string)
            self.db = self.client[self.database]
            # Test connection
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Close connection to MongoDB database"""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
    
    def fetch_data(self, query: str) -> List[Dict[str, Any]]:
        """Fetch data from MongoDB collection"""
        if not self.db:
            raise Exception("Not connected to database")
        
        try:
            # Parse query as JSON to get collection name and filter
            query_dict = json.loads(query) if isinstance(query, str) else query
            collection_name = query_dict.get("collection")
            filter_query = query_dict.get("filter", {})
            limit = query_dict.get("limit", 1000)
            
            if not collection_name:
                raise Exception("Collection name is required in query")
            
            collection = self.db[collection_name]
            cursor = collection.find(filter_query).limit(limit)
            
            # Convert cursor to list of dictionaries
            results = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
            
            return results
        except Exception as e:
            raise Exception(f"Error fetching data from MongoDB: {str(e)}")

class OracleConnector(DataConnector):
    """Connector for Oracle databases"""
    
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        if not ORACLE_AVAILABLE:
            raise ImportError("cx_Oracle is not installed. Please install it to use Oracle connector.")
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        """Establish connection to Oracle database"""
        try:
            dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.database)
            self.connection = cx_Oracle.connect(self.username, self.password, dsn)
            return True
        except Exception as e:
            print(f"Error connecting to Oracle: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Close connection to Oracle database"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def fetch_data(self, query: str) -> List[Dict[str, Any]]:
        """Execute query and fetch data from Oracle database"""
        if not self.connection:
            raise Exception("Not connected to database")
        
        try:
            df = pd.read_sql(query, self.connection)
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error executing Oracle query: {str(e)}")

class RedisConnector(DataConnector):
    """Connector for Redis databases"""
    
    def __init__(self, host: str, port: int, username: str, password: str, database: str):
        if not REDIS_AVAILABLE:
            raise ImportError("redis is not installed. Please install it to use Redis connector.")
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.client = None
    
    def connect(self) -> bool:
        """Establish connection to Redis database"""
        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                db=int(self.database) if self.database.isdigit() else 0
            )
            # Test connection
            self.client.ping()
            return True
        except Exception as e:
            print(f"Error connecting to Redis: {str(e)}")
            return False
    
    def disconnect(self) -> None:
        """Close connection to Redis database"""
        if self.client:
            self.client.close()
            self.client = None
    
    def fetch_data(self, query: str) -> List[Dict[str, Any]]:
        """Fetch data from Redis"""
        if not self.client:
            raise Exception("Not connected to database")
        
        try:
            # Parse query to determine operation
            query_dict = json.loads(query) if isinstance(query, str) else query
            operation = query_dict.get("operation", "get")
            key = query_dict.get("key")
            pattern = query_dict.get("pattern", "*")
            
            if operation == "get" and key:
                # Get specific key
                value = self.client.get(key)
                if value:
                    return [{"key": key, "value": value.decode('utf-8') if isinstance(value, bytes) else value}]
                else:
                    return []
            elif operation == "scan":
                # Scan keys matching pattern
                keys = self.client.scan_iter(match=pattern)
                results = []
                for key in keys:
                    key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                    value = self.client.get(key_str)
                    value_str = value.decode('utf-8') if isinstance(value, bytes) else value
                    results.append({"key": key_str, "value": value_str})
                return results
            else:
                raise Exception("Invalid Redis operation or missing key/pattern")
        except Exception as e:
            raise Exception(f"Error fetching data from Redis: {str(e)}")

class ExcelConnector(DataConnector):
    """Connector for Excel files"""
    
    def __init__(self, file_path: str):
        if not EXCEL_AVAILABLE:
            raise ImportError("openpyxl is not installed. Please install it to use Excel connector.")
        
        self.file_path = file_path
    
    def connect(self) -> bool:
        """Check if file exists and is readable"""
        try:
            pd.read_excel(self.file_path, nrows=1)
            return True
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """No connection to close for Excel files"""
        pass
    
    def fetch_data(self, query: str = None) -> List[Dict[str, Any]]:
        """Read data from Excel file"""
        try:
            # Parse query to get sheet name and range
            sheet_name = "Sheet1"
            if query:
                query_dict = json.loads(query) if isinstance(query, str) else query
                sheet_name = query_dict.get("sheet", "Sheet1")
            
            # Read Excel file using pandas
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            # Convert to list of dictionaries
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")

class JSONConnector(DataConnector):
    """Connector for JSON files"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def connect(self) -> bool:
        """Check if file exists and is readable"""
        try:
            with open(self.file_path, 'r') as f:
                json.load(f)
            return True
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """No connection to close for JSON files"""
        pass
    
    def fetch_data(self, query: str = None) -> List[Dict[str, Any]]:
        """Read data from JSON file"""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            
            # If data is a dictionary, convert to list
            if isinstance(data, dict):
                # Check if it's already in the right format
                if isinstance(data, list):
                    return data
                # If it's a single object, wrap it in a list
                elif isinstance(data, dict):
                    return [data]
                # Otherwise return as is
                else:
                    return [data]
            else:
                return data
        except Exception as e:
            raise Exception(f"Error reading JSON file: {str(e)}")

class ParquetConnector(DataConnector):
    """Connector for Parquet files"""
    
    def __init__(self, file_path: str):
        if not PARQUET_AVAILABLE:
            raise ImportError("pyarrow is not installed. Please install it to use Parquet connector.")
        
        self.file_path = file_path
    
    def connect(self) -> bool:
        """Check if file exists and is readable"""
        try:
            pq.ParquetFile(self.file_path)
            return True
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """No connection to close for Parquet files"""
        pass
    
    def fetch_data(self, query: str = None) -> List[Dict[str, Any]]:
        """Read data from Parquet file"""
        try:
            # Read Parquet file using pyarrow
            table = pq.read_table(self.file_path)
            # Convert to pandas DataFrame then to list of dictionaries
            df = table.to_pandas()
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error reading Parquet file: {str(e)}")

class AvroConnector(DataConnector):
    """Connector for Avro files"""
    
    def __init__(self, file_path: str):
        if not AVRO_AVAILABLE:
            raise ImportError("avro is not installed. Please install it to use Avro connector.")
        
        self.file_path = file_path
    
    def connect(self) -> bool:
        """Check if file exists and is readable"""
        try:
            with open(self.file_path, 'rb') as f:
                avro.datafile.DataFileReader(f, avro.io.DatumReader())
            return True
        except Exception:
            return False
    
    def disconnect(self) -> None:
        """No connection to close for Avro files"""
        pass
    
    def fetch_data(self, query: str = None) -> List[Dict[str, Any]]:
        """Read data from Avro file"""
        try:
            records = []
            with open(self.file_path, 'rb') as f:
                reader = avro.datafile.DataFileReader(f, avro.io.DatumReader())
                for record in reader:
                    records.append(record)
                reader.close()
            return records
        except Exception as e:
            raise Exception(f"Error reading Avro file: {str(e)}")

# Factory function to create appropriate connector
def create_connector(connector_type: str, **kwargs) -> DataConnector:
    """Factory function to create data connectors"""
    if connector_type.lower() == 'csv':
        return CSVConnector(kwargs.get('file_path'))
    elif connector_type.lower() == 'mysql':
        return MySQLConnector(
            kwargs.get('host'),
            kwargs.get('port', 3306),
            kwargs.get('username'),
            kwargs.get('password'),
            kwargs.get('database')
        )
    elif connector_type.lower() == 'postgresql':
        return PostgreSQLConnector(
            kwargs.get('host'),
            kwargs.get('port', 5432),
            kwargs.get('username'),
            kwargs.get('password'),
            kwargs.get('database')
        )
    elif connector_type.lower() == 'mssql':
        return MSSQLConnector(
            kwargs.get('host'),
            kwargs.get('port', 1433),
            kwargs.get('username'),
            kwargs.get('password'),
            kwargs.get('database')
        )
    elif connector_type.lower() == 'mongodb':
        return MongoDBConnector(
            kwargs.get('host'),
            kwargs.get('port', 27017),
            kwargs.get('username'),
            kwargs.get('password'),
            kwargs.get('database')
        )
    elif connector_type.lower() == 'oracle':
        return OracleConnector(
            kwargs.get('host'),
            kwargs.get('port', 1521),
            kwargs.get('username'),
            kwargs.get('password'),
            kwargs.get('database')
        )
    elif connector_type.lower() == 'redis':
        return RedisConnector(
            kwargs.get('host'),
            kwargs.get('port', 6379),
            kwargs.get('username'),
            kwargs.get('password'),
            kwargs.get('database', '0')
        )
    elif connector_type.lower() == 'excel':
        return ExcelConnector(kwargs.get('file_path'))
    elif connector_type.lower() == 'json':
        return JSONConnector(kwargs.get('file_path'))
    elif connector_type.lower() == 'parquet':
        return ParquetConnector(kwargs.get('file_path'))
    elif connector_type.lower() == 'avro':
        return AvroConnector(kwargs.get('file_path'))
    else:
        raise ValueError(f"Unsupported connector type: {connector_type}")