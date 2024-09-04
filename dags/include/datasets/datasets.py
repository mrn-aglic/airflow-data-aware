from airflow import Dataset

SIMPLE_DATASET = Dataset("simple_dataset")
ENRICHED_DATASET = Dataset("enriched_dataset")
ENRICHED_DATASET_TRIGGER = Dataset("enriched_dataset_trigger_dagrun")