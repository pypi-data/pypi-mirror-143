from ml.ml40.features.properties.values.documents.reports.report import Report


class LogMeasurement(Report):
    def __init__(self, namespace="fml40", name="", identifier=""):
        super().__init__(namespace=namespace, name=name, identifier=identifier)
