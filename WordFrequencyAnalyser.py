from collections import Counter
import re

print("=" * 40)
print("       WORD FREQUENCY ANALYSER")
print("=" * 40)

text = input("\nEnter a sentence: ")

words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

frequency = Counter(words)

print("\n========== ANALYSIS ==========")

for word, count in frequency.items():
    print(f"{word:<20} : {count}")

print("-" * 30)
print("Total words:", len(words))
print("Unique words:", len(frequency))

print("=" * 40)