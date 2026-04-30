# tools/recon_tools.py

import subprocess
import os
import requests
from shodan import Shodan

class ReconTools:

    def curl_request(self, url):
        try:
            result = subprocess.run(
                ["curl", "-s", url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )
            return result.stdout.decode("utf-8")
        except Exception as e:
            return f"Error: {str(e)}"


    def nuclei_scan(self, target):
        try:
            if not target.startswith("http"):
                return "Invalid target."

            result = subprocess.run(
                ["nuclei", "-u", target, "-silent"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )

            output = result.stdout.decode("utf-8")
            return output if output.strip() else "No vulnerabilities found."

        except Exception as e:
            return f"Error: {str(e)}"


    def gobuster_scan(self, url, wordlist="/usr/share/wordlists/dirb/big.txt"):
        try:
            result = subprocess.run(
                ["gobuster", "dir", "-u", url, "-w", wordlist, "-q"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )

            output = result.stdout.decode("utf-8")
            return output if output.strip() else "No directories found."

        except Exception as e:
            return f"Error: {str(e)}"


    def shodan_search(self, query):
        try:
            api_key = os.getenv("SHODAN_API_KEY")
            if not api_key:
                return "Missing SHODAN_API_KEY"

            api = Shodan(api_key)
            results = api.search(query)

            return results.get("matches", [])[:5]

        except Exception as e:
            return f"Error: {str(e)}"


    def get_cve(self, cve_id):
        try:
            username = os.getenv("OPENCVE_USERNAME")
            password = os.getenv("OPENCVE_PASSWORD")

            if not username or not password:
                return "Missing OpenCVE credentials"

            url = f"https://app.opencve.io/api/cve/{cve_id}"
            response = requests.get(url, auth=(username, password))

            if response.status_code != 200:
                return f"Error {response.status_code}"

            data = response.json()

            return {
                "id": data.get("id"),
                "summary": data.get("summary"),
                "cvss": data.get("cvss")
            }

        except Exception as e:
            return f"Error: {str(e)}"
        
    def nuclei_scan(self, target, templates=""):
        """
        Run Nuclei vulnerability scan

        target: URL or IP
        templates: optional template path
        """

        try:
            cmd = ["nuclei", "-u", target]

            # Add templates if provided
            if templates:
                cmd.extend(["-t", templates])

            # Default behavior: fast scan
            cmd.extend([
                "-silent",
                "-no-color"
            ])

            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )

            output = result.stdout.decode("utf-8")

            # If nothing found, return meaningful message
            if not output.strip():
                return "No vulnerabilities detected by Nuclei"

            return output

        except FileNotFoundError:
            return "Error: nuclei not installed or not in PATH"

        except Exception as e:
            return f"Error: {str(e)}"