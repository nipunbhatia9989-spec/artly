"""
Generate flashcard and question content for levels using Wikipedia + Claude.

Usage:
    # Generate a single level
    python -m content.generate --level 6

    # Generate all levels that have no content yet
    python -m content.generate --all

    # Regenerate specific levels (overwrites existing)
    python -m content.generate --level 6 --force
"""

import argparse
import json
import sys
import time

import anthropic
import requests

# Run from project root: python -m content.generate
sys.path.insert(0, ".")


WIKIPEDIA_API = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
HEADERS = {"User-Agent": "ArtDuolingo/1.0 (educational app)"}

PROMPT_TEMPLATE = """You are creating content for an art education app aimed at beginners.

Topic: {title} (Level {level_id} of 50, Difficulty {difficulty}/5)
Description: {description}

Wikipedia summary:
{extract}

Generate 6 flashcards and 8 questions about this topic for someone who knows nothing about art.
Use language that is clear, engaging, and jargon-free.

Return ONLY valid JSON — no markdown, no explanation:
{{
  "flashcards": [
    {{"front": "Short term or concept (1-5 words)", "back": "Clear explanation in 2-3 sentences."}}
  ],
  "questions": [
    {{
      "type": "mcq",
      "stem": "Question text?",
      "options": ["A. option", "B. option", "C. option", "D. option"],
      "answer": "A",
      "explanation": "One sentence explaining why."
    }}
  ]
}}

Mix these question types across the 8 questions:
- "mcq": 4 options (A/B/C/D), answer is the letter
- "single": 2 options (A/B), answer is the letter
- "yesno": options are ["Yes", "No"], answer is "Yes" or "No"
- "fill": options is null, answer is a 1-3 word phrase; use ___ in the stem

Calibrate difficulty to level {difficulty}/5. Level 1 is very basic; level 5 is nuanced.
"""


def fetch_wikipedia(article_title: str) -> str:
    url = WIKIPEDIA_API.format(article_title.replace(" ", "_"))
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.ok:
            return r.json().get("extract", "")
    except requests.RequestException:
        pass
    return ""


def generate_for_level(level, force: bool = False) -> bool:
    from extensions import db
    from models import Flashcard, Question

    existing_flashcards = Flashcard.query.filter_by(level_id=level.id).count()
    if existing_flashcards > 0 and not force:
        print(f"  Level {level.id} already has content — skipping (use --force to overwrite)")
        return False

    print(f"  Fetching Wikipedia: {level.wikipedia_article} ...", end=" ", flush=True)
    extract = fetch_wikipedia(level.wikipedia_article)
    if not extract:
        print("FAILED (no Wikipedia content)")
        return False
    print(f"OK ({len(extract)} chars)")

    client = anthropic.Anthropic()
    prompt = PROMPT_TEMPLATE.format(
        title=level.title,
        level_id=level.id,
        difficulty=level.difficulty,
        description=level.description,
        extract=extract[:3000],
    )

    print(f"  Generating content with Claude ...", end=" ", flush=True)
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()

    # Strip markdown code fences if present
    if "```" in raw:
        parts = raw.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                raw = part
                break

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"FAILED (JSON parse error: {e})")
        return False

    # Clear existing content if force
    if force:
        Flashcard.query.filter_by(level_id=level.id).delete()
        Question.query.filter_by(level_id=level.id).delete()

    for i, fc in enumerate(data.get("flashcards", [])):
        db.session.add(Flashcard(
            level_id=level.id,
            front=fc["front"],
            back=fc["back"],
            order=i,
        ))

    for i, q in enumerate(data.get("questions", [])):
        db.session.add(Question(
            level_id=level.id,
            type=q["type"],
            stem=q["stem"],
            options=q.get("options"),
            answer=q["answer"],
            explanation=q.get("explanation", ""),
            order=i,
        ))

    db.session.commit()
    fc_count = len(data.get("flashcards", []))
    q_count = len(data.get("questions", []))
    print(f"OK ({fc_count} flashcards, {q_count} questions)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate art lesson content")
    parser.add_argument("--level", type=int, help="Generate a specific level")
    parser.add_argument("--all", action="store_true", help="Generate all levels without content")
    parser.add_argument("--force", action="store_true", help="Overwrite existing content")
    args = parser.parse_args()

    from app import create_app
    app = create_app()

    with app.app_context():
        from models import Level

        if args.level:
            level = Level.query.get(args.level)
            if not level:
                print(f"Level {args.level} not found")
                sys.exit(1)
            print(f"Generating level {level.id}: {level.title}")
            generate_for_level(level, force=args.force)

        elif args.all:
            levels = Level.query.order_by(Level.id).all()
            print(f"Generating content for {len(levels)} levels...")
            for level in levels:
                print(f"\nLevel {level.id}: {level.title}")
                generate_for_level(level, force=args.force)
                time.sleep(1)  # polite rate limiting
            print("\nDone.")

        else:
            parser.print_help()


if __name__ == "__main__":
    main()
