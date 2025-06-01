# AI Music Co-Producer for REAPER DAW

An intelligent music production assistant that integrates with REAPER DAW, providing AI-powered tools for music creation and production. This project implements a MCP(Model Context Protocol) server that allows for automated control and manipulation of REAPER projects. Users can chat with any LLM that supports MCP protocol, and the AI agent will understand their musical intentions and make the necessary changes to their REAPER project in real-time - similar to having a virtual music producer that can understand and implement your creative vision through natural conversation.

## Features

- **AI-Powered Music Production**
  - Integrate with any LLM that supports MCP server protocol
  - Similar to Cursor for coding, but for music production

- **Project Management**
  - Get project state (BPM, length, tracks)
  - Set project BPM
  - Create and delete tracks
  - Add and delete MIDI items

- **MIDI Editing**
  - Add MIDI notes to active takes
  - Create new MIDI items
  - Manage MIDI items on tracks

- **VST Plugin Integration**
  - List available VST plugins
  - Add VST plugins to tracks
  - Get and set FX parameters
  - Manage FX chains on tracks

## Prerequisites

- REAPER DAW (64-bit version)
- Python 3.x
- Required Python packages (see Installation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Aavishkar-Kolte/reaper-daw-mcp-server
cd ai-music-coproducer
```

2. Install uv (if not already installed):
```bash
pip install uv
```

3. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

## Usage

1. Add the MCP server to your preferred LLM application that supports MCP protocol
2. Start REAPER DAW and open your project
3. Start the MCP server from your LLM application:

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.