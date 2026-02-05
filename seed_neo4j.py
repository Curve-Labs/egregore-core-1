#!/usr/bin/env python3
"""Seed the test org Neo4j with initial schema and data."""

from neo4j import GraphDatabase

# Test org credentials
URI = "neo4j+s://668bb747.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "vGZaClcdYGeAzp0LbyVWPfuUgMW_QO-L6LGZQ45lBCY"

def seed():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    with driver.session() as session:
        # Create constraints
        print("Creating constraints...")
        session.run("CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE")
        session.run("CREATE CONSTRAINT project_name IF NOT EXISTS FOR (proj:Project) REQUIRE proj.name IS UNIQUE")
        session.run("CREATE CONSTRAINT quest_id IF NOT EXISTS FOR (q:Quest) REQUIRE q.id IS UNIQUE")

        # Create indexes
        print("Creating indexes...")
        session.run("CREATE INDEX session_date IF NOT EXISTS FOR (s:Session) ON (s.date)")
        session.run("CREATE INDEX artifact_created IF NOT EXISTS FOR (a:Artifact) ON (a.created)")

        # Create initial project
        print("Creating initial project...")
        session.run("""
            MERGE (p:Project {name: "egregore"})
            ON CREATE SET p.domain = "coordination",
                          p.description = "Egregore test environment"
            RETURN p
        """)

        # Verify
        result = session.run("MATCH (n) RETURN labels(n) AS label, count(*) AS count")
        print("\nDatabase contents:")
        for record in result:
            print(f"  {record['label']}: {record['count']}")

    driver.close()
    print("\nDone!")

if __name__ == "__main__":
    seed()
