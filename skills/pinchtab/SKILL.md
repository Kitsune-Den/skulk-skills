# Pinchtab Skill 🦀

This skill provides efficient, HTTP-based browser control for AI agents using Pinchtab. It's designed for faster, cheaper, and more robust web automation, leveraging accessibility trees for precise interaction and token efficiency.

## Functions:

### `start_server(port=9867, token=None, headless=True)`

Starts the Pinchtab HTTP server in the background. If a server is already running, it will attempt to connect to it.

**Parameters:**
- `port` (integer, optional): The port Pinchtab should listen on. Defaults to 9867.
- `token` (string, optional): An authentication token for the Pinchtab API. If not provided, it will attempt to retrieve `PINCHTAB_API_TOKEN` from secrets.db.
- `headless` (boolean, optional): If `True`, Chrome runs in headless mode (no visible window). Defaults to `True`.

**Returns:**
A string indicating the Pinchtab server status and URL.

### `stop_server()`

Stops the running Pinchtab server process.

**Returns:**
A string indicating the server's shutdown status.

### `navigate(url, tab_id=None)`

Navigates the browser to the specified URL.

**Parameters:**
- `url` (string, required): The URL to navigate to.
- `tab_id` (string, optional): The ID of the tab to navigate. Defaults to the first tab.

**Returns:**
A string indicating successful navigation or an error.

### `get_snapshot(tab_id=None, filter='interactive', format='text', max_tokens=None, selector=None)`

Gets an accessibility tree snapshot of the current page. Optimized for token efficiency.

**Parameters:**
- `tab_id` (string, optional): The ID of the tab to snapshot. Defaults to the first tab.
- `filter` (string, optional): Filter for snapshot. `'interactive'` (buttons, links, inputs) or `'full'`. Defaults to `'interactive'`.
- `format` (string, optional): Output format. `'text'` (indented plain text), `'compact'` (one-line-per-node), or `'json'`. Defaults to `'text'`.
- `max_tokens` (integer, optional): Truncate output to ~N tokens.
- `selector` (string, optional): CSS selector to scope the tree to a subtree.

**Returns:**
A string containing the formatted page snapshot.

### `get_text(tab_id=None, mode='readability')`

Gets readable page text, either via readability extraction or raw `innerText`.

**Parameters:**
- `tab_id` (string, optional): The ID of the tab. Defaults to the first tab.
- `mode` (string, optional): Extraction mode. `'readability'` (strips nav/ads) or `'raw'` (`innerText`). Defaults to `'readability'`.

**Returns:**
A string containing the extracted page text.

### `click_element(ref, tab_id=None)`

Clicks an element on the page using its accessibility tree reference (e.g., `'e5'`).

**Parameters:**
- `ref` (string, required): The accessibility tree reference of the element to click.
- `tab_id` (string, optional): The ID of the tab. Defaults to the first tab.

**Returns:**
A string indicating success or failure.

### `type_text(ref, text, tab_id=None)`

Types text into an input field identified by its accessibility tree reference.

**Parameters:**
- `ref` (string, required): The accessibility tree reference of the input element.
- `text` (string, required): The text to type.
- `tab_id` (string, optional): The ID of the tab. Defaults to the first tab.

**Returns:**
A string indicating success or failure.
