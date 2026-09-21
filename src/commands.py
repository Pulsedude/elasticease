core_commands = [
    {
        "name": "health",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See health of Elastic Cluster (🤖)",
        "example": "health | health json | heath json true",
        "info": "Use this command to see active elastic cluster health or status. You can use commands in three different ways\n(i) health - Use when you need response in proper table format (more readable)\n(ii) health json - Use when you actually need a response in JSON format\n(iii) health json true - Use when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "shards",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See all available shards in your running node (🤖)",
        "info": "Use this command to see available shards on active nodes. You can use commands in three different ways\n(i) shards - Use when you need response in proper table format (more readable)\n(ii) shards json - Use when you actually need a response in JSON format\n(iii) shards json true - Use when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "indices",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See all available indices in your running nodes (🤖)",
        "info": "Use this command to see existing indices on the active nodes. You can use commands in three different ways\n(i) indices - Use when you need response in proper table format (more readable)\n(ii) indices json - Use when you actually need a response in JSON format\n(iii) indices json true - Use when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "ping",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "Ping to your Elastic cluster (🤖)",
        "info": "Use this command to ping to your elastic cluster. You can use commands in two different ways\n(i) ping - Use when you need response in JSON format\n(ii) ping true - Use when you need AI-powered summary on ping data\n"
    },
    {
        "name": "indexinfo",
        "arguments": {
            "required": "<index_name>",
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See details of target index (🤖)",
        "example": "indexinfo \"students\"",
        "info": "Use this command to see details of any such exising index. You can use commands in two different ways\n(i) indexinfo <index_name> - Use when you need response in JSON format\n(ii) indexinfo <index_name> true - Use when you need AI-powered summary to understand specific index\n"
    },
    {
        "name": "master",
        "arguments": {
            "required": None,
            "optional": "<json_response>"
        },
        "purpose": "See master nodes",
        "info": "Use this see active master node. You can use commands in two different ways\n(i) master - Use when you need response Table format (readable format)\n(ii) master json - Use when you want response in JSON format\n"
    },
    {
        "name": "nodes",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See total nodes running on the current cluster (🤖)",
        "info": "Use this command to active nodes on cluster. You can use commands in three different ways\n(i) nodes - Use when you need response in proper table format (more readable)\n(ii) nodes json - Use when you actually need a response in JSON format\n(iii) nodes json true - Use when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "capacity",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See the total storage capacities of active nodes (🤖)",
        "info": "Use this command to see storage capacities of active nodes (allocated storage). You can use commands in three different ways\n(i) capacity - Use when you need response in proper table format (more readable)\n(ii) capacity json - Use when you actually need a response in JSON format\n(iii) capacity json true - Use when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "clear",
        "arguments": {
            "required": None,
            "optional": None
        },
        "purpose": "Clear console screen",
        "info": "Use this command to clear console screen. You can use commands in one way only\nclear or cls - Clear console screen\n"
    },
    {
        "name": "conn",
        "arguments": {
            "required": "<URL>",
            "optional": None
        },
        "purpose": "Change a connection URL for Elasticsearch to allow Elasticease to make connection",
        "example": "conn \"https://localhost:9200\"",
        "info": "Use this command to change or add new elastic connection base URL. You can use commands in one way only\nconn \"https://localhost:9200\" - Update or add new elastic connection base URL\n"
    },
    {
        "name": "newcred <password>",
        "arguments": {
            "required": None,
            "optional": None
        },
        "purpose": "Add or Update new Elasticsearch credentials (username, password)  for Elasticease to make connection",
        "example": "newcred \"1234@newpasswordXYZ\"",
        "info": "Use this command to add or update elasticsearch credentials to make connection with elasticsearch. You can use commands in one way only\nnewcred \"1234@newpasswordXYZ\" - Add or update elasticsearch credentials\n"
    }
]

crud_commands = [
    {
        "name": "index:new <index_name>",
        "purpose": "Create a new index",
        "example": "index:new \"students\""
    },
    {
        "name": "index:del <index_name>",
        "purpose": "index:del a existing index",
        "example": "delete \"students\""
    },
    {
        "name": "addoc <index_name> <document>",
        "purpose": "Add a document into a index",
        "example": "addoc \"students\" \"name: John, age: 18, interest: AI\""
    },
    {
        "name": "inspect:doc <index_name> <document_id>",
        "purpose": "See specific document of any such existing index",
        "example": "inspect:doc \"students\" \"12345XYSA_abc\""
    },
    {
        "name": "inspect:index <index_name>",
        "purpose": "See any such existing specific index with their stored data",
        "example": "inspect:index \"students\""
    },
    {
        "name": "updoc <index_name> <document_id> <document>",
        "purpose": "Update a document of existing index",
        "example": "updoc \"students\" \"12345XYSA_abc\" \"name: John, interest: Backend\""
    }
]
