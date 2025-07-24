from collections import Counter
import statistics
import psycopg2
import random

all_colors = []
# === PART 1: COLORS ANALYSIS ===
colors_data = {
    'MONDAY':   'GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN',
    'TUESDAY':  'ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE',
    'WEDNESDAY':'GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE',
    'THURSDAY': 'BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN',
    'FRIDAY':   'GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE'
}


for day in colors_data:
    all_colors += [color.strip().upper() for color in colors_data[day].split(',')]

color_freq = Counter(all_colors)
sorted_by_freq = sorted(color_freq.items(), key=lambda x: x[1])
total_entries = sum(color_freq.values())


mean_index = total_entries // 2
cumulative = 0

for color, count in sorted_by_freq:
    cumulative += count
    if cumulative >= mean_index:
        mean_color = color
        break

print("1. Mean color:", mean_color)

most_common_color = color_freq.most_common(1)[0][0]
print('2. Most worn color:', most_common_color)

all_colors_sorted = sorted(all_colors)
median_color = all_colors_sorted[len(all_colors_sorted)//2]
print("3. Median color:", median_color)

frequencies = list(color_freq.values())
variance = statistics.variance(frequencies)
print('4. Variance of color frequencies:', variance)

red_count = color_freq.get('RED', 0)
prob_red = red_count / len(all_colors)
print('5. Probability color is RED:', round(prob_red, 4))


conn = psycopg2.connect(
    dbname='bincom_db',
    user='jay',
    password='bincomjay',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS color_frequency (
        id SERIAL PRIMARY KEY,
        color VARCHAR(20),
        frequency INTEGER
    )
''')

for color, freq in color_freq.items():
    cur.execute("INSERT INTO color_frequency (color, frequency) VALUES (%s, %s)", (color, freq))

conn.commit()
cur.close()
conn.close()
print("6. Saved to PostgreSQL successfully.")


def recursive_search(lst, target, index=0):
    if index >= len(lst):
        return -1
    if lst[index] == target:
        return index
    return recursive_search(lst, target, index + 1)

numbers = [5, 9, 3, 1, 8, 7]
target = 8
found_index = recursive_search(numbers, target)
print(f"7. Recursive search: Found {target} at index {found_index}" if found_index != -1 else "Not found")


binary_digits = ''.join(random.choice(['0', '1']) for _ in range(4))
decimal_value = int(binary_digits, 2)
print("8. Binary:", binary_digits, "→ Decimal:", decimal_value)

def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fib_sum = fibonacci_sum(50)
print("9. Sum of first 50 Fibonacci numbers:", fib_sum)
