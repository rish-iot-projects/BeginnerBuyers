# Author: Rishabh
# Date: April 14, 2025
# Description: Fetches real estate listings using pyRealtor, saves them to a SQLite database,
#              and allows retrieval of saved listings.

import sqlite3
import json
from datetime import datetime
import pyRealtor  # Direct import of pyRealtor

def init_database():
    """Initialize SQLite database using setup_listings.sql."""
    conn = sqlite3.connect("listings.db")
    cursor = conn.cursor()
    
    with open("setup_listings.sql", "r") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()
    print("Database initialized.")

def fetch_listings(city, state, max_price=500000, min_bedrooms=2):
    """Fetch real estate listings using pyRealtor."""
    try:
        # Initialize pyRealtor without API key
        realtor = pyRealtor.Realtor()  # Assumes pyRealtor handles authentication internally
        
        # Fetch listings for the given city and state
        listings = realtor.search_properties(
            city=city,
            state_code=state,
            limit=10,
            prop_type="house"  # Single-family homes; adjust as needed
        )
        
        # Filter listings based on criteria
        filtered_listings = [
            {
                "address": listing.get("address", {}).get("line", "N/A") + ", " + 
                          listing.get("address", {}).get("city", city) + ", " + 
                          listing.get("address", {}).get("state_code", state),
                "price": listing.get("price", float("inf")),
                "bedrooms": listing.get("beds", 0),
                "bathrooms": listing.get("baths", 0),
                "squareFootage": listing.get("sqft", 0)
            }
            for listing in listings
            if listing.get("price", float("inf")) <= max_price
            and listing.get("beds", 0) >= min_bedrooms
        ]
        
        return filtered_listings
    
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return []

def save_listings_to_db(listings, user_name, city, state):
    """Save listings to SQLite database."""
    conn = sqlite3.connect("listings.db")
    cursor = conn.cursor()
    
    for listing in listings:
        cursor.execute("""
            INSERT INTO Listings (
                user_name, address, price, bedrooms, bathrooms,
                square_footage, city, state
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_name,
            listing.get("address", "N/A"),
            listing.get("price", None),
            listing.get("bedrooms", None),
            listing.get("bathrooms", None),
            listing.get("squareFootage", None),
            city,
            state
        ))
    
    conn.commit()
    conn.close()
    print(f"Listings saved to database for {user_name}.")

def retrieve_listings(user_name):
    """Retrieve saved listings for a user from SQLite database."""
    conn = sqlite3.connect("listings.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Listings WHERE user_name = ?", (user_name,))
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def display_listings(listings):
    """Display listings fetched from pyRealtor."""
    if not listings:
        print("No listings found.")
        return
    
    for i, listing in enumerate(listings, 1):
        print(f"\nListing {i}:")
        print(f"Address: {listing.get('address', 'N/A')}")
        print(f"Price: ${listing.get('price', 'N/A')}")
        print(f"Bedrooms: {listing.get('bedrooms', 'N/A')}")
        print(f"Bathrooms: {listing.get('bathrooms', 'N/A')}")
        print(f"Size: {listing.get('squareFootage', 'N/A')} sq ft")

def display_saved_listings(rows):
    """Display saved listings from database."""
    if not rows:
        print("No saved listings found.")
        return
    
    for i, row in enumerate(rows, 1):
        print(f"\nSaved Listing {i}:")
        print(f"Address: {row[2]}")
        print(f"Price: ${row[3] if row[3] else 'N/A'}")
        print(f"Bedrooms: {row[4] if row[4] else 'N/A'}")
        print(f"Bathrooms: {row[5] if row[5] else 'N/A'}")
        print(f"Size: {row[6] if row[6] else 'N/A'} sq ft")
        print(f"City: {row[7]}, {row[8]}")
        print(f"Saved At: {row[9]}")

def save_listings_to_json(listings, filename="listings.json"):
    """Save listings to a JSON file (optional)."""
    with open(filename, 'w') as f:
        json.dump(listings, f, indent=4)
    print(f"Listings saved to {filename}")

def main():
    # Initialize database
    init_database()
    
    # Get user info
    user_name = input("Enter your name: ") or "Guest"
    city = input("Enter city (e.g., Chicago): ") or "Chicago"
    state = input("Enter state (e.g., IL): ") or "IL"
    
    while True:
        print("\n=== Home Listings Menu ===")
        print("1. Fetch new listings")
        print("2. View saved listings")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            # Fetch and display new listings
            listings = fetch_listings(
                city=city,
                state=state,
                max_price=400000,  # Matches your homebuyer list example
                min_bedrooms=2
            )
            display_listings(listings)
            
            # Save options
            if listings:
                save_option = input("\nSave to database? (yes/no): ").lower()
                if save_option == 'yes':
                    save_listings_to_db(listings, user_name, city, state)
                
                json_option = input("Save to JSON file? (yes/no): ").lower()
                if json_option == 'yes':
                    save_listings_to_json(listings)
        
        elif choice == "2":
            # Retrieve and display saved listings
            saved_listings = retrieve_listings(user_name)
            display_saved_listings(saved_listings)
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()