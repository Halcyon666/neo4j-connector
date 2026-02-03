from collections.abc import Generator
from typing import Any
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError, ServiceUnavailable, AuthError

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class Neo4jConnectorTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Execute a Cypher query on Neo4j database
        Supports: READ (query), WRITE (create/update/delete)
        """
        # 1. 获取连接凭证
        uri = self.runtime.credentials.get("uri")
        username = self.runtime.credentials.get("username")
        password = self.runtime.credentials.get("password")
        database = self.runtime.credentials.get("database", "neo4j")

        # 2. 获取查询参数
        operation_type = tool_parameters.get("operation_type", "query").lower()
        query = tool_parameters.get("query", "").strip()
        max_results = tool_parameters.get("max_results", 100)

        # 参数验证
        if not query:
            yield self.create_text_message("❌ Error: No query provided.")
            return

        if not uri or not username or not password:
            yield self.create_text_message("❌ Error: Missing connection credentials.")
            return

        # 验证操作类型
        valid_operations = ["query", "create", "update", "delete", "write"]
        if operation_type not in valid_operations:
            yield self.create_text_message(f"❌ Error: Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}")
            return

        # 限制最大结果数
        if max_results > 1000:
            max_results = 1000

        # 3. 连接并执行查询
        driver = None
        try:
            # 连接到 Neo4j
            driver = GraphDatabase.driver(uri, auth=(username, password))
            
            # 验证连接
            driver.verify_connectivity()

            # 根据操作类型执行不同的逻辑
            if operation_type in ["create", "update", "delete", "write"]:
                # 写操作：创建、更新、删除
                yield from self._execute_write_operation(driver, database, query, operation_type)
            else:
                # 读操作：查询
                yield from self._execute_read_operation(driver, database, query, max_results)

        except AuthError as e:
            yield self.create_text_message(f"❌ Authentication Error: Invalid username or password.\n{str(e)}")
        
        except ServiceUnavailable as e:
            yield self.create_text_message(f"❌ Connection Error: Cannot connect to Neo4j at {uri}\n{str(e)}")
        
        except Neo4jError as e:
            # Neo4j 特定错误(如语法错误)
            yield self.create_text_message(f"❌ Neo4j Query Error: {e.message}\nCode: {e.code}")
        
        except Exception as e:
            # 其他未预期的错误
            yield self.create_text_message(f"❌ Unexpected Error: {str(e)}")

        finally:
            # 确保关闭连接
            if driver:
                driver.close()

    def _execute_read_operation(self, driver, database: str, query: str, max_results: int) -> Generator[ToolInvokeMessage, None, None]:
        """
        执行读操作（查询）
        """
        with driver.session(database=database) as session:
            result = session.run(query)
            
            # 收集结果
            records = []
            count = 0
            
            for record in result:
                if count >= max_results:
                    break
                records.append(dict(record))
                count += 1
            
            # 获取查询统计信息
            summary = result.consume()
            
            # 构建响应
            response_data = {
                "status": "success",
                "operation": "query",
                "results": records,
                "count": count,
                "summary": {
                    "query_type": summary.query_type,
                    "counters": {
                        "nodes_created": summary.counters.nodes_created,
                        "nodes_deleted": summary.counters.nodes_deleted,
                        "relationships_created": summary.counters.relationships_created,
                        "relationships_deleted": summary.counters.relationships_deleted,
                        "properties_set": summary.counters.properties_set,
                        "labels_added": summary.counters.labels_added,
                        "labels_removed": summary.counters.labels_removed,
                    }
                }
            }
            
            # 如果有更多结果被截断，添加提示
            if count >= max_results:
                response_data["truncated"] = True
                response_data["message"] = f"Results limited to {max_results}. Increase max_results to see more."

            # 返回 JSON 结果
            yield self.create_json_message(response_data)

    def _execute_write_operation(self, driver, database: str, query: str, operation_type: str) -> Generator[ToolInvokeMessage, None, None]:
        """
        执行写操作（创建、更新、删除）
        """
        with driver.session(database=database) as session:
            # 使用写事务执行操作
            def write_transaction(tx):
                result = tx.run(query)
                
                # 先收集返回的记录（如果有 RETURN 子句）
                records = []
                for record in result:
                    records.append(dict(record))
                
                # 然后获取统计信息
                summary = result.consume()
                
                return records, summary
            
            # 执行写事务
            records, summary = session.execute_write(write_transaction)
            
            # 构建响应
            response_data = {
                "status": "success",
                "operation": operation_type,
                "query_type": summary.query_type,
                "counters": {
                    "nodes_created": summary.counters.nodes_created,
                    "nodes_deleted": summary.counters.nodes_deleted,
                    "relationships_created": summary.counters.relationships_created,
                    "relationships_deleted": summary.counters.relationships_deleted,
                    "properties_set": summary.counters.properties_set,
                    "labels_added": summary.counters.labels_added,
                    "labels_removed": summary.counters.labels_removed,
                }
            }
            
            # 如果有返回结果，添加到响应中
            if records:
                response_data["results"] = records
                response_data["count"] = len(records)
            
            # 添加操作成功的消息
            operation_messages = {
                "create": f"✅ Created {summary.counters.nodes_created} node(s) and {summary.counters.relationships_created} relationship(s)",
                "update": f"✅ Updated {summary.counters.properties_set} propertie(s)",
                "delete": f"✅ Deleted {summary.counters.nodes_deleted} node(s) and {summary.counters.relationships_deleted} relationship(s)",
                "write": "✅ Write operation completed successfully"
            }
            
            response_data["message"] = operation_messages.get(operation_type, "✅ Operation completed successfully")
            
            # 返回 JSON 结果
            yield self.create_json_message(response_data)
