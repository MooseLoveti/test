import subprocess
import sys

def check_ip(ip):
    cmd = (
        f"curl -s 'https://www.virustotal.com/api/v3/ip_addresses/{ip}' "
        "-H \"x-apikey: {input your api key}\" "
        "| jq -r '.data.attributes.last_analysis_stats as $s | \"\\($s.malicious)/\\(($s | to_entries | map(.value) | add))\"'"
    )
    cp = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(cp.stdout)

i = 0
args = sys.argv[1:]
while True:
    try:
        ip = args[i]
        check_ip(ip)
        i += 1
    except IndexError:
        break
