import random

def coin_toss(num_tosses,p_head):
    return random.choices(["H", "T"], weights= [p_head, 1-p_head], k=num_tosses)

if __name__ == "__main__":
    num_tosses = int(input("Number of coin tosses: "))
    p_head = float(input("Probability of tossing heads (between 0 and 1, default=0.5): ") or "0.5")
    tosses = coin_toss(num_tosses, p_head)
    print(f"Results after {num_tosses} tosses:")
    print(", ".join(tosses))
    heads_count = tosses.count("H")
    print(f"Heads: {heads_count}")
    tails_count = tosses.count("T")
    print(f"Tails: {tails_count}")
