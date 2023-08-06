import copy
import json
import os
import tempfile
from unittest.mock import patch

from octue import definitions, exceptions
from octue.cloud import storage
from octue.cloud.storage import GoogleCloudStorageClient
from octue.resources import Datafile, Dataset
from octue.resources.filter_containers import FilterSet
from tests import TEST_BUCKET_NAME
from tests.base import BaseTestCase
from tests.resources import create_dataset_with_two_files


class TestDataset(BaseTestCase):
    def _create_nested_cloud_dataset(self, dataset_name="a_dataset"):
        cloud_storage_client = GoogleCloudStorageClient()

        cloud_storage_client.upload_from_string(
            "[1, 2, 3]", cloud_path=storage.path.generate_gs_path(TEST_BUCKET_NAME, dataset_name, "file_0.txt")
        )

        cloud_storage_client.upload_from_string(
            "[4, 5, 6]", cloud_path=storage.path.generate_gs_path(TEST_BUCKET_NAME, dataset_name, "file_1.txt")
        )

        cloud_storage_client.upload_from_string(
            "['a', 'b', 'c']",
            cloud_path=storage.path.generate_gs_path(TEST_BUCKET_NAME, dataset_name, "sub-directory/sub_file.txt"),
        )

        cloud_storage_client.upload_from_string(
            "['blah', 'b', 'c']",
            cloud_path=storage.path.generate_gs_path(
                TEST_BUCKET_NAME, dataset_name, "sub-directory", "sub-sub-directory", "sub_sub_file.txt"
            ),
        )

    def _create_files_and_nested_subdirectories(self, directory_path):
        """Create files and nested subdirectories of files in the given directory.

        :param str directory_path: the directory to create the nested structure in
        :return list(str): the paths of the files in the directory and subdirectories
        """
        paths = [
            os.path.join(directory_path, "file_0.txt"),
            os.path.join(directory_path, "file_1.txt"),
            os.path.join(directory_path, "sub-directory", "sub_file.txt"),
            os.path.join(directory_path, "sub-directory", "sub-sub-directory", "sub_sub_file.txt"),
        ]

        os.makedirs(os.path.join(directory_path, "sub-directory", "sub-sub-directory"))

        # Create nested files in directory.
        for path, data in zip(paths, range(len(paths))):
            with open(path, "w") as f:
                f.write(str(data))

        return paths

    def test_instantiates_with_no_args(self):
        """Ensures a Datafile instantiates using only a path and generates a uuid ID"""
        Dataset()

    def test_instantiates_with_kwargs(self):
        """Ensures that keyword arguments can be used to construct the dataset initially"""
        files = [Datafile(path="path-within-dataset/a_test_file.csv")]
        resource = Dataset(files=files, labels="one two")
        self.assertEqual(len(resource.files), 1)

    def test_len(self):
        """Test that the length of a Dataset is the number of files it contains."""
        dataset = self.create_valid_dataset()
        self.assertEqual(len(dataset), len(dataset.files))

    def test_iter(self):
        """Test that iterating over a Dataset is equivalent to iterating over its files."""
        dataset = self.create_valid_dataset()
        iterated_files = {file for file in dataset}
        self.assertEqual(iterated_files, dataset.files)

    def test_add_single_file_to_empty_dataset(self):
        """Ensures that when a dataset is empty, it can be added to"""
        resource = Dataset()
        resource.add(Datafile(path="path-within-dataset/a_test_file.csv"))
        self.assertEqual(len(resource.files), 1)

    def test_add_single_file_to_existing_dataset(self):
        """Ensures that when a dataset is not empty, it can be added to"""
        files = [Datafile(path="path-within-dataset/a_test_file.csv")]
        resource = Dataset(files=files, labels="one two", tags={"a": "b"})
        resource.add(Datafile(path="path-within-dataset/a_test_file.csv"))
        self.assertEqual(len(resource.files), 2)

    def test_add_with_datafile_creation_shortcut(self):
        """Ensures that when a dataset is not empty, it can be added to"""
        resource = Dataset()
        resource.add(path="path-within-dataset/a_test_file.csv")
        self.assertEqual(len(resource.files), 1)

    def test_add_multiple_files(self):
        """Ensures that when a dataset is not empty, it can be added to"""
        files = [
            Datafile(path="path-within-dataset/a_test_file.csv"),
            Datafile(path="path-within-dataset/a_test_file.csv"),
        ]
        resource = Dataset()
        resource.add(*files)
        self.assertEqual(len(resource.files), 2)

    def test_cannot_add_non_datafiles(self):
        """Ensures that exception will be raised if adding a non-datafile object"""

        class NotADatafile:
            pass

        resource = Dataset()
        with self.assertRaises(exceptions.InvalidInputException) as e:
            resource.add(NotADatafile())

        self.assertIn("must be of class Datafile to add it to a Dataset", e.exception.args[0])

    def test_filter_catches_single_underscore_mistake(self):
        """Ensure that if the filter name contains only single underscores, an error is raised."""
        resource = Dataset(
            files=[
                Datafile(path="path-within-dataset/A_Test_file.csv"),
                Datafile(path="path-within-dataset/a_test_file.txt"),
            ]
        )

        with self.assertRaises(exceptions.InvalidInputException) as e:
            resource.files.filter(name_icontains="Test")

        self.assertIn("Invalid filter name 'name_icontains'. Filter names should be in the form", e.exception.args[0])

    def test_filter_name_contains(self):
        """Ensures that filter works with the name_contains and name_icontains lookups"""
        resource = Dataset(
            files=[
                Datafile(path="path-within-dataset/A_Test_file.csv"),
                Datafile(path="path-within-dataset/a_test_file.txt"),
            ]
        )
        files = resource.files.filter(name__icontains="Test")
        self.assertEqual(2, len(files))
        files = resource.files.filter(name__icontains="A")
        self.assertEqual(2, len(files))
        files = resource.files.filter(name__contains="Test")
        self.assertEqual(1, len(files))
        files = resource.files.filter(name__icontains="test")
        self.assertEqual(2, len(files))
        files = resource.files.filter(name__icontains="file")
        self.assertEqual(2, len(files))

    def test_filter_name_with(self):
        """Ensures that filter works with the name_endswith and name_startswith lookups"""
        resource = Dataset(
            files=[
                Datafile(path="path-within-dataset/a_my_file.csv"),
                Datafile(path="path-within-dataset/a_your_file.csv"),
            ]
        )
        files = resource.files.filter(name__starts_with="a_my")
        self.assertEqual(1, len(files))
        files = resource.files.filter(name__starts_with="a_your")
        self.assertEqual(1, len(files))
        files = resource.files.filter(name__starts_with="a_")
        self.assertEqual(2, len(files))
        files = resource.files.filter(name__starts_with="b")
        self.assertEqual(0, len(files))
        files = resource.files.filter(name__ends_with="_file.csv")
        self.assertEqual(2, len(files))
        files = resource.files.filter(name__ends_with="r_file.csv")
        self.assertEqual(1, len(files))
        files = resource.files.filter(name__ends_with="y_file.csv")
        self.assertEqual(1, len(files))
        files = resource.files.filter(name__ends_with="other.csv")
        self.assertEqual(0, len(files))

    def test_filter_by_label(self):
        """Ensures that filter works with label lookups"""
        resource = Dataset(
            files=[
                Datafile(path="path-within-dataset/a_my_file.csv", labels="one a2 b3 all"),
                Datafile(path="path-within-dataset/a_your_file.csv", labels="two a2 b3 all"),
                Datafile(path="path-within-dataset/a_your_file.csv", labels="three all"),
            ]
        )

        files = resource.files.filter(labels__contains="a")
        self.assertEqual(0, len(files))
        files = resource.files.filter(labels__contains="one")
        self.assertEqual(1, len(files))
        files = resource.files.filter(labels__contains="all")
        self.assertEqual(3, len(files))
        files = resource.files.filter(labels__any_label_starts_with="b")
        self.assertEqual(2, len(files))
        files = resource.files.filter(labels__any_label_ends_with="3")
        self.assertEqual(2, len(files))
        # files = resource.files.filter(labels__contains="hre")
        # self.assertEqual(1, len(files))

    def test_get_file_by_label(self):
        """Ensure files can be accessed by label from the dataset."""
        files = [
            Datafile(path="path-within-dataset/a_my_file.csv", labels="one a b3 all"),
            Datafile(path="path-within-dataset/a_your_file.csv", labels="two a2 b3 all"),
            Datafile(path="path-within-dataset/a_your_file.csv", labels="three all"),
        ]

        resource = Dataset(files=files)

        # Check working for single result
        self.assertIs(resource.get_file_by_label("three"), files[2])

        # Check raises for too many results
        with self.assertRaises(exceptions.UnexpectedNumberOfResultsException) as e:
            resource.get_file_by_label("all")

        self.assertIn("More than one result found", e.exception.args[0])

        # Check raises for no result
        with self.assertRaises(exceptions.UnexpectedNumberOfResultsException) as e:
            resource.get_file_by_label("billyjeanisnotmylover")

        self.assertIn("No results found for filters {'labels__contains': 'billyjeanisnotmylover'}", e.exception.args[0])

    def test_filter_name_filters_include_extension(self):
        """Ensures that filters applied to the name will catch terms in the extension"""
        files = [
            Datafile(path="path-within-dataset/a_test_file.csv"),
            Datafile(path="path-within-dataset/a_test_file.txt"),
        ]

        self.assertEqual(Dataset(files=files).files.filter(name__icontains="txt"), FilterSet({files[1]}))

    def test_filter_name_filters_exclude_path(self):
        """Ensures that filters applied to the name will not catch terms in the extension"""
        resource = Dataset(
            files=[
                Datafile(path="first-path-within-dataset/a_test_file.csv"),
                Datafile(path="second-path-within-dataset/a_test_file.txt"),
            ]
        )
        files = resource.files.filter(name__icontains="second")
        self.assertEqual(0, len(files))

    def test_hash_value(self):
        """Test hashing a dataset with multiple files gives a hash of length 8."""
        hash_ = self.create_valid_dataset().hash_value
        self.assertTrue(isinstance(hash_, str))
        self.assertTrue(len(hash_) == 8)

    def test_hashes_for_the_same_dataset_are_the_same(self):
        """Ensure the hashes for two datasets that are exactly the same are the same."""
        first_dataset = self.create_valid_dataset()
        second_dataset = copy.deepcopy(first_dataset)
        self.assertEqual(first_dataset.hash_value, second_dataset.hash_value)

    def test_serialise(self):
        """Test that a dataset can be serialised."""
        dataset = self.create_valid_dataset()
        self.assertEqual(len(dataset.to_primitive()["files"]), 2)

    def test_exists_in_cloud(self):
        """Test whether all files of a dataset are in the cloud or not can be determined."""
        self.assertFalse(self.create_valid_dataset().all_files_are_in_cloud)
        self.assertTrue(Dataset().all_files_are_in_cloud)

        files = [
            Datafile(path="gs://hello/file.txt", hypothetical=True),
            Datafile(path="gs://goodbye/file.csv", hypothetical=True),
        ]

        self.assertTrue(Dataset(files=files).all_files_are_in_cloud)

    def test_from_cloud(self):
        """Test that a Dataset in cloud storage can be accessed via (`bucket_name`, `output_directory`) and via
        `cloud_path`.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            dataset = create_dataset_with_two_files(temporary_directory)
            dataset.tags = {"a": "b", "c": 1}

            cloud_path = storage.path.generate_gs_path(TEST_BUCKET_NAME, "a_directory", dataset.name)
            dataset.to_cloud(cloud_path)
            persisted_dataset = Dataset.from_cloud(cloud_path)

            self.assertEqual(persisted_dataset.path, f"gs://{TEST_BUCKET_NAME}/a_directory/{dataset.name}")
            self.assertEqual(persisted_dataset.id, dataset.id)
            self.assertEqual(persisted_dataset.name, dataset.name)
            self.assertEqual(persisted_dataset.hash_value, dataset.hash_value)
            self.assertEqual(persisted_dataset.tags, dataset.tags)
            self.assertEqual(persisted_dataset.labels, dataset.labels)
            self.assertEqual({file.name for file in persisted_dataset.files}, {file.name for file in dataset.files})

            for file in persisted_dataset:
                self.assertEqual(file.path, f"gs://{TEST_BUCKET_NAME}/a_directory/{dataset.name}/{file.name}")

    def test_from_cloud_with_no_datafile_metadata_file(self):
        """Test that any cloud directory can be accessed as a dataset if it has no `dataset_metadata.json` metadata
        file in it, the cloud dataset doesn't lose any information during serialization, and a metadata file is
        uploaded afterwards.
        """
        cloud_storage_client = GoogleCloudStorageClient()

        cloud_storage_client.upload_from_string(
            "[1, 2, 3]",
            cloud_path=storage.path.generate_gs_path(TEST_BUCKET_NAME, "my_dataset", "file_0.txt"),
        )

        cloud_storage_client.upload_from_string(
            "[4, 5, 6]",
            cloud_path=storage.path.generate_gs_path(TEST_BUCKET_NAME, "my_dataset", "file_1.txt"),
        )

        cloud_dataset = Dataset.from_cloud(cloud_path=f"gs://{TEST_BUCKET_NAME}/my_dataset")

        self.assertEqual(cloud_dataset.path, f"gs://{TEST_BUCKET_NAME}/my_dataset")
        self.assertEqual(cloud_dataset.name, "my_dataset")
        self.assertEqual({file.name for file in cloud_dataset.files}, {"file_0.txt", "file_1.txt"})

        for file in cloud_dataset:
            self.assertEqual(file.path, f"gs://{TEST_BUCKET_NAME}/my_dataset/{file.name}")

        # Test serialisation doesn't lose any information.
        deserialised_dataset = Dataset.deserialise(cloud_dataset.to_primitive())
        self.assertEqual(deserialised_dataset.id, cloud_dataset.id)
        self.assertEqual(deserialised_dataset.name, cloud_dataset.name)
        self.assertEqual(deserialised_dataset.path, cloud_dataset.path)
        self.assertEqual(deserialised_dataset.hash_value, cloud_dataset.hash_value)

        # Test dataset metadata file has been uploaded.
        dataset_metadata = json.loads(
            cloud_storage_client.download_as_string(
                cloud_path=storage.path.join(cloud_dataset.path, definitions.DATASET_METADATA_FILENAME)
            )
        )
        del dataset_metadata["id"]

        self.assertEqual(
            dataset_metadata,
            {
                "files": [
                    "gs://octue-test-bucket/my_dataset/file_0.txt",
                    "gs://octue-test-bucket/my_dataset/file_1.txt",
                ],
                "labels": [],
                "name": "my_dataset",
                "tags": {},
            },
        )

    def test_from_cloud_with_nested_dataset_and_no_datafile_json_file(self):
        """Test that a nested dataset is loaded from the cloud correctly."""
        self._create_nested_cloud_dataset()

        cloud_dataset = Dataset.from_cloud(cloud_path=f"gs://{TEST_BUCKET_NAME}/a_dataset", recursive=True)

        self.assertEqual(cloud_dataset.path, f"gs://{TEST_BUCKET_NAME}/a_dataset")
        self.assertEqual(cloud_dataset.name, "a_dataset")
        self.assertEqual(
            {file.name for file in cloud_dataset.files},
            {"file_0.txt", "file_1.txt", "sub_file.txt", "sub_sub_file.txt"},
        )

        # Test dataset metadata file has been uploaded.
        dataset_metadata = json.loads(
            GoogleCloudStorageClient().download_as_string(
                cloud_path=storage.path.join(cloud_dataset.path, definitions.DATASET_METADATA_FILENAME)
            )
        )
        del dataset_metadata["id"]

        self.assertEqual(
            set(dataset_metadata["files"]),
            {
                "gs://octue-test-bucket/a_dataset/file_0.txt",
                "gs://octue-test-bucket/a_dataset/file_1.txt",
                "gs://octue-test-bucket/a_dataset/sub-directory/sub_file.txt",
                "gs://octue-test-bucket/a_dataset/sub-directory/sub-sub-directory/sub_sub_file.txt",
            },
        )

    def test_to_cloud(self):
        """Test that a dataset can be uploaded to a cloud path, including all its files and the dataset's metadata."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            dataset = create_dataset_with_two_files(temporary_directory)
            dataset.tags = {"a": "b", "c": 1}

            output_directory = "my_datasets"
            cloud_path = storage.path.generate_gs_path(TEST_BUCKET_NAME, output_directory, dataset.name)
            dataset.to_cloud(cloud_path)

            storage_client = GoogleCloudStorageClient()

            # Check its files have been uploaded.
            persisted_file_0 = storage_client.download_as_string(storage.path.join(cloud_path, "file_0.txt"))
            self.assertEqual(persisted_file_0, "0")

            persisted_file_1 = storage_client.download_as_string(storage.path.join(cloud_path, "file_1.txt"))
            self.assertEqual(persisted_file_1, "1")

            # Check its metadata has been uploaded.
            persisted_dataset_metadata = json.loads(
                storage_client.download_as_string(storage.path.join(cloud_path, definitions.DATASET_METADATA_FILENAME))
            )

            self.assertEqual(
                persisted_dataset_metadata["files"],
                [
                    f"gs://octue-test-bucket/my_datasets/{dataset.name}/file_0.txt",
                    f"gs://octue-test-bucket/my_datasets/{dataset.name}/file_1.txt",
                ],
            )

            self.assertEqual(persisted_dataset_metadata["tags"], dataset.tags.to_primitive())

    def test_to_cloud_with_nested_dataset_preserves_nested_structure(self):
        """Test that uploading a dataset containing datafiles in a nested directory structure to the cloud preserves
        this structure in the cloud.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            local_paths = self._create_files_and_nested_subdirectories(temporary_directory)
            dataset = Dataset.from_local_directory(temporary_directory, recursive=True)

            upload_path = storage.path.generate_gs_path(TEST_BUCKET_NAME, "my-dataset")
            dataset.to_cloud(cloud_path=upload_path)

        uploaded_dataset = Dataset.from_cloud(cloud_path=upload_path)

        # Check that the paths relative to the dataset directory are the same in the cloud as they are locally.
        local_datafile_relative_paths = {
            path.split(temporary_directory)[-1].strip(os.path.sep).replace(os.path.sep, "/") for path in local_paths
        }

        cloud_datafile_relative_paths = {
            storage.path.split_bucket_name_from_gs_path(datafile.path)[-1].split("my-dataset/")[-1]
            for datafile in uploaded_dataset.files
        }

        self.assertEqual(cloud_datafile_relative_paths, local_datafile_relative_paths)

    def test_download_all_files(self):
        """Test that all files in a dataset can be downloaded with one command."""
        storage_client = GoogleCloudStorageClient()

        dataset_name = "another-dataset"
        storage_client.upload_from_string(
            string=json.dumps([1, 2, 3]),
            cloud_path=storage.path.generate_gs_path(TEST_BUCKET_NAME, dataset_name, "file_0.txt"),
        )
        storage_client.upload_from_string(
            string=json.dumps([4, 5, 6]),
            cloud_path=storage.path.generate_gs_path(TEST_BUCKET_NAME, dataset_name, "file_1.txt"),
        )

        dataset = Dataset.from_cloud(cloud_path=f"gs://{TEST_BUCKET_NAME}/{dataset_name}")

        with tempfile.TemporaryDirectory() as temporary_directory:
            dataset.download_all_files(local_directory=temporary_directory)

            with open(os.path.join(temporary_directory, "file_0.txt")) as f:
                self.assertEqual(f.read(), "[1, 2, 3]")

            with open(os.path.join(temporary_directory, "file_1.txt")) as f:
                self.assertEqual(f.read(), "[4, 5, 6]")

    def test_download_all_files_from_nested_dataset(self):
        """Test that all files in a nested dataset can be downloaded with one command."""
        self._create_nested_cloud_dataset("nested_dataset")

        dataset = Dataset.from_cloud(cloud_path=f"gs://{TEST_BUCKET_NAME}/nested_dataset", recursive=True)

        with tempfile.TemporaryDirectory() as temporary_directory:
            dataset.download_all_files(local_directory=temporary_directory)

            with open(os.path.join(temporary_directory, "file_0.txt")) as f:
                self.assertEqual(f.read(), "[1, 2, 3]")

            with open(os.path.join(temporary_directory, "file_1.txt")) as f:
                self.assertEqual(f.read(), "[4, 5, 6]")

            with open(os.path.join(temporary_directory, "sub-directory", "sub_file.txt")) as f:
                self.assertEqual(f.read(), "['a', 'b', 'c']")

            with open(os.path.join(temporary_directory, "sub-directory", "sub-sub-directory", "sub_sub_file.txt")) as f:
                self.assertEqual(f.read(), "['blah', 'b', 'c']")

    def test_download_all_files_from_nested_dataset_with_no_local_directory_given(self):
        """Test that, when downloading all files from a nested dataset and no local directory is given, the dataset
        structure is preserved in the temporary directory used.
        """
        self._create_nested_cloud_dataset("nested_dataset")

        dataset = Dataset.from_cloud(f"gs://{TEST_BUCKET_NAME}/nested_dataset", recursive=True)

        # Mock the temporary directory created in `Dataset.download_all_files` so we can access it for the test.
        temporary_directory = tempfile.TemporaryDirectory()

        with patch("tempfile.TemporaryDirectory", return_value=temporary_directory):
            dataset.download_all_files()

        with open(os.path.join(temporary_directory.name, "file_0.txt")) as f:
            self.assertEqual(f.read(), "[1, 2, 3]")

        with open(os.path.join(temporary_directory.name, "file_1.txt")) as f:
            self.assertEqual(f.read(), "[4, 5, 6]")

        with open(os.path.join(temporary_directory.name, "sub-directory", "sub_file.txt")) as f:
            self.assertEqual(f.read(), "['a', 'b', 'c']")

        with open(
            os.path.join(temporary_directory.name, "sub-directory", "sub-sub-directory", "sub_sub_file.txt")
        ) as f:
            self.assertEqual(f.read(), "['blah', 'b', 'c']")

    def test_from_local_directory(self):
        """Test that a dataset can be instantiated from a local nested directory ignoring its subdirectories and that
        extra keyword arguments can be provided for the dataset instantiation.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            paths = self._create_files_and_nested_subdirectories(temporary_directory)
            dataset = Dataset.from_local_directory(temporary_directory, recursive=False, name="my-dataset")
            self.assertEqual(dataset.name, "my-dataset")

            # Check that just the top-level files from the directory are present in the dataset.
            datafile_paths = {datafile.path for datafile in dataset.files}
            self.assertEqual(datafile_paths, set(paths[:2]))

    def test_from_local_directory_recursively(self):
        """Test that a dataset can be instantiated from a local nested directory including its subdirectories."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            paths = self._create_files_and_nested_subdirectories(temporary_directory)
            dataset = Dataset.from_local_directory(temporary_directory, recursive=True)

            # Check that all the files from the directory are present in the dataset.
            datafile_paths = {datafile.path for datafile in dataset.files}
            self.assertEqual(datafile_paths, set(paths))
