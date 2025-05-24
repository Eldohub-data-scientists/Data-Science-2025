
import string

def analyze_text(s: str) -> dict:
    """
    Analyzes a string for character types and word statistics.

    Args:
        s (str): The input string.

    Returns:
        dict: A dictionary with counts and analysis results.
    """
    vowels = "aeiouAEIOU"
    punctuation_chars = string.punctuation

    total_chars = len(s)
    vowel_count = 0
    consonant_count = 0
    digit_count = 0
    punctuation_count = 0

    # Index-based loop
    for i in range(len(s)):
        ch = s[i]
        if ch in vowels:
            vowel_count += 1
        elif ch.isalpha():
            consonant_count += 1
        elif ch.isdigit():
            digit_count += 1
        elif ch in punctuation_chars:
            punctuation_count += 1

    substring = input("Enter a substring to search for: ")
    first_index = s.find(substring)
    last_index = s.rfind(substring)

    # Direct character-based loop to gather words
    word_buffer = ""
    word_list = []
    for ch in s:
        if ch.isalnum() or ch == "'":
            word_buffer += ch.lower()
        elif word_buffer:
            word_list.append(word_buffer)
            word_buffer = ""
    if word_buffer:
        word_list.append(word_buffer)

    unique_words = sorted(set(word_list))

    return {
        "total_characters": total_chars,
        "vowels": vowel_count,
        "consonants": consonant_count,
        "digits": digit_count,
        "punctuation": punctuation_count,
        "first_index": first_index,
        "last_index": last_index,
        "unique_words": unique_words
    }


def stats_numbers(nums: list[int]) -> dict:
    """
    Calculates statistics from a list of integers.

    Args:
        nums (list[int]): List of integers.

    Returns:
        dict: A dictionary with sum, average, min, max, and divisible flags.
    """
    if not nums:
        return {}

    total = 0
    min_num = max_num = nums[0]
    divisible_by_3_or_5 = []

    for n in nums:
        total += n
        if n < min_num:
            min_num = n
        if n > max_num:
            max_num = n
        if n % 3 == 0 or n % 5 == 0:
            divisible_by_3_or_5.append(n)

    average = total / len(nums)

    return {
        "sum": total,
        "average": average,
        "minimum": min_num,
        "maximum": max_num,
        "divisible_by_3_or_5": divisible_by_3_or_5
    }


def to_binary(n: int) -> str:
    """
    Converts an integer to its binary representation using division-by-2.

    Args:
        n (int): Integer input (positive or negative).

    Returns:
        str: Binary representation as a string.
    """
    if n == 0:
        return "0"

    is_negative = n < 0
    n = abs(n)
    binary_digits = ""

    while n > 0:
        remainder = n % 2
        binary_digits = str(remainder) + binary_digits
        n = n // 2

    if is_negative:
        binary_digits = "-" + binary_digits

    return binary_digits


def main_menu():
    """
    Displays a menu to the user and drives program flow.
    """
    while True:
        print("\n=== Analyzer Menu ===")
        print("|| 1. String Analysis")
        print("|| 2. Numeric Statistics")
        print("|| 3. Binary Converter")
        print("||4. Exit")

        choice = input("Choose an option (1–4): ").strip()

        if choice == "1":
            s = input("Enter a string: ")
            result = analyze_text(s)
            print("\nString Analysis Results:")
            for key, value in result.items():
                print(f"{key.replace('_', ' ').capitalize()}: {value}")

        elif choice == "2":
            while True:
                user_input = input("Enter a comma-separated list of integers: ")
                parts = user_input.split(",")
                try:
                    nums = [int(x.strip()) for x in parts]
                    break
                except ValueError:
                    print("Invalid input. Please enter only integers separated by commas.")

            result = stats_numbers(nums)
            print("\nNumeric Statistics Results:")
            for key, value in result.items():
                print(f"{key.replace('_', ' ').capitalize()}: {value}")

        elif choice == "3":
            while True:
                user_input = input("Enter an integer: ")
                try:
                    num = int(user_input.strip())
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

            binary = to_binary(num)
            print(f"Binary representation: {binary}")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

# When the file is run directly, it shows the menu,won't run if the program is imported
if __name__ == "__main__":
    main_menu()
