# SandBoxExecEngine

A secure sandbox environment for executing code in multiple programming languages using Docker containers.

## Features

- Supports multiple programming languages:
  - Python
  - C
  - JavaScript (Node.js)
  - Bash
  - PowerShell
- Secure execution in isolated containers
- Resource limits and security controls
- RESTful API interface using FastAPI
- Automatic cleanup of temporary files
- Network disabled by default for security

## Prerequisites

- Docker
- Docker Compose
- Git (for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd SandBoxExecEngine
```

2. Build and start the services:
```bash
docker-compose up --build
```

The API server will be available at `http://localhost:8000`

## API Usage

The API accepts POST requests to `/run` endpoint with the following JSON structure:

```json
{
    "lang": "python",
    "code": "print('Hello, World!')"
}
```

Supported values for `lang`:
- `python` - Python 3.10
- `c` - GCC latest
- `javascript` - Node.js 16
- `bash` - Bash on Debian
- `pwsh` - PowerShell

### Example Requests

#### Python
```bash
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{"lang": "python", "code": "print(\"Hello, World!\")"}'
```

#### C
```bash
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{"lang": "c", "code": "#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}"}'
```

#### JavaScript
```bash
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{"lang": "javascript", "code": "console.log(\"Hello, World!\")"}'
```

## Security Features

- Containers run with no network access
- Memory limited to 256MB (Python runtime)
- CPU limited to 0.5 cores (Python runtime)
- No privileged access
- Automatic container removal after execution
- Isolated workspace for each execution

## Architecture

The project consists of:
- Main API service (FastAPI)
- Language-specific runtime containers
- Docker Compose orchestration
- Volume mounting for code execution

## Error Handling

The API returns:
- 400 for unsupported languages
- 500 for container execution errors
- JSON response with output or error details

## Development

To add a new language runtime:
1. Create a new directory under `runtimes/`
2. Add a Dockerfile for the runtime
3. Add the service to `docker-compose.yml`
4. Update `sandbox_server.py` with language support

## License

[Your License Here]
