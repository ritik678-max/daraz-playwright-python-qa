POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {
            "type": "integer"
        },
        "id": {
            "type": "integer"
        },
        "title": {
            "type": "string"
        },
        "body": {
            "type": "string"
        }
    },
    "required": [
        "userId",
        "id",
        "title",
        "body"
    ]
}


USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "username": {
            "type": "string"
        },
        "email": {
            "type": "string"
        }
    },
    "required": [
        "id",
        "name",
        "username",
        "email"
    ]
}