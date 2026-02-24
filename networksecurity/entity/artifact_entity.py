from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
  def __init__(self,train_file_path,test_file_path):
    self.train_file_path = train_file_path
    self.test_file_path = test_file_path