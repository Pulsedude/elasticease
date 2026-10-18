# 📖 ElasticEase Command Reference Manual

Welcome to the comprehensive command specification and execution guide for **ElasticEase**. This document provides an exhaustive breakdown of every available command, its underlying Elasticsearch REST API mechanisms, parameter syntax, interactive prompts, and real-world examples.

---

## 📑 Table of Contents

- [General Syntax & Execution Rules](#general-syntax--execution-rules)
- [Core Cluster & Monitoring Commands](#core-cluster--monitoring-commands)
  - [`health`](#1-health)
  - [`shards`](#2-shards)
  - [`indices`](#3-indices)
  - [`ping`](#4-ping)
  - [`indexinfo`](#5-indexinfo)
  - [`master`](#6-master)
  - [`nodes`](#7-nodes)
  - [`capacity`](#8-capacity)
  - [`conn`](#9-conn)
  - [`ainf`](#10-ainf)
  - [`newpass` / `newcred`](#11-newpass--newcred)
  - [`help`](#12-help)
  - [`clear` / `cls`](#13-clear--cls)
  - [`exit` / `quit` / `q`](#14-exit--quit--q)
- [CRUD & Document Management Commands](#crud--document-management-commands)
  - [`index:new`](#15-indexnew)
  - [`index:del`](#16-indexdel)
  - [`inspect:doc`](#17-inspectdoc)
  - [`inspect:index`](#18-inspectindex)
  - [`addoc`](#19-addoc)
  - [`addocs`](#20-addocs)
  - [`updoc`](#21-updoc)
  - [`updocs`](#22-updocs)
  - [`deldoc`](#23-deldoc)
  - [`deldocs`](#24-deldocs)
- [Bulk Data File Formats (.json)](#bulk-data-file-formats-json)
- [Optimistic Concurrency Control (OCC) Mechanics](#optimistic-concurrency-control-occ-mechanics)

---

<a id="general-syntax--execution-rules"></a>
## 🛠 General Syntax & Execution Rules

1. **Case-Insensitive Command Names**: Commands such as `HEALTH`, `health`, `Indices`, and `indices` are normalized automatically.
2. **Quoting Values**: Arguments containing spaces, special characters, or URLs should be enclosed in double quotes (e.g., `"https://localhost:9200"` or `"playing video games"`).
3. **Flexible Argument Ordering for AI & JSON**:
   - For commands supporting both JSON and AI summaries, arguments can be passed in any order:
     - `shards json true` or `shards true json`
4. **Key-Value String Format**:
   - Inline document commands (`addoc`, `updoc`) accept key-value pairs formatted as:
     ```bash
     field1=value1 field2='value with spaces' field3=100
     ```
5. **Interactive Safety Prompts**: Bulk destructive operations (`updocs`, `deldocs`, `index:new "mappings"`) prompt for user confirmation (`[Y]/[N]`) before applying changes.

---

<a id="core-cluster--monitoring-commands"></a>
## 🖥 Core Cluster & Monitoring Commands

<a id="1-health"></a>
### 1. `health`

Checks the active Elasticsearch cluster's status, tracking shard reallocation, active nodes, and cluster health state (`green`, `yellow`, `red`).

- **Elasticsearch API**: `GET /_cluster/health`
- **Arguments**:
  - `[optional]` `json` — Render raw Elasticsearch response as colorized JSON.
  - `[optional]` `true` / `false` — Request an AI-powered health interpretation.

#### Execution Modes
| Syntax | Output Format | AI Summary |
|---|---|---|
| `health` | Rich Formatted Table + Latency | ❌ Disabled |
| `health json` | Formatted JSON + Latency | ❌ Disabled |
| `health true` | Rich Formatted Table | ✅ Enabled |
| `health json true` | Formatted JSON | ✅ Enabled |

#### Usage Examples
```bash
>>> health
>>> health json
>>> health true
```

#### Under the Hood
ElasticEase requests the cluster health endpoint asynchronously via HTTPX, measures the round-trip latency in milliseconds, and translates metrics such as `active_primary_shards`, `unassigned_shards`, and `status` into a structured Rich table. If AI summarization is enabled, the diagnostic data is passed to your configured LLM (Ollama or LiteLLM) to highlight potential issues (e.g., explaining why unassigned replica shards result in a yellow status).

---

<a id="2-shards"></a>
### 2. `shards`

Inspects all shard allocations across cluster nodes, identifying primary shards (`p`), replica shards (`r`), shard states (`STARTED`, `UNASSIGNED`, `INITIALIZING`, `RELOCATING`), document counts, and memory footprint.

- **Elasticsearch API**: `GET /_cat/shards?format=json`
- **Arguments**:
  - `[optional]` `json` — Render as JSON output.
  - `[optional]` `true` / `false` — Enable AI diagnostic summary of shard distribution.

#### Usage Examples
```bash
>>> shards
>>> shards json
>>> shards json true
>>> shards true
```

#### Table Columns Displayed
- `index`: Index name
- `shard`: Shard number (e.g., `0`, `1`)
- `primary & replica`: `p` (Primary) or `r` (Replica)
- `state`: Shard lifecycle state
- `docs`: Number of documents stored
- `store`: Disk space consumed (e.g., `4.2kb`, `120mb`)
- `dataset`: Underlying Lucene dataset size
- `ip`: IP address of the host node
- `node`: Node name hosting the shard

---

<a id="3-indices"></a>
### 3. `indices`

Displays all indices within the cluster along with operational metadata including shard allocation, document count, deleted documents, and total storage sizes.

- **Elasticsearch API**: `GET /_cat/indices?format=json`
- **Arguments**:
  - `[optional]` `json` — Output as JSON.
  - `[optional]` `true` / `false` — AI analysis of index health and storage bloat.

#### Usage Examples
```bash
>>> indices
>>> indices json
>>> indices true
```

#### Metrics Reported
- **Health**: Color-coded `green` (all primary and replica shards allocated) or `yellow` (replicas unassigned).
- **Status**: `open` or `close`.
- **UUID**: Unique internal index identifier.
- **Primary / Replica**: Shard counts (`pri`, `rep`).
- **Docs Count & Deleted**: Live document count and pending deleted documents awaiting Lucene segment merges.
- **Store Size & Primary Store Size**: Total disk consumption.

---

<a id="4-ping"></a>
### 4. `ping`

Sends a lightweight heartbeat probe to the configured Elasticsearch base URL to verify cluster reachability, measure network latency, and retrieve cluster version info.

- **Elasticsearch API**: `GET /`
- **Arguments**:
  - `[optional]` `true` — Trigger AI summary of cluster version and response times.

#### Usage Examples
```bash
>>> ping
>>> ping true
```

#### Sample Terminal Output
```text
Base URL: https://localhost:9200
Status: 🟢 Healthy
Latency: 14.821 ms
```

---

<a id="5-indexinfo"></a>
### 5. `indexinfo`

Retrieves deep schema specifications, settings, aliases, and explicit field type mappings for a designated index.

- **Elasticsearch API**: `GET /{index_name}`
- **Arguments**:
  - `[required]` `<index_name>` — Name of the target index.
  - `[optional]` `true` — Generate an AI summary explaining the schema mappings, data types, and shard settings.

#### Usage Examples
```bash
>>> indexinfo "students"
>>> indexinfo "products" true
```

#### Under the Hood
Fetches the full index definition including `mappings` (`properties`, field types like `keyword`, `text`, `integer`, `date`, `geo_point`) and `settings` (`number_of_shards`, `number_of_replicas`, analysis filters). If `true` is supplied, AI breaks down the schema structure and highlights unoptimized field definitions.

---

<a id="6-master"></a>
### 6. `master`

Identifies the currently elected master node responsible for cluster-wide actions such as creating indices, tracking node join/leave events, and assigning shards.

- **Elasticsearch API**: `GET /_cat/master?format=json`
- **Arguments**:
  - `[optional]` `json` — View raw master node JSON.

#### Usage Examples
```bash
>>> master
>>> master json
```

#### Output Fields
- `id`: Unique node hash
- `host`: Hostname or FQDN
- `ip`: Network IP address
- `node`: Human-readable node name

---

<a id="7-nodes"></a>
### 7. `nodes`

Reports live resource utilization and performance metrics across all nodes participating in the Elasticsearch cluster.

- **Elasticsearch API**: `GET /_cat/nodes?format=json`
- **Arguments**:
  - `[optional]` `json` — Raw JSON output.
  - `[optional]` `true` / `false` — AI analysis of resource bottlenecks.

#### Usage Examples
```bash
>>> nodes
>>> nodes json
>>> nodes true
```

#### Resource Metrics Tracked
- `ip`: Node IP address
- `heap.percent`: JVM heap memory usage percentage (⚠️ AI alerts if > 75%)
- `ram.percent`: Host physical RAM utilization
- `cpu`: Current CPU core utilization
- `load_1m`, `load_5m`, `load_15m`: System load averages
- `node.role`: Node roles (e.g., `cdimrst` for master, data, ingest, transform)
- `master`: `*` indicates the active elected master, `-` indicates master-eligible or worker
- `name`: Node name

---

<a id="8-capacity"></a>
### 8. `capacity`

Reports disk space allocation, storage capacities, available headroom, and disk usage forecast for all active data nodes.

- **Elasticsearch API**: `GET /_cat/allocation?format=json`
- **Arguments**:
  - `[optional]` `json` — JSON formatted disk metrics.
  - `[optional]` `true` / `false` — AI summary analyzing disk watermark safety margins.

#### Usage Examples
```bash
>>> capacity
>>> capacity json
>>> capacity true
```

#### Key Metrics
- `shards`: Total number of shards hosted on this node
- `disk.indices`: Space consumed by Lucene indices
- `disk.used`: Total host disk space consumed
- `disk.avail`: Remaining available disk space
- `disk.total`: Total disk capacity
- `disk.percent`: Percentage of disk space consumed
- **AI Threshold Insights**: Warns if any node is approaching Elasticsearch disk watermarks:
  - **Low Watermark (85%)**: Elasticsearch stops allocating new shards to this node.
  - **High Watermark (90%)**: Elasticsearch attempts to relocate shards to other nodes.
  - **Flood Stage (95%)**: Elasticsearch enforces a read-only index block (`read_only_allow_delete`).

---

<a id="9-conn"></a>
### 9. `conn`

Updates the Elasticsearch connection URL in `config.yaml` dynamically from the CLI without manual file editing.

- **Arguments**:
  - `[required]` `<URL>` — Valid HTTP/HTTPS base URL.

#### Usage Examples
```bash
>>> conn "https://localhost:9200"
>>> conn "http://192.168.1.50:9200"
```

> [!NOTE]
> Validates protocol (`http://` or `https://`). Updates `config.yaml` and requests a restart of the ElasticEase console to apply the new connection.

---

<a id="10-ainf"></a>
### 10. `ainf`

Displays the active AI Inference provider or toggles between available AI engines (**Ollama** and **LiteLLM**) without having to manually modify `config.yaml`.

- **Arguments**:
  - `[optional]` `switch` — Toggle active AI inference provider between `ollama` and `litellm`.

#### Execution Modes
| Syntax | Purpose | Action Taken |
|---|---|---|
| `ainf` | View Active Provider | Reads and displays current `selected_ai_inference` from `config.yaml` |
| `ainf switch` | Switch Provider | Toggles between `ollama` ↔ `litellm` and writes directly to `config.yaml` |

#### Usage Examples
```bash
>>> ainf
Active AI-Inference (provider): ollama

>>> ainf switch
Switched to AI-Inference (provider): litellm

>>> ainf switch
Switched to AI-Inference (provider): ollama
```

#### Under the Hood
ElasticEase checks the `selected_ai_inference` property inside `config.yaml`. When executed with `switch`, it toggles the value between local offline inference (`ollama`) and multi-model cloud gateway (`litellm`), persists the change immediately via YAML serialization, and prints confirmation to the console. If no provider is configured or an unrecognized value is found, it automatically initializes or recovers by defaulting to `ollama`.

---

<a id="11-newpass--newcred"></a>
### 11. `newpass` / `newcred`

Updates the Elasticsearch user password in `config.yaml` directly from the terminal.

- **Aliases**: `newpass`, `newcred`
- **Arguments**:
  - `[required]` `<password>` — New plaintext password string.

#### Usage Examples
```bash
>>> newpass "MyNewSecur3P@ssw0rd!"
>>> newcred "SuperSecret456#"
```

---

<a id="12-help"></a>
### 12. `help`

Interactive documentation viewer. Displays the complete command catalog or renders detailed syntax, arguments, and practical examples for an individual command.

- **Arguments**:
  - `[optional]` `<command_name>` — Name of command to inspect (e.g., `nodes`, `addoc`, `index:new`).

#### Usage Examples
```bash
>>> help
>>> help "nodes"
>>> help "index:new"
>>> help "updoc"
```

---

<a id="13-clear--cls"></a>
### 13. `clear` / `cls`

Clears the terminal viewport using ANSI escape codes (`\033[2J\033[H`).

#### Usage Examples
```bash
>>> clear
>>> cls
```

---

<a id="14-exit--quit--q"></a>
### 14. `exit` / `quit` / `q`

Terminates the interactive ElasticEase CLI session cleanly.

#### Usage Examples
```bash
>>> exit
>>> quit
>>> q
>>> ex
```

---

<a id="crud--document-management-commands"></a>
## 📦 CRUD & Document Management Commands

<a id="15-indexnew"></a>
### 15. `index:new`

Creates a new Elasticsearch index. Supports either dynamic schema generation (Elasticsearch infers types on first insert) or explicit interactive custom mappings.

- **Elasticsearch API**: `PUT /{index_name}`
- **Arguments**:
  - `[required]` `<index_name>` — Name of the new index.
  - `[optional]` `"mappings"` — Flag to trigger custom mapping builder.

#### Mode A: Dynamic Mapping (Default)
```bash
>>> index:new "students"
```
*Creates the index immediately with Elasticsearch default schema handling.*

#### Mode B: Custom Explicit Mapping
```bash
>>> index:new "students" "mappings"
```
*Triggers an interactive prompt:*
```text
Please enter the fields with valid type annotations:
Provide just like that - e.g. "name=text age=integer address=text about=text"
> name=text age=integer email=keyword gpa=float enrolled=boolean

Please recheck your provided mappings:
confirm [Y]/[N]: y
```
*Constructs the payload:*
```json
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "age": { "type": "integer" },
      "email": { "type": "keyword" },
      "gpa": { "type": "float" },
      "enrolled": { "type": "boolean" }
    }
  }
}
```

---

<a id="16-indexdel"></a>
### 16. `index:del`

Permanently deletes an existing index along with all indexed documents and shard data.

- **Elasticsearch API**: `DELETE /{index_name}`
- **Arguments**:
  - `[required]` `<index_name>` — Name of index to delete.

#### Usage Example
```bash
>>> index:del "students"
```

> [!CAUTION]
> This operation is irreversible. All Lucene segment files and documents for this index will be permanently removed from your Elasticsearch cluster.

---

<a id="17-inspectdoc"></a>
### 17. `inspect:doc`

Fetches and displays a single document by its unique Elasticsearch `_id`.

- **Elasticsearch API**: `GET /{index_name}/_doc/{document_id}`
- **Arguments**:
  - `[required]` `<index_name>` — Target index name.
  - `[required]` `<document_id>` — Document identifier.

#### Usage Example
```bash
>>> inspect:doc "students" "Y38386ABt5Meyqi5CwMR"
```

#### Sample Response Output
```json
{
  "_index": "students",
  "_id": "Y38386ABt5Meyqi5CwMR",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "name": "John Doe",
    "age": "22",
    "major": "Computer Science"
  }
}
```

---

<a id="18-inspectindex"></a>
### 18. `inspect:index`

Previews the stored contents of an index by performing a query to fetch the latest documents (default size: up to 100 documents).

- **Elasticsearch API**: `GET /{index_name}/_search?size=100`
- **Arguments**:
  - `[required]` `<index_name>` — Name of the index to preview.

#### Usage Example
```bash
>>> inspect:index "students"
```

---

<a id="19-addoc"></a>
### 19. `addoc`

Inserts a single document into an existing index using intuitive `key=value` string syntax. Elasticsearch automatically assigns a unique document ID.

- **Elasticsearch API**: `POST /{index_name}/_doc`
- **Arguments**:
  - `[required]` `<index_name>` — Target index name.
  - `[required]` `<key_values>` — Key-value pairs. Spaces within values must be single-quoted.

#### Usage Example
```bash
>>> addoc "students" "name=Alice age=23 major='Data Science' city='San Francisco'"
```

#### Under the Hood
ElasticEase parses the key-value sequence into a native Python dictionary:
```json
{
  "name": "Alice",
  "age": "23",
  "major": "Data Science",
  "city": "San Francisco"
}
```
It then issues an async POST request to `/{index_name}/_doc` and prints the resulting JSON containing the auto-generated `_id`, `_seq_no`, and status code `201 (Created)`.

---

<a id="20-addocs"></a>
### 20. `addocs`

Performs high-throughput bulk ingestion of multiple documents from a local `.json` file using Elasticsearch's NDJSON `_bulk` API.

- **Elasticsearch API**: `POST /{index_name}/_bulk` (Content-Type: `application/x-ndjson`)
- **Arguments**:
  - `[required]` `<index_name>` — Target index name.
  - `[required]` `<path_to_data_file>` — Absolute or relative path to a JSON file containing an array of document objects.

#### Usage Example
```bash
>>> addocs "students" "./data/new_students.json"
>>> addocs "catalog" "C:/Users/user/data/products.json"
```

#### Data File Format (`new_students.json`)
```json
[
  {
    "name": "Elena Rostova",
    "age": 24,
    "course": "Distributed Systems"
  },
  {
    "_id": "custom-id-9981",
    "name": "Carlos Gomez",
    "age": 22,
    "course": "Cloud Architecture"
  }
]
```
*(If `_id` or `id` is present, it will be assigned as the document's ID. Otherwise, Elasticsearch generates an automatic ID).*

---

<a id="21-updoc"></a>
### 21. `updoc`

Updates an existing document in an index using **Optimistic Concurrency Control (OCC)** to prevent lost updates or race conditions.

- **Elasticsearch API**: 
  1. `GET /{index_name}/_doc/{document_id}` (fetches latest `_seq_no` & `_primary_term`)
  2. `POST /{index_name}/_update/{document_id}?if_seq_no={seq_no}&if_primary_term={primary_term}`
- **Arguments**:
  - `[required]` `<index_name>` — Name of index.
  - `[required]` `<document_id>` — Target document ID.
  - `[required]` `<key_values>` — Updated key-value pairs.

#### Usage Example
```bash
>>> updoc "students" "Y38386ABt5Meyqi5CwMR" "age=25 major='Artificial Intelligence'"
```

---

<a id="22-updocs"></a>
### 22. `updocs`

Performs bulk document updates across multiple records from a JSON file while validating OCC sequence numbers for every individual document. Includes an interactive confirmation prompt.

- **Elasticsearch API**:
  1. Multiple `GET /{index_name}/_doc/{doc_id}` to resolve current version vectors.
  2. `POST /{index_name}/_bulk` with `if_seq_no` and `if_primary_term` actions.
- **Arguments**:
  - `[required]` `<index_name>` — Name of the target index.
  - `[required]` `<data_file_path>` — Path to JSON file containing document updates with IDs.

#### Usage Example
```bash
>>> updocs "students" "./data/updates.json"
```
*Prompt:*
```text
Are you sure? [Y] / [N]: y
```

#### Input File Requirement (`updates.json`)
Every object in the JSON file **must** include an `id` or `_id` field:
```json
[
  {
    "id": "Y38386ABt5Meyqi5CwMR",
    "age": 26,
    "grade": "A+"
  },
  {
    "id": "ZH8386ABt5Meyqi5CwMR",
    "age": 23,
    "grade": "A"
  }
]
```

---

<a id="23-deldoc"></a>
### 23. `deldoc`

Deletes a single document from an index by its ID.

- **Elasticsearch API**: `DELETE /{index_name}/_doc/{document_id}`
- **Arguments**:
  - `[required]` `<index_name>` — Name of index.
  - `[required]` `<document_id>` — ID of document to delete.

#### Usage Example
```bash
>>> deldoc "students" "Y38386ABt5Meyqi5CwMR"
```

---

<a id="24-deldocs"></a>
### 24. `deldocs`

Performs high-performance bulk deletion of multiple documents using the `_bulk` API. Includes an interactive confirmation prompt to prevent accidental data loss.

- **Elasticsearch API**: `POST /{index_name}/_bulk` (with `"delete"` action headers)
- **Arguments**:
  - `[required]` `<index_name>` — Target index.
  - `[required]` `<targets_data_file>` — Path to a JSON file containing objects with IDs to delete.

#### Usage Example
```bash
>>> deldocs "students" "./data/to_delete.json"
```
*Prompt:*
```text
Are you sure? [Y] / [N]: y
```

#### Targets File Format (`to_delete.json`)
```json
[
  { "id": "Y38386ABt5Meyqi5CwMR" },
  { "id": "ZH8386ABt5Meyqi5CwMR" },
  { "id": "custom-id-9981" }
]
```

---

<a id="bulk-data-file-formats-json"></a>
## 📂 Bulk Data File Formats (.json)

ElasticEase standardizes batch file interactions for `addocs`, `updocs`, and `deldocs`. Here is a quick reference matrix:

| Command | File Content Schema | Requires ID? | Example |
|---|---|---|---|
| `addocs` | Array of JSON objects | Optional (auto-generated if omitted) | `[ {"title": "Book 1", "price": 29.99} ]` |
| `updocs` | Array of objects with `id` or `_id` and update fields | **Mandatory** | `[ {"id": "doc123", "price": 34.99} ]` |
| `deldocs` | Array of objects with `id` or `_id` | **Mandatory** | `[ {"id": "doc123"}, {"id": "doc456"} ]` |

---

<a id="optimistic-concurrency-control-occ-mechanics"></a>
## 🔒 Optimistic Concurrency Control (OCC) Mechanics

### Why OCC is Critical in Elasticsearch
In high-throughput environments, multiple users or workers may attempt to read and mutate the same document simultaneously. Without concurrency controls:
1. Client A reads document version 1.
2. Client B reads document version 1.
3. Client A writes changes (version 2).
4. Client B writes changes (overwriting Client A's changes blindly — the classic **Lost Update Problem**).

### How ElasticEase Handles OCC
Whenever you execute `updoc` or `updocs`:
1. **Pre-flight Sequence Fetch**: ElasticEase automatically queries `GET /{index}/_doc/{id}` to obtain the active `_seq_no` and `_primary_term`.
2. **Conditional Update Request**: ElasticEase crafts the update request with the query parameters:
   ```text
   POST /{index}/_update/{id}?if_seq_no={seq_no}&if_primary_term={primary_term}
   ```
3. **Conflict Detection**: If another process modified the document between your read and update, Elasticsearch returns a `409 Version Conflict`. ElasticEase catches this and presents a clear error, preventing silent data corruption.

---

*For additional assistance or issues, run `help <command>` inside the ElasticEase CLI.*
