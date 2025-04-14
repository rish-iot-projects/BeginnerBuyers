# Author: Rishabh Sinha
# Date: April 14, 2025
# Description: Fetches real estate listings for a given area using the RentCast API via RapidAPI
#              and filters them based on user-defined criteria. Saves results to a JSON file.

import requests
import json

def fetch_listings(city, state, max_price=500000, min_bedrooms=2):
    """
    Fetch real estate listings from RentCast API for a given city and state.
    Returns a list of listings matching criteria.
    """
    api_key = "YOUR_RAPIDAPI_KEY"  # Replace with your RapidAPI key
    url = "https://realty-mole-property-api.p.rapidapi.com/properties"
    
    querystring = {
        "city": city,
        "state": state,
        "limit": "10"  # Adjust limit as needed
    }
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        listings = response.json()
        
        # Filter listings based on criteria
        filtered_listings = [
            listing for listing in listings
            if listing.get("price", float("inf")) <= max_price
            and listing.get("bedrooms", 0) >= min_bedrooms
        ]
        
        return filtered_listings
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching listings: {e}")
        return []

def display_listings(listings):
    """Display listings in a readable format."""
    if not listings:
        print("No listings found.")
        return
    
    for i, listing in enumerate(listings, 1):
        print(f"\nListing {i}:")
        print(f"Address: {listing.get('formattedAddress', 'N/A')}")
        print(f"Price: ${listing.get('price', 'N/A')}")
        print(f"Bedrooms: {listing.get('bedrooms', 'N/A')}")
        print(f"Bathrooms: {listing.get('bathrooms', 'N/A')}")
        print(f"Size: {listing.get('squareFootage', 'N/A')} sq ft")

def save_listings(listings, filename="listings.json"):
    """Save listings to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(listings, f, indent=4)
    print(f"Listings saved to {filename}")

def main():
    # Example location (modify as needed)
    city = input("Enter city (e.g., Chicago): ") or "Chicago"
    state = input("Enter state (e.g., IL): ") or "IL"
    
    # Fetch and filter listings
    listings = fetch_listings(
        city=city,
        state=state,
        max_price=400000,  # Matches example budget from your prior list
        min_bedrooms=2     # Matches example must-have
    )
    
    # Display results
    display_listings(listings)
    
    # Save results
    save_option = input("\nWould you like to save these listings? (yes/no): ").lower()
    if save_option == 'yes':
        save_listings(listings)

if __name__ == "__main__":
    main()
