"""Seed the database: create all 50 levels and load pre-built content for levels 1–5."""

import sys

sys.path.insert(0, ".")


def seed(app):
    from content.curriculum import LEVELS
    from content.seed_data import SEED
    from extensions import db
    from models import Flashcard, Level, Question

    with app.app_context():
        db.create_all()

        for (level_id, title, description, difficulty, wikipedia_article) in LEVELS:
            existing = Level.query.get(level_id)
            if not existing:
                xp = 10 + (difficulty - 1) * 5  # 10–30 XP based on difficulty
                db.session.add(Level(
                    id=level_id,
                    title=title,
                    description=description,
                    difficulty=difficulty,
                    wikipedia_article=wikipedia_article,
                    xp_reward=xp,
                ))
        db.session.commit()
        print(f"✓ {len(LEVELS)} levels created")

        seeded = 0
        for level_id, content in SEED.items():
            existing = Flashcard.query.filter_by(level_id=level_id).first()
            if existing:
                continue

            for i, card in enumerate(content["flashcards"]):
                front, back = card[0], card[1]
                image_url = card[2] if len(card) > 2 else None
                image_caption = card[3] if len(card) > 3 else None
                db.session.add(Flashcard(level_id=level_id, front=front, back=back, image_url=image_url, image_caption=image_caption, order=i))

            for i, q in enumerate(content["questions"]):
                db.session.add(Question(
                    level_id=level_id,
                    type=q["type"],
                    stem=q["stem"],
                    options=q["options"],
                    answer=q["answer"],
                    explanation=q["explanation"],
                    order=i,
                ))
            seeded += 1

        db.session.commit()
        print(f"✓ Pre-built content loaded for {seeded} levels (1–5)")
        print("  Run `python -m content.generate --all` to generate levels 6–50 via Wikipedia + Claude")


if __name__ == "__main__":
    from app import create_app
    seed(create_app())
