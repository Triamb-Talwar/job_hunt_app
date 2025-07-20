#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from job_app.crew import JobApp

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        "fields": "AI Engineer, Full Stack Developer, LLM Researcher",
        "location": "India",
        "recency_days": 7,
        "name": "Triamb Talwar"
    }

    result = JobApp().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL DECISION ===\n\n")
    print(result.raw)

if __name__ == "__main__":
    run()