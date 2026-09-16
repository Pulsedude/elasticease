core_commands = [
    {
        "name": "health <AI Summary>",
        "purpose": "See health of Elastic Cluster",
        "example": "health | health true"
    },
    {
        "name": "shards",
        "purpose": "See all available shards in your running node"
    },
    {
        "name": "indices",
        "purpose": "See all available indices in your running node"
    },
    {
        "name": "ping",
        "purpose": "Ping to your Elastic cluster"
    },
    {
        "name": "indexinfo <index_name>",
        "purpose": "See details of target index",
        "example": "indexinfo \"students\""
    },
    {
        "name": "master",
        "purpose": "See master nodes"
    },
    {
        "name": "nodes",
        "purpose": "See total nodes running on the current cluster"
    },
    {
        "name": "capacity",
        "purpose": "See the total storage capacities of active nodes"
    },
    {
        "name": "clear",
        "purpose": "Clear console screen"
    },
    {
        "name": "conn <URL>",
        "purpose": "Change a connection URL for Elasticsearch to allow Elasticease to make connection",
        "example": "conn \"https://my_instance_xyz:9200\""
    },
    {
        "name": "newcred <password>",
        "purpose": "Add or Update new Elasticsearch password for Elasticease to make connection",
        "example": "nrecred \"1234@newpasswordXYZ\""
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