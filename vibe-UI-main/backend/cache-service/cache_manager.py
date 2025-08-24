import redis
import json
import os
import hashlib
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta

class CacheManager:
    """Redis-based cache manager for storing and retrieving data"""
    
    def __init__(self):
        """Initialize the cache manager with Redis connection"""
        redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = int(os.getenv('CACHE_TTL', 3600))  # Default 1 hour
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a value in the cache
        
        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            ttl: Time to live in seconds (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Serialize the value to JSON
            serialized_value = json.dumps(value, default=str)
            
            # Set the value in Redis with TTL
            ttl = ttl or self.default_ttl
            result = self.redis_client.setex(key, ttl, serialized_value)
            
            return result
        except Exception as e:
            print(f"Error setting cache key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        try:
            # Get the value from Redis
            serialized_value = self.redis_client.get(key)
            
            if serialized_value is None:
                return None
            
            # Deserialize the value from JSON
            return json.loads(serialized_value)
        except Exception as e:
            print(f"Error getting cache key {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a value from the cache
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.redis_client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Error deleting cache key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the cache
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists, False otherwise
        """
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            print(f"Error checking cache key {key}: {e}")
            return False
    
    def generate_key(self, prefix: str, data: Dict[str, Any]) -> str:
        """
        Generate a cache key based on prefix and data
        
        Args:
            prefix: Key prefix
            data: Data to hash for key generation
            
        Returns:
            Generated cache key
        """
        # Create a hash of the data
        data_str = json.dumps(data, sort_keys=True, default=str)
        data_hash = hashlib.md5(data_str.encode()).hexdigest()
        
        return f"{prefix}:{data_hash}"
    
    def set_with_tags(self, key: str, value: Any, tags: List[str], ttl: Optional[int] = None) -> bool:
        """
        Set a value in the cache with tags for easy invalidation
        
        Args:
            key: Cache key
            value: Value to cache
            tags: List of tags to associate with this key
            ttl: Time to live in seconds (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Set the main value
            success = self.set(key, value, ttl)
            
            if success:
                # Associate the key with each tag
                for tag in tags:
                    self.redis_client.sadd(f"tag:{tag}", key)
                    # Set expiration for tag sets (longer than item TTL)
                    tag_ttl = (ttl or self.default_ttl) + 3600
                    self.redis_client.expire(f"tag:{tag}", tag_ttl)
            
            return success
        except Exception as e:
            print(f"Error setting cache key with tags {key}: {e}")
            return False
    
    def invalidate_tag(self, tag: str) -> int:
        """
        Invalidate all cache entries with a specific tag
        
        Args:
            tag: Tag to invalidate
            
        Returns:
            Number of keys deleted
        """
        try:
            # Get all keys associated with this tag
            keys = self.redis_client.smembers(f"tag:{tag}")
            
            if not keys:
                return 0
            
            # Delete all tagged keys
            deleted_count = 0
            for key in keys:
                # Decode bytes to string if needed
                key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                if self.delete(key_str):
                    deleted_count += 1
            
            # Delete the tag set itself
            self.redis_client.delete(f"tag:{tag}")
            
            return deleted_count
        except Exception as e:
            print(f"Error invalidating tag {tag}: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            info = self.redis_client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "0B"),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            }
        except Exception as e:
            print(f"Error getting cache stats: {e}")
            return {}
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate"""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)
    
    def flush_all(self) -> bool:
        """
        Flush all cache entries
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.redis_client.flushall()
            return True
        except Exception as e:
            print(f"Error flushing cache: {e}")
            return False