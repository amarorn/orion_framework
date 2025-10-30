from ...core.usecases.RunPipelineUseCase import RunPipelineUseCase

class PipelineRunner:
    def run(self, pipeline, context):
        uc = RunPipelineUseCase(pipeline, context)
        return uc.execute()
