from dify_plugin import ToolProvider
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError


class Neo4jProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        """
        Validate Neo4j connection credentials
        """
        uri = credentials.get("uri")
        username = credentials.get("username")
        password = credentials.get("password")
        database = credentials.get("database", "neo4j")
        
        if not uri or not username or not password:
            raise ValueError("Missing required credentials: uri, username, or password")
        
        try:
            # Try to connect to Neo4j
            driver = GraphDatabase.driver(uri, auth=(username, password))
            driver.verify_connectivity()
            driver.close()
        except AuthError as e:
            raise ValueError(f"Authentication failed: Invalid username or password - {str(e)}")
        except ServiceUnavailable as e:
            raise ValueError(f"Cannot connect to Neo4j at {uri} - {str(e)}")
        except Exception as e:
            raise ValueError(f"Connection error: {str(e)}")

