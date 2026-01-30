import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_sql_safe_string(s):
    return s.replace("'", "''")

def generate_users(num_users=100):
    users = []
    print(f"Generating {num_users} users...")
    for _ in range(num_users):
        username = fake.unique.user_name()
        email = fake.unique.email()
        users.append(f"('{username}', '{email}')")
    return users

def generate_articles(num_articles=10000):
    articles = []
    categories = ['Technology', 'Health', 'Science', 'Business', 'Entertainment', 'Sports', 'Politics', 'Food', 'Travel']
    print(f"Generating {num_articles} articles...")
    
    for _ in range(num_articles):
        # Generate a realistic-looking title (remove trailing period if present)
        title = generate_sql_safe_string(fake.sentence(nb_words=6).rstrip('.'))
        
        # Generate some paragraph content
        content = generate_sql_safe_string(fake.text(max_nb_chars=500))
        
        category = random.choice(categories)
        articles.append(f"('{title}', '{content}', '{category}')")
    return articles

def generate_reading_history(num_users, num_articles, num_entries=20000):
    history = []
    print(f"Generating {num_entries} history entries...")
    for _ in range(num_entries):
        user_id = random.randint(1, num_users)
        article_id = random.randint(1, num_articles)
        # Random date within last 90 days
        fake_date = fake.date_time_between(start_date='-90d', end_date='now')
        read_at = fake_date.strftime('%Y-%m-%d %H:%M:%S')
        history.append(f"({user_id}, {article_id}, '{read_at}')")
    return history

def main():
    num_users = 100
    num_articles = 10000
    num_history = 20000

    users = generate_users(num_users)
    articles = generate_articles(num_articles)
    history = generate_reading_history(num_users, num_articles, num_history)

    print("Writing to seed.sql...")
    with open('seed.sql', 'w') as f:
        f.write("-- Seed data for users\n")
        f.write("INSERT INTO users (username, email) VALUES\n")
        f.write(",\n".join(users) + ";\n\n")

        f.write("-- Seed data for articles\n")
        # Write articles in chunks to avoid query length limits
        chunk_size = 1000
        for i in range(0, len(articles), chunk_size):
            chunk = articles[i:i + chunk_size]
            f.write("INSERT INTO articles (title, content, category) VALUES\n")
            f.write(",\n".join(chunk) + ";\n")
        f.write("\n")

        f.write("-- Seed data for reading_history\n")
        # Write history in chunks
        for i in range(0, len(history), chunk_size):
            chunk = history[i:i + chunk_size]
            f.write("INSERT INTO reading_history (user_id, article_id, read_at) VALUES\n")
            f.write(",\n".join(chunk) + ";\n")

    print(f"Successfully generated seed.sql with realistic data.")

if __name__ == "__main__":
    main()
