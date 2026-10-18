core_commands = [
    {
        "name": "health",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See health of Elastic Cluster (🤖)",
        "example": "health | health json | heath json true",
        "info": "Use it command to see active elastic cluster health or status. You can use commands in three different ways\n(i) health - Use it when you need response in proper table format (more readable)\n(ii) health json - Use when you actually need a response in JSON format\n(iii) health json true - Use it when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "shards",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See all available shards in your running node (🤖)",
        "example": "shards | shards json | shards json true",
        "info": "Use it command to see available shards on active nodes. You can use commands in three different ways\n(i) shards - Use when you need response in proper table format (more readable)\n(ii) shards json - Use it when you actually need a response in JSON format\n(iii) shards json true - Use it when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "indices",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See all available indices in your running nodes (🤖)",
        "example": "indices | indices json | indices json true",
        "info": "Use it command to see existing indices on the active nodes. You can use commands in three different ways\n(i) indices - Use it when you need response in proper table format (more readable)\n(ii) indices json - Use when you actually need a response in JSON format\n(iii) indices json true - Use it when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "ping",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "Ping to your Elastic cluster (🤖)",
        "example": "ping | ping true",
        "info": "Use this command to ping to your elastic cluster. You can use commands in two different ways\n(i) ping - Use it when you need response in JSON format\n(ii) ping true - Use it when you need AI-powered summary on ping data\n"
    },
    {
        "name": "indexinfo",
        "arguments": {
            "required": "<index_name>",
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See details of target index (🤖)",
        "example": "indexinfo \"students\" | indexinfo \"students\" true",
        "info": "Use this command to see details of any such exising index. You can use commands in two different ways\n(i) indexinfo <index_name> - Use it when you need response in JSON format\n(ii) indexinfo <index_name> true - Use it when you need AI-powered summary to understand specific index\n"
    },
    {
        "name": "master",
        "arguments": {
            "required": None,
            "optional": "<json_response>"
        },
        "purpose": "See master nodes",
        "example": "master | master json",
        "info": "Use this command to see active master node. You can use commands in two different ways\n(i) master - Use it when you need response Table format (readable format)\n(ii) master json - Use it when you want response in JSON format\n"
    },
    {
        "name": "nodes",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See total nodes running on the current cluster (🤖)",
        "example": "nodes | nodes json | nodes json true",
        "info": "Use this command to see active nodes on cluster. You can use commands in three different ways\n(i) nodes - Use it when you need response in proper table format (more readable)\n(ii) nodes json - Use it when you actually need a response in JSON format\n(iii) nodes json true - Use it when you need JSON response with AI-powered summary\n"
    },
    {
        "name": "capacity",
        "arguments": {
            "required": None,
            "optional": "<json_response> <ai_summary>"
        },
        "purpose": "See the total storage capacities of active nodes (🤖)",
        "example": "capacity | capacity json | capacity json true",
        "info": "Use this command to see storage capacities of active nodes (allocated storage). You can use commands in three different ways\n(i) capacity - Use it when you need response in proper table format (more readable)\n(ii) capacity json - Use when you actually need a response in JSON format\n(iii) capacity json true - Use it when you need JSON response with AI-powered summary\n"
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
        "purpose": "Change a connection URL for Elasticsearch to allow elasticease to make connection",
        "example": "conn \"https://localhost:9200\"",
        "info": "Use this command to change or add new elastic connection base URL. You can use commands in one way only\nconn \"https://localhost:9200\" - Update or add new elastic connection base URL\n"
    },
    {
        "name": "ainf",
        "arguments": {
            "required": None,
            "optional": "switch"
        },
        "purpose": "See current selected & active AI Inference (provider) or switch to another AI-Inference from available options Ollama or LiteLLM",
        "example": "ainf | ainf switch",
        "info": "Use this command to see your current selected AI Inference (provider). You can use commands in two ways\n(i) ainf - Use it to see selected & active AI Inference (provider)\n(ii) ainf switch - Use it to switch to another AI Inference (provider)"
    },
    {
        "name": "newpass <password>",
        "arguments": {
            "required": None,
            "optional": None
        },
        "purpose": "Add or Update new Elasticsearch password for elasticease to make connection",
        "example": "newpass \"1234@newpasswordXYZ\"",
        "info": "Use this command to add or update elasticsearch credentials to make connection with elasticsearch. You can use commands in one way only\nnewpass \"1234@newpasswordXYZ\" - Add or update elasticsearch pasword to make connection with elasticsearch\n"
    },
    {
        "name": "help",
        "arguments": {
            "required": None,
            "optional": "<command_name>"
        },
        "purpose": "See all available commands or see usage of any specific available command",
        "example": "help | help \"nodes\"",
        "info": "Use this command to see all available commands (options) or to see or usage of specific available command. You can use commands in two ways\n(i)help - Use it when you want to see all available commands (options)\n(ii)help <command_name> - Use it when you want to know the usage of any specific command\n"
    }
]

crud_commands = [
    {
        "name": "index:new",
        "arguments": {
            "required": "<index_name>",
            "optional": "<with_mappings>"
        },
        "purpose": "Create a new index with or without custom mappings",
        "example": "index:new \"students\" | index:new \"students\" \"mappings\"",
        "info": "Use this command create new index with or without custom mappings. You can use commands in two ways\n(i)index:new <index_name> - Use it when you don't want a custom mappings, elasticsearch will create automatically for you according to data fields\n(ii)index:new <index_name> \"true\"- Use it when you want provide a custom mappings according to data fields\n"
    },
    {
        "name": "index:del",
        "arguments": {
            "required": "<index_name>",
            "optional": None
        },
        "purpose": "Delete eixsting index with their stored data",
        "example": "index:del \"students\"",
        "info": "Use this command to delete existing data with their data. You can use commands in one way only\n(i)index:del <index_name>  - Use it when you want to delete an existing index with their stored data (use it with caution)\n"
    },
    {
        "name": "inspect:doc",
        "arguments": {
            "required": "<index_name> <document_id>",
            "optional": None
        },
        "purpose": "See specific document of any such existing index",
        "example": "inspect:doc \"students\" \"12345XYSA_abc\"",
        "info": "Use this to inspect existing document from any such existing index. You can use commands in one way only\n(i)inspect:doc <index_name> <document_id> - Use it to inspect single existing document\n"
    },
    {
        "name": "inspect:index",
        "arguments": {
            "required": "<index_name>",
            "optional": None
        },
        "purpose": "See any such existing specific index with their stored data",
        "example": "inspect:index \"students\"",
        "info": "Use this command to inspect existing index with their stored data. You can use commands in one way only\n(i)inspect:index <index_name>  - Use it to inspect any such existing index with their stored data\n"
    },
    {
        "name": "addoc",
        "arguments": {
            "required": "<index_name> <key_values>",
            "optional": None
        },
        "purpose": "Insert a document into a index",
        "example": "addoc \"students\" \"name=john age=22 hobby=\'playing video games\'\"",
        "info": "Use this command insert new document into existing index. You can use commands in one way only\n(i)addoc <index_name> \"name=john age=22 hobby=\'playing video games\'\"  - Use it to insert new single document into existing index \n"
    },
    {
        "name": "addocs",
        "arguments": {
            "required": "<index_name> <path_to_data_file>",
            "optional": None
        },
        "purpose": "Add a multiple documents directly from specific data (.json) file",
        "example": "addocs \"students\" \"/path/to/data.json\"",
        "info": "Use this command insert multiple documents by reading specific data (.json) file. You can use commands in one way only\n(i)addocs <index_name> \"/path/to/data.json\"  - Use it to insert multiple documents from spsecific data (.json) file\n"
    },
    {
        "name": "updoc",
        "arguments": {
            "required": "<index_name> <document_id> <document>",
            "optional": None
        },
        "purpose": "Update single document of existing index (with OCC control)",
        "example": "updoc \"students\" \"12345XYSA_abc\" \"name=John hobby=\'do coding\'\"",
        "info": "Use this command to update single exsting document. You can use commands in one way only\n(i)updoc <index_name> <document_id> \"name=kelvin age=22 role=\'making DIY crafts\'\" - Use it to update single existing document\n"
    },
    {
        "name": "updocs",
        "arguments": {
            "required": "<index_name> <data_file_path>",
            "optional": None
        },
        "purpose": "Update multiple documents of existing index (with OCC control)",
        "example": "updoc \"students\" \"path/to/data.json\"",
        "info": "Use this command to update multiple exsting documents. You can use commands in one way only\n(i)updocs <index_name> \"path/to/data.json\" - Use it update multiple existing documents\n"
    },
    {
        "name": "deldoc",
        "arguments": {
            "required": "<index_name> <document_id>",
            "optional": None
        },
        "purpose": "Delete any such particular single document",
        "example": "deldoc \"students\" \"2\"",
        "info": "Use this command to delete any such particular single document. You can use commands in one way only\n(i)deldoc <index_name> <document_id>- Use it for delete single document\n"
    },
    {
        "name": "deldocs",
        "arguments": {
            "required": "<index_name> <targets>",
            "optional": None
        },
        "purpose": "Delete multiple documents at once",
        "example": "deldocs \"students\" \"path/to/targets.json\"",
        "info": "Use this command to delete multiple documents at once. You can use commands in one way only\n(i)deldoc <index_name> <targets> - Use it to delete multiple documents at once\n"
    }
]
