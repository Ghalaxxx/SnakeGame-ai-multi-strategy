class AlgorithmPerformanceTracker:
    def __init__(self):
        self.results = {}  # {mode: [(score, time), ...]}

    def record(self, mode, score, time_sec):
        if mode not in self.results:
            self.results[mode] = []
        self.results[mode].append((score, time_sec))

    def get_summary(self):
        summary = {}
        for mode, runs in self.results.items():
            total_score = sum(s for s, _ in runs)
            total_time = sum(t for _, t in runs)
            avg_score = total_score / len(runs)
            avg_time = total_time / len(runs)
            summary[mode] = {
                "avg_score": round(avg_score, 2),
                "avg_time": round(avg_time, 2),
                "runs": len(runs)
            }
        return summary

    def print_summary(self):
        summary = self.get_summary()
        if not summary:
            print("No data recorded yet.")
            return

        print("\n Game Performance Summary:\n")
        for mode, data in summary.items():
            print(f"{mode.upper()} | Avg Score: {data['avg_score']} | Avg Time: {data['avg_time']}s | Runs: {data['runs']}")

        best_score_mode = max(summary.items(), key=lambda x: x[1]['avg_score'])[0]
        best_time_mode = min(summary.items(), key=lambda x: x[1]['avg_time'])[0]

        print("\n Analysis:")
        print(f" Best at scoring: {best_score_mode.upper()} → Collected more food on average.")
        print(f" Fastest decision-making: {best_time_mode.upper()} → Survived with faster paths.")
        print("\n" + "-" * 40 + "\n")

    
    def get_best_run(self, mode):
        if mode not in self.results:
            return None
        return max(self.results[mode], key=lambda x: x[0])  # based on score
