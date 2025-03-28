from typing import List, Dict, Any


class Knowledge:
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents

    def add_document(self, document: Dict[str, Any]) -> None:
        self.documents.append(document)

    def remove_document(self, document_id: str) -> None:
        self.documents = [doc for doc in self.documents if doc["id"] != document_id]
