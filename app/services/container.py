class ServiceContainer:
    _instance = None
    
    def __init__(self):
        self.document_processor = None
        self.embedding_service = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ServiceContainer()
        return cls._instance
    
    @classmethod
    def initialize(cls, document_processor, embedding_service):
        instance = cls.get_instance()
        instance.document_processor = document_processor
        instance.embedding_service = embedding_service
