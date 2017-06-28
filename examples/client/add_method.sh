#!/bin/bash

# request
# .............
curl --data-binary '{
    "jsonrpc": "2.0", 
    "id": "1", 
    "method": "v3.add",
    "params": {
        "x":1,
        "y":3
    }
}' \
-H 'content-type:application/json;' \
${API_URL} \
| python -m json.tool

# response
# .............
# {
#     "id": "1",
#     "jsonrpc": "2.0",
#     "result": 3
# }

