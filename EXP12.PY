# Function to generate the full XOR truth table
def xor_truth_table():
    print("\nXOR Truth Table:")
    print("A | B | A ⊕ B")
    print("--|---|------")
    for A in [0, 1]:
        for B in [0, 1]:
            print(f"{A} | {B} |  {A ^ B}")

# Function to compute XOR for user inputs
def xor_user_input():
    try:
        A = int(input("\nEnter value for A (0 or 1): "))
        B = int(input("Enter value for B (0 or 1): "))
        
        if A not in [0, 1] or B not in [0, 1]:
            print("Invalid input! Please enter only 0 or 1.")
            return

        print(f"{A} ⊕ {B} = {A ^ B}")

    except ValueError:
        print("Invalid input! Please enter only numbers (0 or 1).")

# Main menu
def main():
    while True:
        print("\n XOR Operation Menu")
        print("1️ Compute XOR for user input")
        print("2️ Display XOR truth table")
        print("3️ Exit")

        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            xor_user_input()
        elif choice == "2":
            xor_truth_table()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

# Run the program
main()
