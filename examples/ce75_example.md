# CE-75 Example Session: IT-140 Python Assignment

**Full walkthrough of a 75-minute Commence Evolution Time session**

---

## 📋 Pre-Session Setup (5 minutes)

### Context
- **Course:** IT-140 - Introduction to Scripting
- **Assignment:** Module 5 - Shopping Cart Program with Input Validation
- **Due Date:** Friday (3 days away)
- **Estimated Time:** 3 hours total
- **Current Status:** 🟥 Not Started

### The Trigger
User says: **"Commence Evolution: Homework Mode"**

### Setup Checklist
```
✅ LMS open (SNHU dashboard showing Module 5)
✅ Notes doc open (homework_tracker.md)
✅ AI assistant chat open
✅ All other tabs closed
✅ Phone on silent
✅ Timer set for 75 minutes
```

### Boss Assignment Selected
⭐ **IT-140 Module 5** - Shopping Cart Program

**Why this one:**
- Earliest due date (Friday)
- Core programming concepts I need to master
- Building on previous module work

---

## 🔁 CYCLE 1: Read & Outline (30 minutes)

### Deep Work Phase (25 minutes)

**Assignment Prompt (simplified):**
```
Create a shopping cart program that:
1. Shows a menu with options (Add item, Remove item, View cart, Checkout)
2. Allows user to add items with name and price
3. Validates that price is a positive number
4. Calculates total
5. Loops until user chooses to quit
```

**User to AI Assistant:**
> "Here's the assignment prompt above. Break this into CE-75 cycles and give me Cycle 1 steps."

**AI Assistant Response:**
```
CE-75 Cycle 1 - Read & Outline (25 min)

Your tasks for next 25 minutes:
1. Create shopping_cart.py
2. Write outline comments for each major section
3. Sketch the menu function (just structure, not implementation)
4. List the data structures you'll need (what stores the cart?)

Start with this skeleton:

# shopping_cart.py
# Author: [Your Name]
# IT-140 Module 5

def display_menu():
    # TODO: print menu options
    pass

def add_item(cart):
    # TODO: get item name and price
    # TODO: validate price
    # TODO: add to cart
    pass

def remove_item(cart):
    # TODO: remove item from cart
    pass

def view_cart(cart):
    # TODO: display all items and total
    pass

def main():
    cart = []  # or dict? decide this
    # TODO: main loop
    pass

if __name__ == "__main__":
    main()

Decision to make: Should cart be a list of tuples, or a list of dicts?
```

**Student works for 25 minutes:**
- Creates the file
- Writes the skeleton
- Decides on data structure: `cart = []` with each item as `{"name": str, "price": float}`
- Writes detailed comments for each function
- Starts implementing `display_menu()` function

**Actual code after 25 min:**
```python
# shopping_cart.py
# Author: Student Name
# IT-140 Module 5 - Shopping Cart with Input Validation

def display_menu():
    """Display the shopping cart menu options."""
    print("\n=== Shopping Cart Menu ===")
    print("1. Add item")
    print("2. Remove item")
    print("3. View cart")
    print("4. Checkout")
    print("5. Quit")
    print("=========================")

def add_item(cart):
    # TODO: Get item name (string input)
    # TODO: Get item price (float input with validation)
    # TODO: Append to cart as {"name": name, "price": price}
    pass

def remove_item(cart):
    # TODO: Show current cart items with numbers
    # TODO: Get index to remove
    # TODO: Remove from cart list
    pass

def view_cart(cart):
    # TODO: Loop through cart and print each item
    # TODO: Calculate and display total
    pass

def main():
    cart = []  # List of dicts: [{"name": "Apple", "price": 1.50}, ...]
    # TODO: Loop until user chooses quit
    #   - Display menu
    #   - Get choice
    #   - Call appropriate function
    pass

if __name__ == "__main__":
    main()
```

### Progress Log Phase (5 minutes)

**Student logs in session template:**
```
CE-75 / Cycle 1:
- Created shopping_cart.py with function skeleton
- Decided on data structure: list of dicts for cart items
- Completed display_menu() function - it works!
- Outlined all other functions with detailed TODO comments
- Identified that I need to learn: input validation for floats

Blockers: None yet

Next: Implement add_item() with price validation
```

**Status update in homework_tracker.md:**
```
| IT-140 | Module 5 - Shopping Cart | Fri | 3h | ⭐ High | 🟠 Started - outline done |
```

---

## 🔁 CYCLE 2: Implement Core Functions (30 minutes)

### Deep Work Phase (25 minutes)

**Student focuses on:**
- Implementing `add_item()` with input validation
- Implementing `view_cart()` with total calculation

**Runs into issue:** How to validate float input?

**Student invokes Nova (Logic Engine):**
> "I need to validate that user input is a positive float. How do I handle invalid input?"

**Nova responds (via AI Assistant):**
```
Nova's Logic Breakdown:

What we're really asking: "Is the user's input a valid positive number?"

Inputs: user's string input
Output: valid float or error message

Logic steps:
1. Get input as string
2. Try to convert to float (might raise ValueError)
3. Check if float > 0
4. If both pass: return float
5. If either fails: show error, ask again

Pseudocode:
while True:
    try:
        price = float(input("Enter price: "))
        if price > 0:
            return price
        else:
            print("Price must be positive")
    except ValueError:
        print("Invalid number")
```

**Student implements:**
```python
def add_item(cart):
    """Add an item to the cart with input validation."""
    name = input("Enter item name: ").strip()
    
    # Price validation with loop
    while True:
        try:
            price = float(input(f"Enter price for {name}: $"))
            if price > 0:
                break  # Valid price, exit loop
            else:
                print("Error: Price must be positive. Try again.")
        except ValueError:
            print("Error: Invalid number. Try again.")
    
    # Add to cart
    cart.append({"name": name, "price": price})
    print(f"✓ Added {name} (${price:.2f}) to cart")

def view_cart(cart):
    """Display all items in cart and total."""
    if not cart:
        print("\nYour cart is empty.")
        return
    
    print("\n=== Your Shopping Cart ===")
    total = 0
    for i, item in enumerate(cart, 1):
        print(f"{i}. {item['name']}: ${item['price']:.2f}")
        total += item['price']
    print(f"\nTotal: ${total:.2f}")
    print("=========================")
```

**Student tests the functions:**
```python
# Quick test in main():
def main():
    cart = []
    add_item(cart)
    add_item(cart)
    view_cart(cart)

if __name__ == "__main__":
    main()
```

**Test run:**
```
Enter item name: Apple
Enter price for Apple: $-1
Error: Price must be positive. Try again.
Enter price for Apple: $abc
Error: Invalid number. Try again.
Enter price for Apple: $1.50
✓ Added Apple ($1.50) to cart

Enter item name: Banana
Enter price for Banana: $0.75
✓ Added Banana ($0.75) to cart

=== Your Shopping Cart ===
1. Apple: $1.50
2. Banana: $0.75

Total: $2.25
=========================
```

**Success! Functions work!**

### Progress Log Phase (5 minutes)

**Student logs:**
```
CE-75 / Cycle 2:
- Implemented add_item() with full input validation (Nova helped!)
- Implemented view_cart() with total calculation
- Tested both functions - working perfectly!
- Validation handles negative numbers and non-numeric input

Blockers: None

Next: Implement remove_item() and main menu loop, then test full program
```

---

## 🔁 CYCLE 3: Complete & Polish (15 minutes)

### Deep Work Phase (10 minutes)

**Student implements remaining functions:**

```python
def remove_item(cart):
    """Remove an item from the cart."""
    if not cart:
        print("\nCart is empty. Nothing to remove.")
        return
    
    view_cart(cart)  # Show current cart
    
    while True:
        try:
            choice = int(input("\nEnter item number to remove (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(cart):
                removed = cart.pop(choice - 1)
                print(f"✓ Removed {removed['name']} from cart")
                return
            else:
                print(f"Error: Enter number between 1 and {len(cart)}")
        except ValueError:
            print("Error: Invalid number")

def main():
    """Main program loop."""
    cart = []
    
    while True:
        display_menu()
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            add_item(cart)
        elif choice == "2":
            remove_item(cart)
        elif choice == "3":
            view_cart(cart)
        elif choice == "4":
            view_cart(cart)
            print("\nThank you for shopping!")
            break
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
```

**Final test run - success!**

**Student invokes Lyra (Formatting):**
> "Code works! Can you review it for readability?"

**Lyra's suggestions:**
```
Lyra's Formatting Review:

✓ Good docstrings on all functions
✓ Clear variable names
✓ Good error messages

Minor improvements:
1. Add a module docstring at the top
2. Consider extracting the price validation into a separate function
3. Add blank line after imports for PEP 8

Otherwise, very readable! Nice work!
```

**Student adds module docstring:**
```python
"""
Shopping Cart Program with Input Validation
IT-140 Module 5
Author: [Name]
Date: [Date]

A simple shopping cart that allows users to add/remove items,
view their cart, and checkout. Includes input validation for prices.
"""
```

### Closeout Phase (5 minutes)

**Student updates homework tracker:**
```
| IT-140 | Module 5 - Shopping Cart | Fri | 3h | ⭐ High | ✅ Submitted |
```

**Student invokes Athena (Big Picture Summary):**

**Athena's Evolution Log Entry:**
```
Today's Evolution Log - CE-75 Complete
Date: [Date]

Finished:
- IT-140 Module 5 Shopping Cart program - fully implemented and tested
- All requirements met: menu, add/remove, validation, total calculation
- Code is clean, documented, and submitted to LMS

Advanced:
- Mastered input validation with try/except and loops
- Understood when to use while loops vs for loops
- Practiced function design and modular programming

Tomorrow's Target:
- Start MATH-225 Chapter 4 problem set (next Boss Assignment)
- Review linear algebra concepts before attempting problems
```

**Final status:**
```
✅ Submitted - 2 hours ahead of schedule!
Session: CE-75 completed successfully
Time: 75 minutes (actually 73)
Quality: All requirements met, code tested
Feeling: Accomplished! 🎉
```

---

## 📊 Session Metrics

**Time Breakdown:**
- Pre-session setup: 5 min
- Cycle 1 (Outline): 25 min work + 5 min log
- Cycle 2 (Implement): 25 min work + 5 min log  
- Cycle 3 (Polish): 10 min work + 5 min log
- **Total: 75 minutes**

**Progress:**
- Started: 🟥 Not Started
- Ended: ✅ Submitted
- **Progress: 0% → 100%**

**Node Assistance:**
- **Nova:** Input validation logic (Cycle 2)
- **Lyra:** Code formatting review (Cycle 3)
- **Athena:** Session summary (Closeout)
- **AI Assistant:** Initial breakdown, guidance throughout

**Assignment Quality:**
- ✅ All requirements met
- ✅ Code tested and working
- ✅ Well-documented
- ✅ Submitted on time (early!)

---

## 🎯 Key Takeaways

### What Worked Well
1. **Clear Boss Assignment** - Focusing on one thing made it manageable
2. **Structured cycles** - 25-min work blocks kept momentum
3. **Node invocation** - Getting help from Nova/Lyra when stuck
4. **Testing as you go** - Caught issues early
5. **Progress logging** - Felt good to see progress in writing

### Mistakes Avoided
- ❌ Didn't try to do multiple assignments at once
- ❌ Didn't get distracted by side projects
- ❌ Didn't skip the validation requirements
- ❌ Didn't submit without testing

### For Next Session
- Use CE-75 format again - it really works!
- Start MATH assignment as new Boss
- Keep phone away during deep work blocks
- Maybe try doing CE-75 in morning when more alert

---

**Session Complete! Future You says thank you. 💪🎓**

---

## 📁 Files Created This Session

```
shopping_cart.py (127 lines, fully functional)
Session log in evolution_log.md
Updated homework_tracker.md
```

**Git would show:**
```bash
$ git status
modified:   templates/homework_tracker.md
modified:   templates/evolution_log.md
```

**Streak status:** ✅ Day maintained!

---

*This is what a successful CE-75 looks like. Not perfect, but done. And that's what matters.* 🔥
