import json

def create_homebuyer_list():
    home_list = {
        "Budget": {},
        "Must_Haves": [],
        "Nice_to_Haves": [],
        "Location": [],
        "Dealbreakers": [],
        "Future_Needs": [],
        "Financing_Logistics": {}
    }
    
    print("=== First-Time Homebuyer List Creator ===")
    
    # Budget
    home_list["Budget"]["Max_Price"] = float(input("Enter your maximum purchase price ($): ") or 0)
    home_list["Budget"]["Monthly_Payment"] = float(input("Enter max monthly payment ($): ") or 0)
    home_list["Budget"]["Down_Payment"] = float(input("Enter down payment amount ($): ") or 0)
    
    # Must-Haves
    print("\nEnter must-have features (e.g., '3 bedrooms', '2 bathrooms'). Type 'done' when finished:")
    while True:
        feature = input("- ")
        if feature.lower() == 'done':
            break
        home_list["Must_Haves"].append(feature)
    
    # Nice-to-Haves
    print("\nEnter nice-to-have features (e.g., 'modern kitchen', 'large backyard'). Type 'done' when finished:")
    while True:
        feature = input("- ")
        if feature.lower() == 'done':
            break
        home_list["Nice_to_Haves"].append(feature)
    
    # Location
    print("\nEnter location preferences (e.g., 'downtown', 'near schools'). Type 'done' when finished:")
    while True:
        location = input("- ")
        if location.lower() == 'done':
            break
        home_list["Location"].append(location)
    
    # Dealbreakers
    print("\nEnter dealbreakers (e.g., 'needs major repairs', 'flood zone'). Type 'done' when finished:")
    while True:
        dealbreaker = input("- ")
        if dealbreaker.lower() == 'done':
            break
        home_list["Dealbreakers"].append(dealbreaker)
    
    # Future Needs
    print("\nEnter future needs (e.g., 'room for kids', 'home office'). Type 'done' when finished:")
    while True:
        future = input("- ")
        if future.lower() == 'done':
            break
        home_list["Future_Needs"].append(future)
    
    # Financing and Logistics
    home_list["Financing_Logistics"]["Mortgage_Type"] = input("\nEnter mortgage type (e.g., FHA, conventional): ") or "Not specified"
    home_list["Financing_Logistics"]["Move_In_Timeline"] = input("Enter move-in timeline (e.g., 3 months): ") or "Not specified"
    
    return home_list

def display_list(home_list):
    print("\n=== Your Homebuyer List ===")
    for category, items in home_list.items():
        print(f"\n{category.replace('_', ' ')}:")
        if isinstance(items, dict):
            for key, value in items.items():
                print(f"  - {key.replace('_', ' ')}: {value}")
        else:
            for item in items:
                print(f"  - {item}")
                
def save_list(home_list, filename="homebuyer_list.json"):
    with open(filename, 'w') as f:
        json.dump(home_list, f, indent=4)
    print(f"\nList saved to {filename}")

def main():
    home_list = create_homebuyer_list()
    display_list(home_list)
    save_option = input("\nWould you like to save this list? (yes/no): ").lower()
    if save_option == 'yes':
        save_list(home_list)
    print("\nGood luck with your home search!")

if __name__ == "__main__":
    main()
