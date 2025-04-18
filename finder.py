import requests
import csv
import time

HEADERS = {
    "X-API-KEY": "32076b2f88d09bda2bf7cccc642d6db18580d9ef",  # your API key
    "Content-Type": "application/json"
}

def google_search(query):
    url = "https://google.serper.dev/search"
    data = { "q": query }

    try:
        res = requests.post(url, headers=HEADERS, json=data)
        res.raise_for_status()
        results = res.json()
        links = []

        for result in results.get("organic", []):
            if "linkedin.com/in" in result["link"]:
                links.append(result["link"])

        return links

    except Exception as e:
        print(f"❌ API Error: {e}")
        return []

def main():
    with open("inputs.csv", newline='') as infile, open("output.csv", "w", newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=["company", "role", "linkedin_url"])
        writer.writeheader()

        for row in reader:
            company = row["company_name"]
            role = row["desired_role"]
            print(f"\n🔍 Searching: {role} at {company}")

            query = f'site:linkedin.com/in "{role}" "{company}"'
            links = google_search(query)

            if not links:
                print("⚠️  No LinkedIn links found.")
            else:
                for link in links:  # 💡 Now includes ALL matches
                    writer.writerow({
                        "company": company,
                        "role": role,
                        "linkedin_url": link
                    })
                    print("✅ Found:", link)

            time.sleep(1)  # be polite to the API

if __name__ == "__main__":
    main()
