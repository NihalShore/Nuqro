#!/usr/bin/env python3
"""
Report generation for NUQRO – displays and exports test results.

Functions:
- print_full_report(name, age, results): Show coloured report with ASCII charts.
- export_report(name, age, results, format='txt' or 'json'): Save report to file.
"""

import json
from datetime import datetime
from pathlib import Path

# Colour codes (mirror main.py)
class Color:
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

def ascii_bar(value, max_value=100, width=30):
    """Return a string like '██████░░░░ 60/100'"""
    if max_value <= 0:
        return "░" * width + " 0/100"
    filled = int(round((value / max_value) * width))
    filled = min(filled, width)
    bar = "█" * filled + "░" * (width - filled)
    return f"{bar} {value}/{max_value}"

def get_coaching(test_type, sub_scores):
    """Return a short actionable tip for the lowest sub‑score."""
    if not sub_scores:
        return "Keep practising! Every test helps you grow."
    
    # Find lowest scoring dimension
    try:
        lowest_dim = min(sub_scores.items(), key=lambda x: x[1])[0]
    except ValueError:
        return "Keep building your skills – every step counts."
    
    tips = {
        # EQ dimensions
        "self_awareness": "Journal your emotions daily to recognise patterns.",
        "self_management": "Try the 5‑second rule before reacting to strong feelings.",
        "social_awareness": "Practice active listening – repeat back what you hear.",
        "relationship_management": "Ask one open‑ended question in every conversation.",
        # SQ factors
        "social_acting": "Role‑play different social scenarios with a friend.",
        "social_cognising": "Read fiction – it builds theory of mind.",
        "social_relating": "Schedule regular check‑ins with people you care about.",
        # AQ CORE dimensions
        "Control": "Focus on what you *can* influence, even if small.",
        "Ownership": "When something goes wrong, ask: 'What can I do next?'",
        "Reach": "Contain setbacks – keep them in one area of your life.",
        "Endurance": "Remind yourself: 'This too shall pass.'",
    }
    return tips.get(lowest_dim, "Focus on your lowest score – small steps lead to big changes.")

def print_full_report(name, age, results):
    """
    Display a beautiful, coloured report in the terminal.
    results: dict like {'IQ': {'adjusted_score': 110, 'raw_score': 8, 'sub_scores': {...}}, ...}
    """
    print("\n" + Color.BOLD + Color.CYAN + "=" * 60 + Color.RESET)
    print(Color.BOLD + f"  📊 NUQRO REPORT for {name} (Age {age})".center(60) + Color.RESET)
    print(Color.CYAN + "=" * 60 + Color.RESET + "\n")

    for test, data in results.items():
        adj = data.get('adjusted_score', 0)
        raw = data.get('raw_score', None)
        sub = data.get('sub_scores', {})
        
        print(Color.BOLD + f"  {test} TEST".ljust(20) + Color.RESET + f"Score: {adj}")
        print(f"  {ascii_bar(adj)}")
        
        if raw is not None:
            print(f"  {Color.DIM}Raw: {raw}{Color.RESET}")
        
        if sub:
            print(f"  {Color.YELLOW}Breakdown:{Color.RESET}")
            for dim, score in sub.items():
                display_name = dim.replace('_', ' ').title()
                print(f"    {display_name:<20} {ascii_bar(score, width=20)}")
        
        # Coaching tip only for non‑IQ tests that have sub‑scores
        if sub and test != "IQ":
            tip = get_coaching(test, sub)
            print(f"  {Color.GREEN}💡 Tip:{Color.RESET} {tip}")
        
        print()  # blank line between tests
    
    print(Color.DIM + "  Thank you for using NUQRO! These results are saved locally." + Color.RESET)
    print()

def export_report(name, age, results, format='txt'):
    """
    Export report to a file (txt or json) inside 'reports/' folder.
    Returns the filename created.
    """
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    
    if format == 'json':
        filename = reports_dir / f"NUQRO_{safe_name}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "name": name,
                "age": age,
                "date": timestamp,
                "results": results
            }, f, indent=2)
        print(f"  {Color.GREEN}✓ JSON report saved: {filename}{Color.RESET}")
        return str(filename)
    
    else:  # txt format
        filename = reports_dir / f"NUQRO_{safe_name}_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"NUQRO REPORT for {name} (Age {age})\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for test, data in results.items():
                adj = data.get('adjusted_score', 0)
                raw = data.get('raw_score', 0)
                sub = data.get('sub_scores', {})
                
                f.write(f"{test} TEST – Score: {adj}\n")
                # Simple text bar (50 chars wide)
                bar_len = int(adj / 2)  # max 50
                bar_len = min(bar_len, 50)
                f.write(f"[{'#' * bar_len}{'.' * (50 - bar_len)}] {adj}/100\n")
                if raw:
                    f.write(f"Raw score: {raw}\n")
                if sub:
                    f.write("Breakdown:\n")
                    for dim, score in sub.items():
                        f.write(f"  {dim.replace('_', ' ').title()}: {score}\n")
                if sub and test != "IQ":
                    tip = get_coaching(test, sub)
                    f.write(f"Tip: {tip}\n")
                f.write("\n")
            
            f.write("Thank you for using NUQRO!\n")
        
        print(f"  {Color.GREEN}✓ Text report saved: {filename}{Color.RESET}")
        return str(filename)