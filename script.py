import requests
import json

# Fetch the data from the Wikimedia API
with open('api-result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Initialize an empty dictionary to store the language details
languages = {}

# Loop through each language entry in the response
for lang_info in data["sitematrix"].values():
    if isinstance(lang_info, dict):  # Skip non-dictionary items like "count"
        # Extract the language code
        lang_code = lang_info.get("code", "")
        
        # Create a dictionary for each language entry with necessary fields
        language_details = {
            "name": lang_info.get("name", ""),
            "localname": lang_info.get("localname", ""),
            "sitename": []
        }

        # Check and add all sitenames to the language entry if 'site' is available
        if "site" in lang_info:
            for site in lang_info["site"]:
                site_details = {
                    "url": site.get("url", ""),
                    "dbname": site.get("dbname", ""),
                    "code": site.get("code", ""),
                    "sitename": site.get("sitename", ""),
                    "closed": site.get("closed", ""),
                }
                language_details["sitename"].append(site_details)

        # Add the language details to the dictionary with the language code as the key
        if lang_code:  # Ensure there's a valid language code
            languages[lang_code] = language_details

# Write the languages dictionary to a JSON file
with open("languages_output.json", "w", encoding="utf-8") as json_file:
    json.dump(languages, json_file, indent=4, ensure_ascii=False)

print("JSON file has been generated successfully.")
