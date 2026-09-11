import random
import pandas as pd

records = []

for i in range(1000):

    visited_resources = random.randint(0,30)
    announcements_view = random.randint(0,10)
    discussion_count = random.randint(0,10)
    raised_hands = random.randint(0,30)
    login_count = random.randint(0,40)

    total = (
        visited_resources +
        announcements_view*2 +
        discussion_count*2 +
        raised_hands +
        login_count
    )

    if total >= 70:
        performance = "Excellent"

    elif total >= 50:
        performance = "Good"

    elif total >= 30:
        performance = "Average"

    else:
        performance = "At Risk"

    records.append([

        visited_resources,
        announcements_view,
        discussion_count,
        raised_hands,
        login_count,
        performance

    ])

df = pd.DataFrame(records, columns=[

    "visited_resources",
    "announcements_view",
    "discussion_count",
    "raised_hands",
    "login_count",
    "Class"

])

df.to_csv("lms_dataset.csv", index=False)

print("Dataset Generated Successfully")
print(df.head())