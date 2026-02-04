# Neo4j 连接器

<div align="center">

![Neo4j Connector](https://img.shields.io/badge/Neo4j-Connector-blue?style=flat-square)
![Version](https://img.shields.io/badge/version-0.0.1-green?style=flat-square)
![Dify Plugin](https://img.shields.io/badge/Dify-Plugin-orange?style=flat-square)

**一个强大的 Dify 插件，用于连接和查询 Neo4j 图数据库**

[English](README.md) | 简体中文

</div>

---

## 📖 简介

Neo4j 连接器是一个专为 Dify 平台设计的插件，允许你在 AI 工作流和应用中直接执行 Cypher 查询，与 Neo4j 图数据库进行交互。

## ✨ 特性

- 🔗 **简单连接**：通过 URI、用户名和密码轻松连接到 Neo4j 数据库
- 📊 **完整的 Cypher 支持**：支持执行任意 Cypher 查询语句（查询、创建、更新、删除）
- 🎯 **结果限制**：可配置返回结果的最大数量（默认 100，最大 1000）
- 📈 **查询统计**：返回详细的查询统计信息（节点创建/删除、关系创建/删除等）
- 🛡️ **错误处理**：完善的错误处理机制，包括认证错误、连接错误和查询错误
- 🌐 **多语言支持**：支持中文和英文界面
- 🕐 **时间类型支持**：自动序列化 Neo4j 的 DateTime、Date、Time、Duration 类型为 ISO 格式
- 🔄 **图对象支持**：自动序列化 Node 和 Relationship 对象为 JSON 格式

## 🚀 快速开始

### 1. 安装插件

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

### 2. 配置连接

在 Dify 插件页面中配置 Neo4j 连接信息：

- **Neo4j URI**: 你的 Neo4j 数据库地址（例如：`bolt://localhost:7687` 或 `neo4j://localhost:7687`）
- **用户名**: Neo4j 数据库用户名（默认：`neo4j`）
- **密码**: Neo4j 数据库密码
- **数据库名称**: 可选，指定要连接的数据库（默认：`neo4j`）

### 3. 使用工具

在你的 Dify 工作流或应用中添加 "Neo4j 数据库连接器" 工具：

**参数：**

- **操作类型**（可选）：选择操作类型
  - `query`（查询/读取）- 默认
  - `create`（创建/插入）
  - `update`（更新/修改）
  - `delete`（删除/移除）
  - `write`（写入/通用）
- **Cypher 查询语句**（必填）：要执行的 Cypher 查询
- **最大返回结果数**（可选）：限制返回结果的数量，默认 100，最大 1000（仅适用于查询操作）

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

// 使用时间函数
RETURN datetime() AS current_time, date() AS today

// 更新节点属性
MATCH (p:Person {name: 'Alice'})
SET p.age = 31, p.updated_at = datetime()
RETURN p

// 删除节点
MATCH (p:Person {name: 'Alice'})
DELETE p
```

## 📊 返回结果格式

工具返回 JSON 格式的结果：

**查询操作（Query）：**

```json
{
  "status": "success",
  "operation": "query",
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

**写操作（Create/Update/Delete）：**

```json
{
  "status": "success",
  "operation": "create",
  "query_type": "w",
  "counters": {
    "nodes_created": 1,
    "nodes_deleted": 0,
    "relationships_created": 0,
    "relationships_deleted": 0,
    "properties_set": 2,
    "labels_added": 1,
    "labels_removed": 0
  },
  "results": [
    {
      "p": {
        "id": 123,
        "labels": ["Person"],
        "properties": {
          "name": "Alice",
          "age": 30
        }
      }
    }
  ],
  "count": 1,
  "message": "✅ Created 1 node(s) and 0 relationship(s)"
}
```

**时间类型序列化：**

```json
{
  "status": "success",
  "operation": "query",
  "results": [
    {
      "current_time": "2024-01-15T10:30:00.123456+00:00",
      "today": "2024-01-15"
    }
  ],
  "count": 1
}
```

## 🛠️ 技术栈

- **Python 3.12+**
- **Neo4j Python Driver 5.10.0+**
- **Dify Plugin SDK 0.4.0+**

## 📝 开发

```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python -m pytest

# 代码格式化
black .
```

## 🔧 故障排除

### 错误：Graph not found: xxx

**原因**：配置的数据库名称在 Neo4j 实例中不存在。

**解决方案**：
1. 检查 Neo4j 中存在的数据库：`SHOW DATABASES`
2. 在 Dify 插件配置中使用正确的数据库名称（通常是 `neo4j`）
3. 或者留空数据库名称字段以使用默认数据库

### 错误：PydanticSerializationError: Unable to serialize unknown type

**原因**：旧版本插件不支持 Neo4j 的特殊类型（DateTime、Node 等）。

**解决方案**：更新到最新版本的插件，已支持自动序列化所有 Neo4j 类型。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👤 作者

**halcyon666**

---

<div align="center">

**Made with ❤️ for the Dify Community**

[报告 Bug](https://github.com/halcyon666/neo4j-connector/issues) · [请求功能](https://github.com/halcyon666/neo4j-connector/issues)

</div>
