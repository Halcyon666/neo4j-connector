#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Neo4j Connector Plugin
"""
import sys
import os
from typing import Any, Generator

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.neo4j_connector import Neo4jConnectorTool
from dify_plugin.entities.tool import ToolInvokeMessage


class MockRuntime:
    """Mock runtime for testing"""
    def __init__(self, credentials: dict):
        self.credentials = credentials


class TestNeo4jConnector:
    """Test class for Neo4j Connector"""
    
    def __init__(self):
        # Test credentials - update these with your Neo4j instance
        self.credentials = {
            "uri": "bolt://localhost:7687",  # Update with your Neo4j URI
            "username": "neo4j",              # Update with your username
            "password": "password",           # Update with your password
            "database": "neo4j"
        }
        
    def create_tool_instance(self) -> Neo4jConnectorTool:
        """Create a tool instance with mock runtime"""
        tool = Neo4jConnectorTool()
        tool.runtime = MockRuntime(self.credentials)
        return tool
    
    def print_results(self, results: Generator[ToolInvokeMessage, None, None], test_name: str):
        """Print test results"""
        print(f"\n{'='*60}")
        print(f"Test: {test_name}")
        print('='*60)
        
        for message in results:
            if hasattr(message, 'message'):
                print(f"Type: {message.type}")
                print(f"Message: {message.message}")
            else:
                print(f"Result: {message}")
        print('='*60)
    
    def test_query_operation(self):
        """Test query (read) operation"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "query",
            "query": "MATCH (n) RETURN n LIMIT 5",
            "max_results": 5
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Query Operation - List 5 nodes")
    
    def test_create_node(self):
        """Test create operation - create a node"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "create",
            "query": "CREATE (p:Person {name: 'TestUser', age: 25, created_at: datetime()}) RETURN p"
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Create Operation - Create Person node")
    
    def test_create_multiple_nodes(self):
        """Test create operation - create multiple nodes"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "create",
            "query": """
                CREATE (p1:Person {name: 'Alice', age: 30}),
                       (p2:Person {name: 'Bob', age: 35})
                RETURN p1, p2
            """
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Create Operation - Create multiple nodes")
    
    def test_update_node(self):
        """Test update operation - update node properties"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "update",
            "query": """
                MATCH (p:Person {name: 'TestUser'})
                SET p.age = 26, p.updated_at = datetime()
                RETURN p
            """
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Update Operation - Update Person age")
    
    def test_create_relationship(self):
        """Test create operation - create relationship"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "create",
            "query": """
                MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
                CREATE (a)-[r:KNOWS {since: 2024}]->(b)
                RETURN a, r, b
            """
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Create Operation - Create relationship")
    
    def test_query_with_relationship(self):
        """Test query operation - query with relationship"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "query",
            "query": """
                MATCH (a:Person)-[r:KNOWS]->(b:Person)
                RETURN a.name as person1, b.name as person2, r.since as since
                LIMIT 10
            """,
            "max_results": 10
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Query Operation - Query relationships")
    
    def test_delete_relationship(self):
        """Test delete operation - delete relationship"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "delete",
            "query": """
                MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'})
                DELETE r
            """
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Delete Operation - Delete relationship")
    
    def test_delete_nodes(self):
        """Test delete operation - delete nodes"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "delete",
            "query": """
                MATCH (p:Person)
                WHERE p.name IN ['TestUser', 'Alice', 'Bob']
                DETACH DELETE p
            """
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Delete Operation - Delete test nodes")
    
    def test_invalid_operation(self):
        """Test invalid operation type"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "invalid",
            "query": "MATCH (n) RETURN n"
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Error Test - Invalid operation type")
    
    def test_empty_query(self):
        """Test empty query"""
        tool = self.create_tool_instance()
        
        params = {
            "operation_type": "query",
            "query": ""
        }
        
        results = tool._invoke(params)
        self.print_results(results, "Error Test - Empty query")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("Starting Neo4j Connector Tests")
        print("="*60)
        
        try:
            # Basic tests
            print("\n>>> Running basic query test...")
            self.test_query_operation()
            
            print("\n>>> Running create node test...")
            self.test_create_node()
            
            print("\n>>> Running create multiple nodes test...")
            self.test_create_multiple_nodes()
            
            print("\n>>> Running update node test...")
            self.test_update_node()
            
            print("\n>>> Running create relationship test...")
            self.test_create_relationship()
            
            print("\n>>> Running query with relationship test...")
            self.test_query_with_relationship()
            
            print("\n>>> Running delete relationship test...")
            self.test_delete_relationship()
            
            print("\n>>> Running delete nodes test...")
            self.test_delete_nodes()
            
            # Error tests
            print("\n>>> Running error tests...")
            self.test_invalid_operation()
            self.test_empty_query()
            
            print("\n" + "="*60)
            print("All tests completed!")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Main test function"""
    print("Neo4j Connector Test Suite")
    print("="*60)
    print("Please update the credentials in the script before running!")
    print("="*60)
    
    # Ask user if they want to continue
    response = input("\nHave you updated the credentials? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Please update the credentials in test_neo4j_connector.py and run again.")
        return
    
    tester = TestNeo4jConnector()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
