# Neo4j 连接器 / Neo4j Connector

<div align="center">

![Neo4j Connector](https://img.shields.io/badge/Neo4j-Connector-blue?style=flat-square)
![Version](https://img.shields.io/badge/version-0.0.1-green?style=flat-square)
![Dify Plugin](https://img.shields.io/badge/Dify-Plugin-orange?style=flat-square)

**一个强大的 Dify 插件，用于连接和查询 Neo4j 图数据库**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 📖 简介

Neo4j 连接器是一个专为 Dify 平台设计的插件，允许你在 AI 工作流和应用中直接执行 Cypher 查询，与 Neo4j 图数据库进行交互。

### ✨ 特性

- 🔗 **简单连接**：通过 URI、用户名和密码轻松连接到 Neo4j 数据库
- 📊 **Cypher 查询**：支持执行任意 Cypher 查询语句
- 🎯 **结果限制**：可配置返回结果的最大数量（默认 100，最大 1000）
- 📈 **查询统计**：返回详细的查询统计信息（节点创建/删除、关系创建/删除等）
- 🛡️ **错误处理**：完善的错误处理机制，包括认证错误、连接错误和查询错误
- 🌐 **多语言支持**：支持中文和英文界面

### 🚀 快速开始

#### 1. 安装插件

在 Dify 插件市场中搜索 "Neo4j 连接器" 并安装，或者通过调试模式安装：

```bash
# 克隆仓库
git clone https://github.com/halcyon666/neo4j-connector.git
cd neo4j-connector

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 Dify 服务器信息

# 运行插件
python -m main
```

#### 2. 配置连接

在 Dify 插件页面中配置 Neo4j 连接信息：

- **Neo4j URI**: 你的 Neo4j 数据库地址（例如：`bolt://localhost:7687` 或 `neo4j://localhost:7687`）
- **用户名**: Neo4j 数据库用户名（默认：`neo4j`）
- **密码**: Neo4j 数据库密码
- **数据库名称**: 可选，指定要连接的数据库（默认：`neo4j`）

#### 3. 使用工具

在你的 Dify 工作流或应用中添加 "Neo4j 查询执行器" 工具：

**参数：**

- **Cypher 查询语句**（必填）：要执行的 Cypher 查询
- **最大返回结果数**（可选）：限制返回结果的数量，默认 100，最大 1000

**示例查询：**

```cypher
// 查询所有节点
MATCH (n) RETURN n LIMIT 10

// 查询特定标签的节点
MATCH (p:Person) RETURN p.name, p.age

// 查询关系
MATCH (p:Person)-[r:KNOWS]->(f:Person)
RETURN p.name, type(r), f.name

// 创建节点
CREATE (p:Person {name: 'Alice', age: 30}) RETURN p

// 创建关系
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[r:KNOWS]->(b)
RETURN r
```

### 📊 返回结果格式

工具返回 JSON 格式的结果：

```json
{
  "status": "success",
  "results": [
    { "n.name": "Alice", "n.age": 30 },
    { "n.name": "Bob", "n.age": 25 }
  ],
  "count": 2,
  "summary": {
    "query_type": "r",
    "counters": {
      "nodes_created": 0,
      "nodes_deleted": 0,
      "relationships_created": 0,
      "relationships_deleted": 0,
      "properties_set": 0,
      "labels_added": 0,
      "labels_removed": 0
    }
  }
}
```

### 🛠️ 技术栈

- **Python 3.12+**
- **Neo4j Python Driver 5.10.0+**
- **Dify Plugin SDK 0.4.0+**

### 📝 开发

```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python -m pytest

# 代码格式化
black .
```

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 📄 许可证

MIT License

### 👤 作者

**halcyon666**

---

## English

### 📖 Introduction

Neo4j Connector is a powerful Dify plugin that enables you to connect and query Neo4j graph databases directly within your AI workflows and applications.

### ✨ Features

- 🔗 **Easy Connection**: Connect to Neo4j databases with URI, username, and password
- 📊 **Cypher Queries**: Execute any Cypher query statements
- 🎯 **Result Limiting**: Configure maximum number of results (default 100, max 1000)
- 📈 **Query Statistics**: Returns detailed query statistics (nodes created/deleted, relationships created/deleted, etc.)
- 🛡️ **Error Handling**: Comprehensive error handling for authentication, connection, and query errors
- 🌐 **Multi-language**: Supports both Chinese and English interfaces

### 🚀 Quick Start

#### 1. Install Plugin

Search for "Neo4j Connector" in the Dify plugin marketplace, or install via debug mode:

```bash
# Clone repository
git clone https://github.com/halcyon666/neo4j-connector.git
cd neo4j-connector

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env file with your Dify server information

# Run plugin
python main.py
```

#### 2. Configure Connection

Configure Neo4j connection in Dify plugin page:

- **Neo4j URI**: Your Neo4j database address (e.g., `bolt://localhost:7687` or `neo4j://localhost:7687`)
- **Username**: Neo4j database username (default: `neo4j`)
- **Password**: Neo4j database password
- **Database Name**: Optional, specify database to connect (default: `neo4j`)

#### 3. Use Tool

Add "Neo4j Query Executor" tool to your Dify workflow or application:

**Parameters:**

- **Cypher Query** (required): The Cypher query to execute
- **Maximum Results** (optional): Limit number of results, default 100, max 1000

**Example Queries:**

```cypher
// Query all nodes
MATCH (n) RETURN n LIMIT 10

// Query nodes with specific label
MATCH (p:Person) RETURN p.name, p.age

// Query relationships
MATCH (p:Person)-[r:KNOWS]->(f:Person)
RETURN p.name, type(r), f.name

// Create node
CREATE (p:Person {name: 'Alice', age: 30}) RETURN p

// Create relationship
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[r:KNOWS]->(b)
RETURN r
```

### 📊 Response Format

The tool returns results in JSON format:

```json
{
  "status": "success",
  "results": [
    { "n.name": "Alice", "n.age": 30 },
    { "n.name": "Bob", "n.age": 25 }
  ],
  "count": 2,
  "summary": {
    "query_type": "r",
    "counters": {
      "nodes_created": 0,
      "nodes_deleted": 0,
      "relationships_created": 0,
      "relationships_deleted": 0,
      "properties_set": 0,
      "labels_added": 0,
      "labels_removed": 0
    }
  }
}
```

### 🛠️ Tech Stack

- **Python 3.12+**
- **Neo4j Python Driver 5.10.0+**
- **Dify Plugin SDK 0.4.0+**

### 📝 Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Code formatting
black .
```

### 🤝 Contributing

Issues and Pull Requests are welcome!

### 📄 License

MIT License

### 👤 Author

**halcyon666**

---

<div align="center">

**Made with ❤️ for the Dify Community**

[Report Bug](https://github.com/halcyon666/neo4j-connector/issues) · [Request Feature](https://github.com/halcyon666/neo4j-connector/issues)

</div>
