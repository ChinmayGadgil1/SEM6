def food_nutrition_expert_system():
    print("Food Nutrition Expert System")
    print()

    goal = input(
        "What is your goal? "
        "(weight_gain/weight_loss/muscle_gain): "
    ).strip().lower()

    vegetarian = input(
        "Are you vegetarian? (yes/no): "
    ).strip().lower()

    appetite = input(
        "Do you have poor appetite? (yes/no): "
    ).strip().lower()

    print("\nAnalyzing your preferences...\n")

    if goal == "weight_gain":
        if vegetarian == "yes":
            if appetite == "yes":
                print("Recommended Plan:")
                print("- Banana Milkshake")
                print("- Peanut Butter")
                print("- Paneer")
                print("- Dry Fruits")
                print("- Soy Chunks")
            else:
                print("Recommended Plan:")
                print("- Rice")
                print("- Dal")
                print("- Paneer")
                print("- Potatoes")
                print("- Nuts")
        else:
            if appetite == "yes":
                print("Recommended Plan:")
                print("- Eggs")
                print("- Chicken Soup")
                print("- Fish")
                print("- Milk")
                print("- Nuts")
            else:
                print("Recommended Plan:")
                print("- Chicken")
                print("- Eggs")
                print("- Fish")
                print("- Rice")
                print("- Milk")

    elif goal == "weight_loss":
        if vegetarian == "yes":
            print("Recommended Plan:")
            print("- Salad")
            print("- Oats")
            print("- Fruits")
            print("- Green Tea")
            print("- Vegetables")
        else:
            print("Recommended Plan:")
            print("- Grilled Chicken")
            print("- Boiled Eggs")
            print("- Vegetables")
            print("- Fruits")
            print("- Soup")

    elif goal == "muscle_gain":
        if vegetarian == "yes":
            print("Recommended Plan:")
            print("- Paneer")
            print("- Soy Chunks")
            print("- Milk")
            print("- Oats")
            print("- Peanut Butter")
        else:
            print("Recommended Plan:")
            print("- Chicken")
            print("- Eggs")
            print("- Fish")
            print("- Milk")
            print("- Rice")

    else:
        print("Invalid Goal")


food_nutrition_expert_system()