import os
import unittest
from unittest.mock import MagicMock, Mock, patch

import pytest
from transformers import (
    AutoTokenizer
)

from azureml.automl.dnn.nlp.common.constants import DataLiterals, OutputLiterals, ModelNames
from azureml.automl.dnn.nlp.ner.io.read.dataloader import load_and_validate_dataset
from ..mocks import file_dataset_mock, MockValidator


@pytest.mark.usefixtures('new_clean_dir')
class DataLoaderTest(unittest.TestCase):
    """Tests for NER data loader."""
    def __init__(self, *args, **kwargs):
        super(DataLoaderTest, self).__init__(*args, **kwargs)

    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    def test_load_dataset(self, validator_mock, get_by_id_mock):
        mock_file_dataset = file_dataset_mock()
        get_by_id_mock.return_value = mock_file_dataset
        dataset_id = "mock_id"
        validation_dataset_id = "mock_validation_id"
        workspace_mock = Mock()
        ner_dir = DataLiterals.NER_DATA_DIR
        output_dir = OutputLiterals.OUTPUT_DIR
        labels_file = "test_load_dataset_labels.txt"
        tokenizer = AutoTokenizer.from_pretrained(ModelNames.BERT_BASE_CASED)

        # data validation mock
        validator_mock.return_value = MockValidator()

        train_dataset, eval_dataset, label_list = load_and_validate_dataset(
            workspace_mock,
            ner_dir,
            output_dir,
            labels_file,
            tokenizer,
            dataset_id,
            validation_dataset_id,
        )

        self.assertEqual(get_by_id_mock.call_count, 2)
        self.assertEqual(mock_file_dataset.download.call_count, 2)
        self.assertEqual(mock_file_dataset.to_path.call_count, 2)
        self.assertEqual(len(train_dataset.data), 3)
        self.assertEqual(len(eval_dataset.data), 2)
        self.assertEqual(
            set(label_list),
            set(['I-PER', 'I-ORG', 'B-LOC', 'B-PER', 'B-ORG', 'I-MISC', 'B-MISC', 'O'])
        )
        labels_output_path = os.path.join(output_dir, labels_file)
        with open(labels_output_path, 'r') as f:
            labels = [line.rstrip() for line in f]
        self.assertIsNotNone(labels)
        self.assertEqual(
            set(labels),
            set(['I-PER', 'I-ORG', 'B-LOC', 'B-PER', 'B-ORG', 'I-MISC', 'B-MISC', 'O'])
        )

    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    def test_load_dataset_train_data_only(self, validator_mock, get_by_id_mock):
        mock_file_dataset = file_dataset_mock()
        get_by_id_mock.return_value = mock_file_dataset
        dataset_id = "mock_id"
        workspace_mock = Mock()
        ner_dir = DataLiterals.NER_DATA_DIR
        output_dir = "ner_data/output_dir"
        labels_file = "test_load_dataset_labels.txt"
        tokenizer = AutoTokenizer.from_pretrained(ModelNames.BERT_BASE_CASED)

        # data validation mock
        validator_mock.return_value = MockValidator()

        train_dataset, eval_dataset, label_list = load_and_validate_dataset(
            workspace_mock,
            ner_dir,
            output_dir,
            labels_file,
            tokenizer,
            dataset_id,
            None,
        )

        self.assertEqual(get_by_id_mock.call_count, 1)
        self.assertEqual(mock_file_dataset.download.call_count, 1)
        self.assertEqual(mock_file_dataset.to_path.call_count, 1)
        self.assertEqual(len(train_dataset.data), 3)
        self.assertIsNone(eval_dataset)
        self.assertEqual(
            set(label_list),
            set(['I-PER', 'I-ORG', 'B-LOC', 'B-PER', 'B-ORG', 'I-MISC', 'B-MISC', 'O'])
        )
        labels_output_path = os.path.join(output_dir, labels_file)
        with open(labels_output_path, 'r') as f:
            labels = [line.rstrip() for line in f]
        self.assertIsNotNone(labels)
        self.assertEqual(
            set(labels),
            set(['I-PER', 'I-ORG', 'B-LOC', 'B-PER', 'B-ORG', 'I-MISC', 'B-MISC', 'O'])
        )

    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    def test_load_dataset_same_ids(self, validator_mock, get_by_id_mock):
        mock_file_dataset = file_dataset_mock([["/train.txt"], ["/train.txt"]])
        get_by_id_mock.return_value = mock_file_dataset
        dataset_id = "mock_id"
        validation_dataset_id = "mock_id"
        workspace_mock = Mock()
        ner_dir = DataLiterals.NER_DATA_DIR
        output_dir = OutputLiterals.OUTPUT_DIR
        labels_file = "test_load_dataset_labels.txt"
        tokenizer = MagicMock()

        # data validation mock
        validator_mock.return_value = MockValidator()

        train_dataset, eval_dataset, label_list = load_and_validate_dataset(
            workspace_mock,
            ner_dir,
            output_dir,
            labels_file,
            tokenizer,
            dataset_id,
            validation_dataset_id,
        )

        self.assertEqual(get_by_id_mock.call_count, 2)
        self.assertEqual(mock_file_dataset.download.call_count, 2)
        self.assertEqual(mock_file_dataset.to_path.call_count, 2)
        self.assertEqual(len(train_dataset.data), 3)
        self.assertEqual(len(eval_dataset.data), 3)


if __name__ == "__main__":
    unittest.main()
