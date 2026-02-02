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
        """
        # 1. 获取连接凭证
        uri = self.runtime.credentials.get("uri")
        username = self.runtime.credentials.get("username")
        password = self.runtime.credentials.get("password")
        database = self.runtime.credentials.get("database", "neo4j")

        # 2. 获取查询参数
        query = tool_parameters.get("query", "").strip()
        max_results = tool_parameters.get("max_results", 100)

        # 参数验证
        if not query:
            yield self.create_text_message("❌ Error: No query provided.")
            return

        if not uri or not username or not password:
            yield self.create_text_message("❌ Error: Missing connection credentials.")
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

            # 执行查询
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
