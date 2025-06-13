# Getting Started
1. upload km data to the gcs and milvus
```
python upload_km_data.py
```
2. do the testing using this python script below.
```
python main.py
```

```
deepeval set-gemini     --model-name=gemini-2.5-flash-preview-04-17     --project-id=project_name     --location=us-central1
```