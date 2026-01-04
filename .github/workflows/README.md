# CI/CD Workflows

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### `ci.yml` - Continuous Integration
- **Triggers**: Push and pull requests to `main` and `develop` branches
- **Jobs**:
  - **Lint**: Code formatting (Black), linting (Flake8), type checking (mypy)
  - **Test**: Runs tests across Python 3.12 and 3.13
  - **Security**: Security scanning with Bandit and Safety
  - **Build**: Verifies the project builds successfully

### `cd.yml` - Continuous Deployment
- **Triggers**: Push to `main` branch or version tags (`v*`)
- **Jobs**:
  - **Deploy**: Builds and deploys the application
  - **Release**: Creates GitHub releases for version tags

### `docker.yml` - Docker Build and Push
- **Triggers**: Push to `main`, version tags, pull requests, or manual dispatch
- **Jobs**:
  - **Build**: Builds multi-architecture Docker images (amd64, arm64)
  - **Push**: Pushes to GitHub Container Registry (ghcr.io)

### `codeql.yml` - CodeQL Security Analysis
- **Triggers**: Push, pull requests, and weekly schedule
- **Jobs**:
  - **Analyze**: Performs static code analysis for Python and JavaScript
  - **Security**: Identifies security vulnerabilities

### `dependency-review.yml` - Dependency Review
- **Triggers**: Pull requests to `main` and `develop`
- **Jobs**:
  - **Dependency Review**: Reviews dependencies for security vulnerabilities

### `release.yml` - Release Automation
- **Triggers**: Version tags (`v*.*.*`)
- **Jobs**:
  - **Release**: Automatically creates GitHub releases with changelog

## Usage

### Running Workflows Locally

You can test workflows locally using [act](https://github.com/nektos/act):

```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run CI workflow
act push

# Run specific job
act -j lint
```

### Manual Workflow Dispatch

Some workflows support manual triggering:

```bash
gh workflow run docker.yml
```

### Version Tagging

To trigger a release:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Configuration

### Required Secrets

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- Additional secrets may be required for deployment (configure in repository settings)

### Environment Variables

Set in repository settings under Settings → Secrets and variables → Actions → Variables

## Status Badges

Add to your README.md:

```markdown
![CI](https://github.com/kmransom56/network-observability-platform/workflows/CI/badge.svg)
![Docker](https://github.com/kmransom56/network-observability-platform/workflows/Docker%20Build/badge.svg)
![CodeQL](https://github.com/kmransom56/network-observability-platform/workflows/CodeQL%20Analysis/badge.svg)
```
