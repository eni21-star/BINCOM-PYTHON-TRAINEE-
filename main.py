import random
from collections import Counter
import statistics
import psycopg2
from bs4 import BeautifulSoup
import requests

# Task 1
def extract_colors_from_html():
    url = "https://drive.google.com/uc?id=1nf9WMDjZWIUnlnKyz7qomEYDdtWfW1Uf"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find_all("tr")[1:]

    colors = []
    for row in rows:
        day_colors = row.find_all("td")[1].text.split(", ")
        colors.extend([color.strip().upper() for color in day_colors])
    return colors

# Task 2
def calculate_statistics(colors):
    if not colors:
        raise ValueError("The colors list is empty. Ensure data extraction is working correctly.")

    color_counts = Counter(colors)
    total_colors = sum(color_counts.values())

    
    sorted_counts = sorted(color_counts.items(), key=lambda x: x[1])
    mean_color = sorted_counts[len(sorted_counts) // 2][0]

   
    mode_color = color_counts.most_common(1)[0][0]

    
    median_color = sorted_counts[len(sorted_counts) // 2][0]

    
    frequencies = list(color_counts.values())
    variance = statistics.variance(frequencies) if len(frequencies) > 1 else 0

   
    probability_red = color_counts.get("RED", 0) / total_colors

    return mean_color, mode_color, median_color, variance, probability_red

# Task 3: Store in PostgreSQL
def store_in_database(color_counts):
    try:
        connection = psycopg2.connect(
            database="colors_db",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS colors (color TEXT, frequency INT)")

        for color, count in color_counts.items():
            cursor.execute("INSERT INTO colors (color, frequency) VALUES (%s, %s)", (color, count))

        connection.commit()
        print("Data stored successfully!")
    except Exception as e:
        print("Database Error:", e)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Task 4
def recursive_search(arr, target, index=0):
    if index >= len(arr):
        return -1
    if arr[index] == target:
        return index
    return recursive_search(arr, target, index + 1)

# Task 5
def random_binary_to_decimal():
    binary_number = ''.join(str(random.randint(0, 1)) for _ in range(4))
    decimal_number = int(binary_number, 2)
    return binary_number, decimal_number

# Task 6
def sum_fibonacci(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

# Task 7
def analyze_binary_sequence(sequence):
    output = ''.join('1' if sequence[i:i+3] == '111' else '0' for i in range(len(sequence) - 2))
    return output

# Main Function 
def main():
    colors = extract_colors_from_html()

    # Calculate statistics
    mean_color, mode_color, median_color, variance, probability_red = calculate_statistics(colors)
    print("Mean Color:", mean_color)
    print("Mode Color:", mode_color)
    print("Median Color:", median_color)
    print("Variance:", variance)
    print("Probability of Red:", probability_red)

    # Store in database
    color_counts = Counter(colors)
    store_in_database(color_counts)

    # Recursive search
    arr = [1, 2, 3, 4, 5]
    print("Index of 3 in list:", recursive_search(arr, 3))

    # Random binary to decimal
    binary, decimal = random_binary_to_decimal()
    print("Random Binary:", binary)
    print("Converted to Decimal:", decimal)

    # Sum of Fibonacci
    print("Sum of first 50 Fibonacci numbers:", sum_fibonacci(50))

    # Binary sequence analysis
    sequence = "0101101011101011011101101000111"
    print("Binary Sequence Output:", analyze_binary_sequence(sequence))

if __name__ == "__main__":
    main()
