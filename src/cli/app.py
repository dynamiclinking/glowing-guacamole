import time


class SearchApp:
    def __init__(self, engine, logger=None):
        self.engine = engine
        self.logger = logger

    def print_results(self, results):
        print("\n━━━━━━━━━━━━━━━━━━━━━━")
        print("RESULTS")
        print("━━━━━━━━━━━━━━━━━━━━━━\n")

        for i, r in enumerate(results, 1):
            print(f"[{i}] {r.doc_id}")
            print(f"    {r.chunk_id}")
            print(f"    {r.text[:200]}\n")

    def run(self):
        print("🧠 Semantic Search Ready (type 'exit' to quit)\n")

        while True:
            query = input("> ")

            if query.strip().lower() == "exit":
                break

            start = time.perf_counter()
            results = self.engine.search(query)
            latency = time.perf_counter() - start

            print(f"\n⏱ {latency:.3f}s")

            self.print_results(results)

            selected = input("Select relevant (comma-separated, Enter skip): ")

            selected_ids = []
            if selected.strip():
                try:
                    idxs = [int(x) - 1 for x in selected.split(",")]
                    for i in idxs:
                        if 0 <= i < len(results):
                            selected_ids.append(results[i].chunk_id)
                except ValueError:
                    pass

            if self.logger:
                self.logger.log_query(query, results, selected_ids)
