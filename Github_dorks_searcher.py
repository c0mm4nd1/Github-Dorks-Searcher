import requests
import urllib.parse
import getpass
import os

print("""
  #####  ### ####### #     # #     # ######     ######  ####### ######  #    #  #####      #####  #######    #    ######   #####  #     # ####### ######  
 #     #  #     #    #     # #     # #     #    #     # #     # #     # #   #  #     #    #     # #         # #   #     # #     # #     # #       #     # 
 #        #     #    #     # #     # #     #    #     # #     # #     # #  #   #          #       #        #   #  #     # #       #     # #       #     # 
 #  ####  #     #    ####### #     # ######     #     # #     # ######  ###     #####      #####  #####   #     # ######  #       ####### #####   ######  
 #     #  #     #    #     # #     # #     #    #     # #     # #   #   #  #         #          # #       ####### #   #   #       #     # #       #   #   
 #     #  #     #    #     # #     # #     #    #     # #     # #    #  #   #  #     #    #     # #       #     # #    #  #     # #     # #       #    #  
  #####  ###    #    #     #  #####  ######     ######  ####### #     # #    #  #####      #####  ####### #     # #     #  #####  #     # ####### #     # 
                                                                                                                                                          

                                                                                                By C0mm4nd1
""")

GITHUB_TOKEN = getpass.getpass("🔑 Enter your GitHub token: ").strip()
GITHUB_API_URL = "https://api.github.com/search/code"
dork_terms = [
    "password", "npmrc _auth", "dockercfg", "pem private", "id_rsa", "aws_access_key_id",
    "s3cfg", "htpasswd", "git-credentials", "bashrc password", "sshd_config", "xoxp OR xoxb OR xoxa",
    "SECRET_KEY", "client_secret", "github_token", "api_key", "FTP", "app_secret",
    "passwd", ".env", ".exs", "beanstalkd.yml", "deploy.rake", "mysql", "credentials",
    "PWD", ".bash_history", ".sls", "secrets", "composer.json"
]

keyword = input("Enter the keyword for the GitHub search: ").strip()
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

test_response = requests.get("https://api.github.com/user", headers=headers)
if test_response.status_code != 200:
    print(f"❌ Error: Invalid token ({test_response.json().get('message', 'Unknown')})")
    exit()

output_file = "github_dorks_results.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write(f"🔍 GitHub search results for '{keyword}'\n")
    file.write("=" * 80 + "\n\n")

    for term in dork_terms:
        query = f'"{keyword}" {term}'
        params = {"q": query, "per_page": 10}
        response = requests.get(GITHUB_API_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f"⚠️ Error in search '{term}': {response.json().get('message', 'Unknown')}")
            continue

        results = response.json().get("items", [])
        total_results = len(results)

        file.write(f"🔹 {term.upper()} ({total_results} results)\n")
        file.write("-" * 80 + "\n")
        if results:
            for item in results:
                file.write(f"📄 {item['html_url']}\n")
            print(f"✅ '{term}': {total_results} results found.")
        else:
            file.write("❌ No results found\n")
            print(f"❌ '{term}': No results found.")

        file.write("\n")

print(f"\n✅ Search completed. Results saved in '{output_file}'.")
