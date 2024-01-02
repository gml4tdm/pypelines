import pickle
import typing

import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

import checkpointed_core
from checkpointed_core import PipelineStep
from checkpointed_core.arg_spec import constraints, arguments

from ... import bases


class RemoveStopwords(checkpointed_core.PipelineStep, bases.TokenizedDocumentSource):

    @classmethod
    def supports_step_as_input(cls, step: type[PipelineStep], label: str) -> bool:
        if label == 'documents':
            return issubclass(step, bases.TokenizedDocumentSource)
        return super(cls, cls).supports_step_as_input(step, label)

    async def execute(self, **inputs) -> typing.Any:
        stopwords = set(nltk.corpus.stopwords.words('english'))
        documents = inputs['documents']
        return [
            [[word for word in sent if word not in stopwords] for sent in document]
            for document in documents
        ]

    @staticmethod
    def save_result(path: str, result: typing.Any):
        with open(path, 'wb') as file:
            pickle.dump(result, file)

    @staticmethod
    def load_result(path: str):
        with open(path, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def is_deterministic() -> bool:
        return True

    def get_checkpoint_metadata(self) -> typing.Any:
        return {}

    def checkpoint_is_valid(self, metadata: typing.Any) -> bool:
        return True

    @classmethod
    def get_arguments(cls) -> dict[str, arguments.Argument]:
        return {}

    @classmethod
    def get_constraints(cls) -> list[constraints.Constraint]:
        return []
