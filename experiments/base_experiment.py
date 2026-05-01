class BaseExperiment:
    def run(self, target):
        raise NotImplementedError("Each experiment must implement run()")