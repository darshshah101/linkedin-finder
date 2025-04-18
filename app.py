from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API Setup
API_KEY = "32076b2f88d09bda2bf7cccc642d6db18580d9ef"
HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def search_linkedin(company, role):
    query = f'site:linkedin.com/in "{role}" "{company}"'
    url = "https://google.serper.dev/search"
    payload = { "q": query }

    try:
        res = requests.post(url, headers=HEADERS, json=payload)
        res.raise_for_status()
        results = res.json()

        entries = []
        for result in results.get("organic", []):
            if "linkedin.com/in" in result["link"]:
                snippet = result.get("snippet", "").lower()
                title = result.get("title", "")
                company_lower = company.lower()

                if company_lower in snippet or company_lower in title.lower():
                    # Try to split title into "Name - Role"
                    if " - " in title:
                        name, designation = title.split(" - ", 1)
                    else:
                        name, designation = title.strip(), "N/A"

                    entries.append({
                        "name": name.strip(),
                        "designation": designation.strip(),
                        "url": result["link"]
                    })

        return entries

    except Exception as e:
        return [{"name": "API Error", "designation": str(e), "url": ""}]

@app.route('/', methods=['GET', 'POST'])
def index():
    links = []
    searched = False

    if request.method == 'POST':
        company = request.form.get('company')
        role = request.form.get('role')
        links = search_linkedin(company.strip(), role.strip())
        searched = True

    return render_template('index.html', links=links, searched=searched)

##if __name__ == '__main__':
 ##   app.run(debug=True)
