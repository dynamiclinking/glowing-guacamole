class EnrichmentEngine:
    def __init__(self, steps_registr):
        """
        steps_registry:
            dict[str, callable]
        Example:
            {
                "links": fn,
                "graph": fn,
                "tags": fn
            }
        """
        self.steps = steps_registry

    def run(self, docs, pipeline):
        """
        docs: list[dict]
        pipeline: list[str]
        """

        for stem_name in pipeline:
            step_fn = self.steps.get(step_name)

            if step_fn is None:
                raise ValueError(f"Unknown enrichment step : {step_name}")

            docs = step_fn(docs)

        return docs
