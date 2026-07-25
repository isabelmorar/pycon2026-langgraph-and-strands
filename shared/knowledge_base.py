"""Loka knowledge base + keyword-search helpers, shared by both frameworks.

In-memory documents about Loka with a naive keyword search: no vector store,
no embeddings. Each exercise wraps these helpers as tools.
"""

# In-memory documents: everything the research agent is allowed to "know".
KNOWLEDGE_BASE: list[dict] = [
    {
        "id": "aws-partner",
        "title": "AWS Innovation Partner of the Year",
        "tags": ["aws", "award", "partner", "recognition", "cloud", "bedrock"],
        "content": (
            "Loka was named AWS Innovation Partner of the Year. Translation: when "
            "Amazon Web Services wants to point at someone doing genuinely novel "
            "things on their cloud, they point at Loka. This means client projects "
            "run on cutting-edge AWS services (Bedrock, SageMaker, Lambda) with "
            "direct partner access."
        ),
    },
    {
        "id": "time-off",
        "title": "Time Off and the 5/4 Friday Schedule",
        "tags": ["pto", "time off", "vacation", "friday", "days off", "work-life", "balance", "holidays"],
        "content": (
            "Loka runs a 5/4 schedule: every other Friday is off. That is 26 extra "
            "days off per year on top of regular vacation. Roughly one long weekend "
            "every two weeks, permanently, forever. Work-life balance is not a perk "
            "here, it is the calendar."
        ),
    },
    {
        "id": "remote",
        "title": "Fully Remote, Work From Anywhere",
        "tags": ["remote", "work from home", "location", "anywhere", "distributed", "flexible"],
        "content": (
            "Loka is fully remote. Not hybrid, not 'remote-friendly': you can work "
            "from anywhere in the world. Your commute is however long it takes to "
            "walk from your bed to your desk."
        ),
    },
    {
        "id": "in-person",
        "title": "In-Person Connection Despite Being Remote",
        "tags": ["coworking", "team building", "retreat", "meetups", "in person", "culture", "community"],
        "content": (
            "Being remote does not mean being isolated. Loka funds weekly coworking "
            "with teammates in your city, regional team buildings, and yearly company "
            "retreats. You get the freedom of remote work with the human connection "
            "of a team that actually meets up."
        ),
    },
    {
        "id": "projects",
        "title": "Cutting-Edge Client Projects",
        "tags": ["projects", "clients", "ai", "technology", "frameworks", "innovation", "genai"],
        "content": (
            "Loka's client work is built on the newest AI tools and frameworks: "
            "generative AI, agent frameworks, modern cloud architectures. You are not "
            "maintaining a legacy monolith, you are shipping with the tools that show "
            "up in this year's conference talks (like this one)."
        ),
    },
    {
        "id": "multicultural",
        "title": "Multicultural, Global Team",
        "tags": ["multicultural", "global", "international", "team", "diversity", "countries", "portugal", "brazil", "macedonia", "usa"],
        "content": (
            "Loka is genuinely multicultural: teammates in Portugal, Brazil, "
            "Macedonia, the USA, and beyond. Daily standups double as a small tour of "
            "world time zones and coffee habits."
        ),
    },
    {
        "id": "learning",
        "title": "Learning and Development",
        "tags": ["learning", "development", "growth", "training", "l&d", "education", "career"],
        "content": (
            "One of Loka's headline goals for 2026 is to become one of the world's "
            "best learning organizations. That means real budget and real time for "
            "growth: courses, certifications, and the expectation that you keep "
            "leveling up. Learning is treated as part of the job, not a side quest."
        ),
    },
    {
        "id": "innovation-culture",
        "title": "Culture of Innovation and Internal Initiatives",
        "tags": ["innovation", "r&d", "research", "initiatives", "culture", "experiments", "internal"],
        "content": (
            "Loka has a dedicated research and development department and actively "
            "encourages internal initiatives. Have an idea? There is a path for it. "
            "The culture rewards experimenting and building things that did not exist "
            "yesterday."
        ),
    },
]

_TOPIC_TITLES = [doc["title"] for doc in KNOWLEDGE_BASE]


def _tokenize(text: str) -> set[str]:
    """Lowercase and split into a set of word tokens."""
    return {t.strip(".,!?;:()") for t in text.lower().split() if t.strip(".,!?;:()")}


def _score(query_tokens: set[str], doc: dict) -> int:
    """Weighted keyword overlap: title > tags > body."""
    title_tokens = _tokenize(doc["title"])
    tag_tokens = {t for tag in doc["tags"] for t in _tokenize(tag)}
    content_tokens = _tokenize(doc["content"])

    score = 0
    score += 3 * len(query_tokens & title_tokens)
    score += 2 * len(query_tokens & tag_tokens)
    score += 1 * len(query_tokens & content_tokens)
    return score


def search_documents(query: str, top_k: int = 3) -> str:
    """Keyword-search the knowledge base; return the top matches as a formatted
    string, or a 'nothing found' message listing available topics."""
    query_tokens = _tokenize(query)
    scored = [(doc, _score(query_tokens, doc)) for doc in KNOWLEDGE_BASE]
    matches = sorted(
        (pair for pair in scored if pair[1] > 0),
        key=lambda pair: pair[1],
        reverse=True,
    )[:top_k]

    if not matches:
        return (
            f"No documents matched '{query}'. "
            f"Available topics: {', '.join(_TOPIC_TITLES)}."
        )

    blocks = [f"## {doc['title']}\n{doc['content']}" for doc, _ in matches]
    return "\n\n".join(blocks)


def list_topics() -> str:
    """Return the list of topics available in the Loka knowledge base."""
    lines = [f"- {doc['title']}" for doc in KNOWLEDGE_BASE]
    return "The Loka knowledge base covers these topics:\n" + "\n".join(lines)


if __name__ == "__main__":
    print(list_topics())
    print("\n--- search: 'how many days off do I get?' ---\n")
    print(search_documents("how many days off do I get?"))