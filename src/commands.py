core_commands = [
    {
        "name": "health",
        "purpose": "See health of Elastic Cluster",
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
        "name": "index \"index_name\"",
        "purpose": "See details of target index",
        "example": "index \"students\""
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
    }
]

crud_command = [
    {
        "name": "create \"index_name\"",
        "purpose": "Create a new index",
        "example": "create \"students\""
    },
    {
        "name": "delete \"index_name\"",
        "purpose": "Delete a existing index",
        "example": "delete \"students\""
    },
    {
        "name": "add \"index_name\" \"document\"",
        "purpose": "Add a document into a index",
        "example": "add \"students\" \"name: John, age: 18, interest: AI\""
    },
    {
        "name": "see \"index_name\" \"document_id\"",
        "purpose": "See specific document of any index",
        "example": "see \"students\" \"12345XYSA_abc\""
    },
    {
        "name": "update \"index_name\" \"document_id\" \"document\"",
        "purpose": "Update a document of existing index",
        "example": "update \"students\" \"12345XYSA_abc\" \"name: John, interest: Backend\""
    }
]