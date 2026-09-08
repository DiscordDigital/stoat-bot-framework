import asyncio
import httpx
import threading
from dataclasses import dataclass

# Used by listener function as data class for events
@dataclass
class Event:
    name: str | None
    data: str

# The listener dispatches events from the API for the modules.
async def listener(event: Event, bot, apiEvent):
    # Ping module support.
    if (event.name == "ping"):
        await apiEvent.dispatch("ping", event.data)

# This function waits for the apiEvent to be ready.
# When it is ready, connect to an SSE endpoint.
async def connect(url, callable, headers, bot, apiEvent):
    # Loop until apiEvent is ready.
    while (apiEvent.ready == False):
        await asyncio.sleep(0.1)

    # Run forever
    while (True):
        # Start httpx http2 client.
        async with httpx.AsyncClient(http2=True, timeout=None) as client:
            # Try-Except for error handling.
            try:
                # Open a streaming GET request (server pushes SSE events to us)
                # "headers" contains the Authorization token. 
                async with client.stream("GET", url, headers=headers) as response:
                    # Handle errors differently, that way we can see errors better.
                    if response.is_error:
                        body = await response.aread()

                        print(f"[API] Error {response.status_code}: {body.decode()}")
                        await asyncio.sleep(1);
                        continue

                    response.raise_for_status()

                    event_name = None
                    data_lines = []
                    body = ""

                    async for line in response.aiter_lines():
                        body += line + "\n"
                        if line == "":
                            # Empty line terminates SSE event
                            if data_lines:
                                event = Event(name=event_name, data="\n".join(data_lines))
                                await callable(event, bot, apiEvent)

                            event_name = None
                            data_lines = []
                            continue

                        field, separator, value = line.partition(":")

                        if not separator:
                            continue

                        # Handle the space after :
                        if value.startswith(" "):
                            value = value[1:]

                        if field == "event":
                            event_name = value

                        elif field == "data":
                            data_lines.append(value)
            except httpx.ConnectError:
                print("[API] Could not connect to server.")
            except httpx.TimeoutException:
                print("[API] Connection/request timed out to server.")
            except Exception as e:
                print(f"[API] An unexpected error occurred: {e}")
        print("[API] Disconnected, reconnecting in 3 seconds.")
        await asyncio.sleep(3);

# Module entry point, starts a thread if API module is enabled.
async def instructor(bot, commands, apiEvent, **kwargs):
    if kwargs["api_enabled"].lower() == "true":
        # Start the SSE listener in a daemon thread, to avoid blocking the main bot loop.
        thread = threading.Thread(target=asyncio.run, args=(connect(
            url=kwargs["api_url"] + "/event/listen",
            callable=listener,
            headers={
                "Authorization": "Bearer " + kwargs["api_token"],
            },
            bot=bot,
            apiEvent=apiEvent
        ),))
        thread.daemon = True
        thread.start()
    else:
        print("API module is disabled.")