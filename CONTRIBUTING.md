# Contributing to Notes API

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/notes-api.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### Making Changes

1. Write your code following the existing style
2. Add tests for new functionality
3. Run tests to ensure nothing breaks: `pytest`
4. Run linting: `flake8 app tests`
5. Format code: `black app tests`

### Testing

- All new features must have tests
- Maintain or improve code coverage
- Run the full test suite before submitting: `pytest --cov=app`

### Database Migrations

- Create migrations for schema changes: `alembic revision --autogenerate -m "description"`
- Test migrations locally: `alembic upgrade head` and `alembic downgrade -1`

### Commit Messages

Use clear, descriptive commit messages:

```
[type] Brief description

Longer explanation if needed.

Fixes #issue-number (if applicable)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Maintenance

Example:
```
feat: Add note status filter endpoint

- Implement filtering by status for list endpoint
- Add status query parameter validation
- Update tests for new filtering functionality

Fixes #42
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass: `pytest`
4. Update the README if necessary
5. Submit the PR with a clear description

### PR Description Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #issue-number

## Testing
- [ ] Added tests
- [ ] All tests pass
- [ ] Coverage maintained

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- Line length: 100 characters
- Use type hints where possible
- Use docstrings for functions and classes
- Use meaningful variable names

### Example:

```python
def get_notes_by_status(
    user_id: int,
    status: NoteStatus,
    db: Session,
) -> List[Note]:
    """
    Fetch notes for a user filtered by status.
    
    Args:
        user_id: ID of the user
        status: Status to filter by
        db: Database session
        
    Returns:
        List of notes matching the criteria
    """
    return db.query(Note).filter(
        (Note.user_id == user_id) &
        (Note.status == status)
    ).all()
```

## Project Structure

Respect the existing project structure:

```
app/
├── routes/           # API endpoints
├── models.py        # Database models
├── schemas.py       # Pydantic schemas
├── auth.py          # Authentication
└── database.py      # Database setup
tests/
├── test_users.py    # User tests
└── test_notes.py    # Notes tests
```

## Common Tasks

### Add a New Endpoint

1. Add route in `app/routes/`
2. Add request/response schema in `app/schemas.py`
3. Add tests in `tests/test_*.py`
4. Update README with new endpoint

### Add a Database Field

1. Update model in `app/models.py`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Update schemas if needed
4. Add tests
5. Update documentation

### Fix a Bug

1. Create a test that reproduces the bug
2. Fix the bug
3. Ensure test passes
4. Add regression test if needed

## Testing Guidelines

### Test Structure

```python
class TestFeatureName:
    """Tests for feature name."""
    
    def test_success_case(self, client, test_user_token):
        """Test successful operation."""
        # Setup
        # Action
        # Assert
        pass
    
    def test_error_case(self, client):
        """Test error handling."""
        pass
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_users.py

# Specific test
pytest tests/test_users.py::TestUserRegistration::test_register_success

# With coverage
pytest --cov=app

# Watch mode
pytest-watch
```

## Documentation

Update documentation for:
- New endpoints
- New configuration options
- Breaking changes
- Important setup steps

Document in:
- README.md for general usage
- Code docstrings for implementation
- PR description for changes

## Performance Considerations

When making changes, consider:

- Database query efficiency
- API response times
- Memory usage
- Caching opportunities
- Index needs

## Security Considerations

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all inputs
- Use parameterized queries
- Sanitize error messages
- Review OWASP Top 10

## Questions?

- Open an issue for discussion
- Ask in PRs
- Check existing documentation

Thank you for contributing! 🎉
