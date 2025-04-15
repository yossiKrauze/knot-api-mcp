from mcp.server.fastmcp import FastMCP, Context
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from enum import Enum
import requests
import base64
import json
import sys
import logging
import traceback

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("knot-api-mcp")

# Print startup message to stderr for debugging
print("Starting knot-api-mcp server...", file=sys.stderr)


class Merchant(BaseModel):
    name: str
    external_merchant_id: str
    card_id: str


class MerchantListRequestType(Enum):
    CARD_SWITCHER = "card_switcher"
    TRANSACTION_LINK = "transaction_link"


class MerchantListRequest(BaseModel):
    type: MerchantListRequestType
    platform: Optional[str] = None
    user_agent: Optional[str] = None
    search: Optional[str] = None
    external_user_id: Optional[str] = None
    status: Optional[str] = None


class ListMerchantsResponse(BaseModel):
    merchants: List[Merchant]


# Create a named server
mcp = FastMCP("knot-api-mcp",
              dependencies=["pydantic", "requests", "httpx", "mcp[cli]"])

# Print server info to stderr for debugging
print(f"Created MCP server: {mcp}", file=sys.stderr)


@mcp.tool()
def list_merchants(ctx: Context,
                   type: str = "card_switcher",
                   user_agent: Optional[str] = None) -> Dict[str, Any]:
    """
    List merchants for a user by calling the test service.

    Args:
        type: Type of merchant list request (card_switcher or transaction_link)

    Returns:
        List of merchants
    """
    try:
        logger.info(
            f"list_merchants called with type={type}, user_agent={user_agent}")

        # Call the test service directly
        url = "http://127.0.0.1:8002/merchant/list"

        # Create the request payload
        payload = {
            "type": type,
            "user_agent": user_agent or "mcp-client",
            "external_user_id": "test-user-123",
            "status": "active",
            "search": ""
        }

        # Create auth header
        auth_string = "username:password"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json"
        }

        logger.info(f"Sending request to {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")

        # Make the API call
        response = requests.post(url, json=payload, headers=headers)

        logger.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            logger.info(f"Response: {json.dumps(result, indent=2)}")
            return result
        else:
            error_msg = f"API call failed with status code {response.status_code}: {response.text}"
            logger.error(error_msg)
            return {"error": error_msg}

    except Exception as e:
        error_msg = f"Error listing merchants: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        ctx.print(error_msg)
        return {"error": error_msg}


if __name__ == "__main__":
    try:
        # NOT NEEDED when running from Claude desktop - it will depend on the claude_desktop_config.json
        # needed for debugging when running from the command line or via the inspector
        print("Starting MCP server run...", file=sys.stderr)
        mcp.run()
    except Exception as e:
        error_msg = f"Error running MCP server: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        print(error_msg, file=sys.stderr)
        sys.exit(1)
