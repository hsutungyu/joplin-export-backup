from google.cloud import storage
import os

BUCKET_NAME = "gcp_pca_dan_tung"

storageClient = storage.Client()

def uploadFolderToBucket(bucketName: str, folderName: str, storageClient: storage.Client):
    """note: the bucket must exist within GCP

    Args:
        bucketName (str): the name of the bucket on GCP
        folderName (str): the folder that you want to uplaod to GCP
        storageClient (storage.Client): a storage client object
    """
    bucket = storageClient.bucket(bucketName.lower())
    
    for file in os.listdir(folderName):
        if os.path.isfile(os.path.join(folderName, file)):
            blob = bucket.blob(folderName + "/" + file)
            blob.upload_from_filename(folderName + "/" + file)


if __name__ == "__main__":
    uploadFolderToBucket(BUCKET_NAME, "GCP_PCA_Dan", storageClient)