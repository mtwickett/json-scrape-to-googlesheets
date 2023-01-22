# JSON DATA SCRAPE TO GOOGLE SHEETS

## Description

This project takes public transport disruption data in json format from the [Philidelphia Septa website](http://www3.septa.org/hackathon/Alerts/get_alert_data.php?req1=all) and uploads it in readable form to Google 
Sheets.

## How To Install The Project

*Make sure you have paired SSH keys with Github*

From the main repository page click the green Code button dropdown, then copy the SSH URL and run the following command from the command line in your chosen location:
```
git clone [SSH URL]
```
Move into the repository folder that has just been created and run:
```
pip install -r requirements.txt
```

## Google Sheets And Credentials Set Up

*Make sure you have a Google Account"

1. Go to the Google Cloud Console [here](https://console.cloud.google.com/) and click on `API's and Services`. Click `Create Project`, choose a project name and click `Create`
2. Enable the Google Drive API and the Google Sheets API by clicking `Enable API's and Services`. Under the `Google Workspace` section click on the
   `Google Drive API` and click `Enable`. Then do the same for the `Google Sheets API`. Now you should be able to see these in the `Enabled API's and Services` section
   of your project
3. Click on `Credentials` -> `Create Credentials` -> `Service Account`. Name the service account `philly_json_data` and click `Create And Continue` -> `Continue` ->
   `Done`
4. In the `Credentials` page under the `Service Accounts` section, click on the `Edit Service Account` pen. Click `Keys` -> `Add Key` -> `Create New Key`, 
   leave JSON selected and click `Create`. This has downloaded a credentials json file to your computer
6. Rename the file to `credentials.json` and put it inside the json-scrape-to-googlesheets repository folder
7. Go to your Google Drive [here](https://drive.google.com/drive/my-drive) and click `New` -> `Google Sheets` to open a new spread sheet. Name the Spreadsheet `json_scrape`
8. Inside the sheet click on `Share`, paste in the "client email" from the credentials.json file, untick `Notify` and click `Share`

## How To Run

Move into the json_scrape folder and run:
```
python3 main.py
```

## Troubleshooting

**Invalid JWT** The virtual machines clock may not be in sync. Run:
```
sudo hwclock -s
```
