# Nova AutoPilot - Demo Video Script

**Duration: ~3 minutes**

## Scene 1: Introduction (0:00-0:20)

**[Screen: Nova AutoPilot logo and title]**

"Nova AutoPilot is an autonomous web task agent built on Amazon Nova Act. It handles complex web-based tasks using simple natural language instructions."

"Let me show you what it can do."

## Scene 2: Basic Task Execution (0:20-0:50)

**[Screen: Terminal with CLI]**

```bash
python -m nova_autopilot "Go to Hacker News and extract the top 5 stories"
```

**[Show browser opening, navigating, extracting data]**

"With a single command, the agent navigates to Hacker News, identifies the story elements, and extracts structured data - all automatically."

**[Show JSON output with extracted stories]**

"The results are returned as clean, structured JSON ready for further processing."

## Scene 3: Price Monitoring Use Case (0:50-1:30)

**[Screen: Code editor showing price_monitor.py]**

"Real-world applications are where Nova AutoPilot shines. Here's a price monitor that tracks products across e-commerce sites."

```python
result = pilot.extract(
    "Find the current price of the main product",
    starting_url=product_url
)
```

**[Show browser checking multiple products]**

"It checks each product, compares against thresholds, and alerts when deals are found."

**[Show output with DEAL alerts]**

"This runs automatically - perfect for finding flash sales or tracking price drops."

## Scene 4: Form Automation (1:30-2:00)

**[Screen: Contact form on a website]**

"Nova AutoPilot handles form automation with chain commands."

```python
pilot.chain([
    f"Enter name: John Smith",
    f"Enter email: john@example.com",
    f"Enter message: Hello!",
    "Click Submit",
    "Confirm success"
])
```

**[Show browser filling form step by step]**

"Each step is verified before proceeding. If something fails, the agent can retry with alternative approaches."

## Scene 5: Architecture & Bedrock Integration (2:00-2:30)

**[Screen: Architecture diagram]**

"Under the hood, Nova AutoPilot combines:

- Amazon Nova Act for reliable browser automation
- Amazon Bedrock with Nova Pro for task planning
- Intelligent retry and error recovery
- Screenshot capture for debugging

The Nova Act SDK handles the complexity of browser interaction while Bedrock provides the reasoning layer for task decomposition."

## Scene 6: Enterprise Features (2:30-2:50)

**[Screen: Code snippets and output]**

"Enterprise-ready features include:

- Parallel session execution for scaling
- Audit logging for compliance
- Human-in-the-loop escalation
- Session persistence with authentication

All built on AWS infrastructure for production reliability."

## Scene 7: Conclusion (2:50-3:00)

**[Screen: GitHub repo and installation]**

"Nova AutoPilot - automating the web with natural language.

Try it yourself:
```
pip install nova-autopilot
```

Built with Amazon Nova Act for the Amazon Nova AI Hackathon 2026."

---

## Recording Notes

1. **Screen resolution**: 1920x1080
2. **Terminal**: Dark theme with good contrast
3. **Browser**: Chrome, standard window size
4. **Speed**: May need to 1.5x speed some browser interactions
5. **Audio**: Clear narration, no background music initially

## B-roll Suggestions

- Close-ups of JSON output
- Architecture diagram zooms
- Quick cuts between terminal and browser
- Fade transitions between scenes
