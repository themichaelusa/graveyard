from sys import cwd 

def export_data_to_gcs(dataset_name, table_name, destination):
    bigquery_client = bigquery.Client()
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)
    job_name = str(uuid.uuid4())

    job = bigquery_client.extract_table_to_storage(job_name, table, destination)

    job.begin()
    job.result()  # Wait for job to complete

    print('Exported {}:{} to {}'.format(
        dataset_name, table_name, destination))


if __name__ == "__main__":
	repoDatasetName = 'bigquery-public-data:github_repos'
	#export_data_to_gcs(repoDatasetName, 'contents', cwd)

	from oauth2client.client import GoogleCredentials
	credentials = GoogleCredentials.get_application_default()
	#print(credentials)
