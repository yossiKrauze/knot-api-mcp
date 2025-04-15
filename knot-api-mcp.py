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


mcp = FastMCP("knot-api-mcp",
              dependencies=["pydantic", "requests", "httpx", "mcp[cli]"])


def call_service(endpoint: str, payload: Dict[str, Any], method: str = "POST") -> Dict[str, Any]:
    """
    Common function to call the test service
    
    Args:
        endpoint: The API endpoint to call (without the base URL)
        payload: The request payload
        method: HTTP method (GET, POST, etc.)
        
    Returns:
        The API response as a dictionary
    """
    try:
        # Construct the full URL
        base_url = "http://127.0.0.1:8002"
        url = f"{base_url}/{endpoint.lstrip('/')}"
        
        # Create auth header - dummy username and password
        # TODO - create a settings class to get it from a .env file, a keyring, a config file, or secrets
        auth_string = "username:password"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"Calling service: {method} {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Make the API call
        response = requests.request(method, url, json=payload, headers=headers)
        
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code >= 200 and response.status_code < 300:
            try:
                result = response.json()
                logger.info(f"Response: {json.dumps(result, indent=2)}")
                return result
            except:
                # Return text response if not JSON
                return {"response": response.text}
        else:
            error_msg = f"API call failed with status code {response.status_code}: {response.text}"
            logger.error(error_msg)
            return {"error": error_msg}
            
    except Exception as e:
        error_msg = f"Error calling service: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return {"error": error_msg}


@mcp.tool()
def list_merchants(
        type: str = "card_switcher",
        user_agent: Optional[str] = None) -> Dict[str, Any]:
    """
    List merchants for a user by calling the test service.

    Args:
        type: Type of merchant list request (card_switcher or transaction_link)
        user_agent: User agent string

    Returns:
        List of merchants
    """
    try:
        logger.info(f"list_merchants called with type={type}, user_agent={user_agent}")
        
        # Create the request payload
        payload = {
            "type": type,
            "user_agent": user_agent or "mcp-client",
            "external_user_id": "test-user-123",
            "status": "active",
            "search": ""
        }
        
        # Call the service
        return call_service("merchant/list", payload)
        
    except Exception as e:
        error_msg = f"Error listing merchants: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return {"error": error_msg}


@mcp.tool()
def switch_card(
        task_id: str,
        card_number: str,
        card_expiration: str,
        card_cvv: str) -> Dict[str, Any]:
    """
    Switch a card by calling the test service.
    
    Args:
        task_id: The task ID
        card_number: The card number
        card_expiration: The card expiration date
        card_cvv: The card CVV
        
    Returns:
        Success message or error
    """
    try:
        logger.info(f"switch_card called with task_id={task_id}")
        
        # Create a simplified payload with just the necessary fields
        payload = {
            "task_id": task_id,
            "user": {
                "name": {
                    "first_name": "Test",
                    "last_name": "User"
                },
                "phone_number": "555-555-5555",
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "region": "CA",
                    "postal_code": "12345",
                    "country": "US"
                }
            },
            "card": {
                "number": card_number,
                "expiration": card_expiration,
                "cvv": card_cvv
            }
        }
        
        # Call the service
        return call_service("card", payload)
        
    except Exception as e:
        error_msg = f"Error switching card: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return {"error": error_msg}


@mcp.tool()
def create_session(
        session_type: str,
        external_user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a session by calling the test service.
    
    Args:
        session_type: The session type
        external_user_id: External user ID
        
    Returns:
        Session ID or error
    """
    try:
        logger.info(f"create_session called with type={session_type}, external_user_id={external_user_id}")
        
        # Create the request payload
        payload = {
            "type": session_type,
            "external_user_id": external_user_id or "test-user-123"
        }
        
        # Call the service
        return call_service("session/create", payload)
        
    except Exception as e:
        error_msg = f"Error creating session: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return {"error": error_msg}


@mcp.tool()
def extend_session(session_id: str) -> Dict[str, Any]:
    """
    Extend a session by calling the test service.
    
    Args:
        session_id: The session ID to extend
        
    Returns:
        Updated session or error
    """
    try:
        logger.info(f"extend_session called with session_id={session_id}")
        
        # Create the request payload
        payload = {
            "session_id": session_id
        }
        
        # Call the service
        return call_service("session/extend", payload)
        
    except Exception as e:
        error_msg = f"Error extending session: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
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
