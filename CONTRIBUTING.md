# Contributing to HEIC Dynamic Wallpaper Extractor

Thank you for considering contributing to HEIC Dynamic Wallpaper Extractor! We welcome all contributions, including bug reports, feature requests, documentation improvements, and code contributions.

## How to Contribute

### Reporting Issues
- Check the [issue tracker](https://github.com/FalloutGhoulBusta/HeicMagic/issues) to see if the issue has already been reported
- Provide a clear title and description of the issue
- Include steps to reproduce the issue
- Specify your operating system and Python version
- If possible, include screenshots or error messages

### Feature Requests
- Explain the feature you'd like to see
- Describe why this feature would be useful
- If possible, provide examples of how it might work

### Code Contributions
1. Fork the repository
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```
3. Make your changes
4. Write or update tests if applicable
5. Run the tests to ensure everything works
6. Commit your changes with a clear message
7. Push to your fork and submit a pull request

### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use docstrings for functions and classes following [PEP 257](https://www.python.org/dev/peps/pep-0257/)
- Keep lines under 100 characters when possible
- Include type hints for better code documentation

### Testing
- Run the existing tests before submitting changes
- Add tests for new features or bug fixes
- Ensure all tests pass before submitting a pull request

### Pull Request Process
1. Ensure any install or build dependencies are removed before the end of the layer when doing a build
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters
3. Update the CHANGELOG.md with details of your changes
4. The project maintainers will review your pull request and may request changes

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make your changes and test them

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Questions?

If you have any questions about contributing, please open an issue or contact the maintainers.
