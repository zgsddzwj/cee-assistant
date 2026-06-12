# tests/test_pipeline.py
def test_pipeline_validates_score_data():
    from core.pipeline import DataPipeline
    pipeline = DataPipeline()
    
    valid_data = {"score": 600, "batch": "本科一批", "year": 2023}
    invalid_data = {"score": 1000, "batch": "本科一批", "year": 2023}
    
    assert pipeline.validate_score_data(valid_data) == True
    assert pipeline.validate_score_data(invalid_data) == False