# Contributing

Thank you for your interest in contributing to the Amazon Scraper project!

## How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test your changes**
5. **Submit a pull request**

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use descriptive variable names
- Keep configuration at the top of scripts
- Use f-strings for string formatting
- Include error handling with try/except

### Node.js
- Use `const` for constants, `let` for variables
- Use async/await for asynchronous operations
- Use camelCase for variable names
- Include error handling with try/catch

### General
- Keep scripts self-contained and runnable
- Include clear configuration sections
- Output data to the `output/` folder
- Use consistent naming conventions across languages

## Adding a New Scraper

1. Create the Python version in `python/`
2. Create the Node.js version in `node.js/`
3. Update the README with the new scraper
4. Add sample output to `output/`

## Reporting Issues

When reporting issues, please include:
- Which script you're running
- The error message
- Your Python/Node.js version
- Any relevant configuration

## Questions?

Open an issue or reach out via the repository discussions.
