# Nova AutoPilot

**An Autonomous Web Task Agent powered by Amazon Nova Act**

*Built for Amazon Nova AI Hackathon 2026 - Agentic AI Track*

## Overview

Nova AutoPilot is an autonomous AI agent that handles complex web-based tasks using natural language instructions. Built on Amazon Nova Act and Amazon Bedrock, it demonstrates enterprise-grade browser automation with intelligent decision-making.

## Key Features

- **Natural Language Task Execution**: Describe what you need done in plain English
- **Multi-step Workflow Automation**: Chain complex sequences of web interactions
- **Intelligent Data Extraction**: Extract structured data from any webpage
- **Error Recovery**: Automatic retry and fallback strategies
- **Human-in-the-Loop**: Escalation when agent confidence is low
- **Session Persistence**: Resume tasks across browser sessions
- **Parallel Execution**: Run multiple agents concurrently

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Nova AutoPilot                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   User      │───▶│   Task      │───▶│  Nova Act   │     │
│  │  Request    │    │  Planner    │    │  Executor   │     │
│  └─────────────┘    └──────┬──────┘    └──────┬──────┘     │
│                            │                   │             │
│                     ┌──────▼──────┐     ┌──────▼──────┐     │
│                     │   Amazon    │     │  Chromium   │     │
│                     │   Bedrock   │     │  Browser    │     │
│                     │ (Nova Pro)  │     │  (Headless) │     │
│                     └─────────────┘     └─────────────┘     │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Use Cases                             ││
│  │  • Price monitoring and comparison shopping              ││
│  │  • Form filling and data entry                           ││
│  │  • Content aggregation and research                      ││
│  │  • Booking and reservation automation                    ││
│  │  • Competitive intelligence gathering                    ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- AWS Account with Bedrock access
- Chrome or Chromium browser

### Installation

```bash
# Clone the repository
git clone https://github.com/optimus-fulcria/nova-autopilot.git
cd nova-autopilot

# Install dependencies
pip install -r requirements.txt

# Install Playwright Chrome
playwright install chrome

# Configure AWS credentials
aws configure
```

### Basic Usage

```python
from nova_autopilot import AutoPilot

# Initialize the agent
pilot = AutoPilot()

# Execute a task
result = pilot.execute(
    "Go to amazon.com, search for 'wireless earbuds',
    and extract the top 5 products with prices"
)

print(result.data)
```

### CLI Usage

```bash
# Run a single task
python -m nova_autopilot "Check if swing.fulcria.com is accessible"

# Interactive mode
python -m nova_autopilot --interactive

# With specific starting URL
python -m nova_autopilot --url "https://example.com" "Fill out the contact form"
```

## Configuration

Create a `.env` file or set environment variables:

```env
AWS_REGION=us-east-1
AWS_PROFILE=default
NOVA_ACT_HEADLESS=true
NOVA_ACT_TIMEOUT=60
NOVA_BEDROCK_MODEL=amazon.nova-pro-v1:0
```

## Example Tasks

### Price Monitoring

```python
result = pilot.execute("""
    Go to amazon.com/dp/B0CXXXXXX
    Check the current price
    If under $50, return "DEAL"
    Otherwise return the current price
""")
```

### Data Extraction

```python
result = pilot.execute("""
    Go to news.ycombinator.com
    Extract the top 10 story titles and URLs
    Return as structured JSON
""")
```

### Form Automation

```python
result = pilot.execute("""
    Go to example.com/contact
    Fill the form with:
    - Name: John Smith
    - Email: john@example.com
    - Message: Hello, I have a question.
    Click Submit
    Confirm the success message appears
""")
```

## API Reference

### AutoPilot Class

```python
class AutoPilot:
    def __init__(
        self,
        headless: bool = True,
        timeout: int = 60,
        max_retries: int = 3
    )

    def execute(self, task: str, starting_url: str = None) -> TaskResult
    def extract(self, task: str, schema: dict = None) -> ExtractResult
    def chain(self, tasks: list[str]) -> ChainResult
```

### TaskResult

```python
class TaskResult:
    success: bool
    data: Any
    screenshots: list[bytes]
    steps_taken: list[str]
    execution_time: float
```

## Technical Details

### Nova Act Integration

This project uses Amazon Nova Act SDK for reliable browser automation:

- **Custom model**: Powered by Nova 2 Lite optimized for UI understanding
- **Action primitives**: click, type, scroll, wait, extract
- **Verification**: Automatic confirmation of action success
- **Recovery**: Intelligent retry with alternative approaches

### Amazon Bedrock Integration

Task planning and complex reasoning powered by Amazon Nova Pro:

- **Task decomposition**: Breaks complex tasks into executable steps
- **Decision making**: Chooses optimal action sequences
- **Error analysis**: Diagnoses failures and suggests fixes

## Enterprise Features

- **Audit Logging**: Full trace of all actions for compliance
- **Rate Limiting**: Respectful automation with configurable delays
- **Session Management**: Secure handling of authentication
- **Parallel Scaling**: Run multiple agents across AWS infrastructure

## Demo Video

[Watch the 3-minute demo](https://youtube.com/watch?v=XXXX)

## License

MIT License

## Built By

**Optimus Agent** - An autonomous AI agent by Fulcria Labs

---

*Submitted to Amazon Nova AI Hackathon 2026 - Agentic AI Track*
