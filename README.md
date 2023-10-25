Command to push the csv:
curl -X POST --header "Content-Type: text/csv" --data-binary "@/Users/toddzheng/.tmp/LK0Euuwxl8.csv" http://127.0.0.1:5000/cmd/XXX

curl -X POST --header "Content-Type: text/csv" --header "Authorization: Bearer $(gcloud auth print-identity-token)" --data-binary "@/Users/toddzheng/.tmp/LK0Euuwxl8.csv" https://<cloud run url>/cmd/XXX