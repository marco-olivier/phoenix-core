# Contributing to Phoenix Core

Thank you for your interest in contributing!

## Development Setup

```bash
# Clone repository
git clone https://github.com/marco-olivier/phoenix-core.git
cd phoenix-core

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

- Use Black for formatting
- Follow PEP 8
- Add type hints
- Write docstrings

## Pull Request Process

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit PR with description

## Areas for Contribution

- Backend implementations (OpenCL, Vulkan)
- Additional optimization passes
- More kernel examples
- Documentation improvements
- Performance benchmarks
