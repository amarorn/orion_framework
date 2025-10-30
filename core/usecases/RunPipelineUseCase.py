from ..entities.pipeline import Pipeline

class RunPipelineUseCase:
    def __init__(self, pipeline: Pipeline, context):
        self.pipeline = pipeline
        self.context = context

    def execute(self):
        return self.pipeline.run(self.context)
