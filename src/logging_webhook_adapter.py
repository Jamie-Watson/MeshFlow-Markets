"""
Custom Logging Gateway Adapter for SAM Webhook Gateway.

This adapter wraps the webhook gateway functionality and adds prominent logging
for all gateway events - incoming requests and Agent Mesh responses.

Uses both logging module AND print statements with flush for guaranteed visibility.
"""

import logging
import json
import sys
from typing import Any, Dict, Optional

from solace_agent_mesh.gateway.adapter.base import GatewayAdapter
from solace_agent_mesh.gateway.adapter.types import (
    GatewayContext,
    ResponseContext,
    SamTask,
    SamUpdate,
)

log = logging.getLogger(__name__)

# Visual separator constants for prominent logging
SEPARATOR_THICK = "=" * 80
SEPARATOR_THIN = "-" * 80
ARROW_IN = ">" * 80
ARROW_OUT = "<" * 80
BANNER_START = "\n" + "#" * 80 + "\n" + "#" + " " * 30 + "GATEWAY EVENT" + " " * 35 + "#\n" + "#" * 80


def _log_and_print(message: str, level: str = "info") -> None:
    """Log and print a message for guaranteed visibility."""
    print(message, flush=True)
    sys.stdout.flush()
    getattr(log, level)(message)


def _format_payload(data: Any, indent: int = 2) -> str:
    """Format payload data for logging."""
    try:
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=indent, default=str)
        return str(data)
    except Exception:
        return str(data)


class LoggingWebhookAdapter(GatewayAdapter):
    """
    A gateway adapter that adds verbose logging for all webhook events.

    This adapter logs:
    - Incoming webhook requests with full payload
    - Tasks being sent to the Agent Mesh
    - All updates/responses from the Agent Mesh

    Uses both Python logging and print() for maximum visibility.
    """

    async def init(self, context: GatewayContext) -> None:
        """Initialize the logging adapter."""
        self.context = context
        _log_and_print(f"\n{SEPARATOR_THICK}")
        _log_and_print("    LOGGING WEBHOOK ADAPTER INITIALIZED")
        _log_and_print(f"    Gateway ID: {getattr(context, 'gateway_id', 'unknown')}")
        _log_and_print(f"{SEPARATOR_THICK}\n")

    async def prepare_task(
        self, external_input: Any, endpoint_context: Optional[Dict[str, Any]] = None
    ) -> SamTask:
        """
        Prepare a task from incoming webhook data with verbose logging.

        This method is called when a webhook request is received.
        """
        _log_and_print(BANNER_START)
        _log_and_print(f"\n{SEPARATOR_THICK}")
        _log_and_print(f"{ARROW_IN}")
        _log_and_print("    INCOMING WEBHOOK REQUEST RECEIVED")
        _log_and_print(f"{ARROW_IN}")
        _log_and_print(f"{SEPARATOR_THIN}")

        # Log endpoint context
        if endpoint_context:
            _log_and_print("\n    ENDPOINT CONTEXT:")
            _log_and_print(_format_payload(endpoint_context))
            _log_and_print(f"{SEPARATOR_THIN}")

        # Log the raw external input
        _log_and_print("\n    RAW EXTERNAL INPUT PAYLOAD:")
        _log_and_print(f"{SEPARATOR_THIN}")
        _log_and_print(_format_payload(external_input))
        _log_and_print(f"{SEPARATOR_THIN}")

        # Extract payload details if possible
        if isinstance(external_input, dict):
            _log_and_print("\n    PAYLOAD BREAKDOWN:")
            for key, value in external_input.items():
                formatted_val = _format_payload(value)
                if len(formatted_val) > 500:
                    formatted_val = formatted_val[:500] + "... [TRUNCATED]"
                _log_and_print(f"      {key}: {formatted_val}")

        _log_and_print(f"\n{ARROW_IN}")
        _log_and_print(f"{SEPARATOR_THICK}\n")

        # Create the SamTask - this is where you'd normally transform the input
        # For the webhook gateway, we create a simple text task
        task_text = external_input if isinstance(external_input, str) else _format_payload(external_input)

        from solace_agent_mesh.common.a2a import create_text_part

        task = SamTask(
            target_agent="OrchestratorAgent",
            content=[create_text_part(task_text)],
            metadata={"source": "logging_webhook_adapter"}
        )

        _log_and_print(f"\n{SEPARATOR_THIN}")
        _log_and_print("    PREPARED SAM TASK:")
        _log_and_print(f"      Target Agent: {task.target_agent}")
        _log_and_print(f"      Content Parts: {len(task.content)}")
        _log_and_print(f"{SEPARATOR_THIN}\n")

        return task

    async def handle_update(
        self, update: SamUpdate, context: ResponseContext
    ) -> None:
        """
        Handle updates from the Agent Mesh with verbose logging.

        This method is called for each update/response from agents.
        """
        _log_and_print(BANNER_START)
        _log_and_print(f"\n{SEPARATOR_THICK}")
        _log_and_print(f"{ARROW_OUT}")
        _log_and_print("    AGENT MESH RESPONSE/UPDATE RECEIVED")
        _log_and_print(f"{ARROW_OUT}")
        _log_and_print(f"{SEPARATOR_THIN}")

        # Log update type and status
        update_type = type(update).__name__
        _log_and_print(f"\n    UPDATE TYPE: {update_type}")

        # Log response context
        _log_and_print(f"\n    RESPONSE CONTEXT:")
        _log_and_print(f"      Session ID: {getattr(context, 'session_id', 'N/A')}")
        _log_and_print(f"      Task ID: {getattr(context, 'task_id', 'N/A')}")
        _log_and_print(f"      User ID: {getattr(context, 'user_id', 'N/A')}")

        _log_and_print(f"\n{SEPARATOR_THIN}")
        _log_and_print("    UPDATE DETAILS:")

        # Log the full update object
        if hasattr(update, '__dict__'):
            for attr_name, attr_value in vars(update).items():
                if not attr_name.startswith('_'):
                    formatted_value = _format_payload(attr_value)
                    # Truncate very long values but show them
                    if len(formatted_value) > 2000:
                        _log_and_print(f"      {attr_name} (truncated):")
                        _log_and_print(f"        {formatted_value[:2000]}...")
                        _log_and_print(f"        [Total length: {len(formatted_value)} chars]")
                    else:
                        _log_and_print(f"      {attr_name}:")
                        _log_and_print(f"        {formatted_value}")
        else:
            _log_and_print(f"      Raw Update: {_format_payload(update)}")

        # Check for specific update types and log accordingly
        if hasattr(update, 'text') and update.text:
            _log_and_print(f"\n{SEPARATOR_THIN}")
            _log_and_print("    TEXT CONTENT:")
            _log_and_print(f"      {update.text}")

        if hasattr(update, 'status') and update.status:
            _log_and_print(f"\n{SEPARATOR_THIN}")
            _log_and_print(f"    STATUS: {update.status}")

        if hasattr(update, 'error') and update.error:
            _log_and_print(f"\n{SEPARATOR_THIN}")
            _log_and_print(f"    ERROR: {update.error}")

        if hasattr(update, 'artifacts') and update.artifacts:
            _log_and_print(f"\n{SEPARATOR_THIN}")
            _log_and_print("    ARTIFACTS:")
            for artifact in update.artifacts:
                _log_and_print(f"      - {_format_payload(artifact)}")

        _log_and_print(f"\n{ARROW_OUT}")
        _log_and_print(f"{SEPARATOR_THICK}\n")

    async def on_task_complete(self, context: ResponseContext) -> None:
        """Called when a task is fully complete."""
        _log_and_print(f"\n{SEPARATOR_THICK}")
        _log_and_print("    TASK COMPLETED")
        _log_and_print(f"      Session ID: {getattr(context, 'session_id', 'N/A')}")
        _log_and_print(f"      Task ID: {getattr(context, 'task_id', 'N/A')}")
        _log_and_print(f"{SEPARATOR_THICK}\n")

    async def on_error(self, error: Exception, context: Optional[ResponseContext] = None) -> None:
        """Handle errors with verbose logging."""
        _log_and_print(f"\n{SEPARATOR_THICK}", "error")
        _log_and_print("    ERROR IN GATEWAY PROCESSING", "error")
        _log_and_print(f"{SEPARATOR_THIN}", "error")
        _log_and_print(f"    Error Type: {type(error).__name__}", "error")
        _log_and_print(f"    Error Message: {str(error)}", "error")
        if context:
            _log_and_print(f"    Context Session ID: {getattr(context, 'session_id', 'N/A')}", "error")
            _log_and_print(f"    Context Task ID: {getattr(context, 'task_id', 'N/A')}", "error")
        _log_and_print(f"{SEPARATOR_THICK}\n", "error")
        log.error("Full traceback:", exc_info=True)
