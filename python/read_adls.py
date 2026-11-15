from azure.identity import AzureCliCredential
from azure.storage.filedatalake import DataLakeServiceClient

STORAGE_ACCOUNT = "stnovabankdev01"

credential = AzureCliCredential()

service_client = DataLakeServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT}.dfs.core.windows.net",
    credential=credential
)

file_system = service_client.get_file_system_client("bronze")

print("Connecting to NovaBank Azure Data Lake...")

for file in file_system.get_paths(path="raw", recursive=True):
    if not file.is_directory:
        print(f"File: {file.name}")

print("Azure Data Lake connection successful!")