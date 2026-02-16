#!/usr/bin/env python3
"""
Form Automation Example

Demonstrates automated form filling and submission
with validation and error handling.
"""

from nova_autopilot import AutoPilot


def submit_contact_form(
    url: str,
    name: str,
    email: str,
    message: str
) -> dict:
    """
    Fill and submit a contact form.

    Args:
        url: Form page URL
        name: Contact name
        email: Contact email
        message: Message content

    Returns:
        Submission result
    """
    pilot = AutoPilot(headless=True)

    # Chain of tasks for form submission
    tasks = [
        f"Find the name/full name input field and enter: {name}",
        f"Find the email input field and enter: {email}",
        f"Find the message/comments textarea and enter: {message}",
        "Find and click the submit button",
        "Wait for a success message or confirmation to appear"
    ]

    result = pilot.chain(tasks, starting_url=url, stop_on_failure=True)

    return {
        "success": result.all_succeeded,
        "tasks_completed": result.tasks_completed,
        "total_time": result.total_execution_time,
        "error": result.results[-1].error if not result.success else None
    }


def batch_form_submissions(
    url: str,
    submissions: list[dict]
) -> list[dict]:
    """
    Submit multiple forms in sequence.

    Args:
        url: Form page URL
        submissions: List of form data dicts

    Returns:
        List of results
    """
    results = []

    for i, data in enumerate(submissions):
        print(f"Submitting form {i + 1}/{len(submissions)}...")

        result = submit_contact_form(
            url=url,
            name=data.get("name", ""),
            email=data.get("email", ""),
            message=data.get("message", "")
        )

        results.append({
            "index": i,
            "data": data,
            **result
        })

        if result["success"]:
            print(f"  ✓ Success ({result['total_time']:.1f}s)")
        else:
            print(f"  ✗ Failed: {result['error']}")

    return results


def main():
    # Example: Single form submission
    url = "https://example.com/contact"

    print("Form Automation Example")
    print("=" * 40)

    result = submit_contact_form(
        url=url,
        name="John Smith",
        email="john@example.com",
        message="Hello! I'm interested in your services."
    )

    if result["success"]:
        print(f"\n✓ Form submitted successfully!")
        print(f"  Completed {result['tasks_completed']} steps")
        print(f"  Total time: {result['total_time']:.1f}s")
    else:
        print(f"\n✗ Form submission failed")
        print(f"  Error: {result['error']}")

    # Example: Batch submissions
    print("\n\nBatch Form Submission Example")
    print("=" * 40)

    test_submissions = [
        {"name": "Alice", "email": "alice@test.com", "message": "Test 1"},
        {"name": "Bob", "email": "bob@test.com", "message": "Test 2"},
    ]

    results = batch_form_submissions("https://example.com/contact", test_submissions)

    successful = sum(1 for r in results if r["success"])
    print(f"\n\nSummary: {successful}/{len(results)} forms submitted successfully")


if __name__ == "__main__":
    main()
