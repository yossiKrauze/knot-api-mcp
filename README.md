# KnotAPI MCP Integration

## ⚠️ DISCLAIMER
**This is a PROOF OF CONCEPT (POC) implementation only and is NOT intended for production use.** 
This project is for demonstration and testing purposes only. There are no valid .env, config, or secrets credential configuration. The backend service is NOT a real KnotAPI service; it's a mock implementation using FastAPI and does no real authentication or authorization.

## Overview
This project provides a Model Context Protocol (MCP) integration for KnotAPI services. It allows AI assistants like Claude to interact with KnotAPI services through a standardized protocol.

## Components

### MCP Server (`knot-api-mcp.py`)
The main MCP server implementation that exposes KnotAPI functionality as MCP tools:

- `list_merchants`: List available merchants
- `switch_card`: Switch a card for a user
- `create_session`: Create a new session
- `extend_session`: Extend an existing session

### Test Service (`test/test_service/app.py`)
A FastAPI-based mock service that simulates the KnotAPI backend for testing purposes. It provides endpoints for:

- `/merchant/list`: Get a list of merchants
- `/session/create`: Create a new session
- `/session/extend`: Extend an existing session
- `/card`: Switch a card

### Data Models (`data/models.py`)
Pydantic models that define the data structures used by both the MCP server and test service.

## Getting Started

### Prerequisites
- Python 3.11+
- uv package manager

### Running the Test Service
```bash
cd /Users/yossikrauze/Dev/knotapi
uv run -m uvicorn knot-api-mcp.test.test_service.app:app --reload --port 8002
```

### Running the MCP Server
```bash
cd /Users/yossikrauze/Dev/knotapi
uv run knot-api-mcp.py
```

### Connecting with Claude Desktop
1. Configure Claude Desktop to use the MCP server by updating `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "knot-api-mcp": {
      "command": "/PATH_TO/.local/bin/uv",
      "args": [
        "run",
        "--with",
        "httpx",
        "--with",
        "mcp[cli]",
        "--with",
        "pydantic",
        "--with",
        "requests",
        "mcp",
        "run",
        "/PATH_TO/knot-api-mcp/knot-api-mcp.py"
      ]
    }
  }
}
```
2. Restart Claude Desktop
3. Check via the tools button that the MCP tools have been added

## Architecture
The project follows a layered architecture:
1. **MCP Layer**: Exposes KnotAPI functionality as MCP tools
2. **Service Layer**: Handles communication with the KnotAPI backend
3. **Model Layer**: Defines the data structures used throughout the application. Uses Pydantic models.

## Limitations
- No real KnotAPI integration
- Authentication is mocked with dummy credentials
- Error handling is minimal
- No rate limiting or throttling
- Limited validation of inputs
- No persistent storage

## Future Improvements
- Integrate with KnotAPI
- Iterate on the test service to have it match the KnotAPI endpoints and authentication & authorization
- Add proper authentication with API keys
- Implement comprehensive error handling
- Add logging and monitoring
- Implement rate limiting
- Add unit and integration tests
- Support for more KnotAPI endpoints

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.