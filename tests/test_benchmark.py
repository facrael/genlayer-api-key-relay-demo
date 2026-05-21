from benchmarks.api_consistency_benchmark import build_report, load_offline_samples


def test_offline_benchmark_produces_consistency_report():
    responses, latencies = load_offline_samples()
    report = build_report(responses, latencies)
    assert report["sample_count"] == 5
    assert report["consistency_score"] >= 0.75
    assert report["recommended_cache_window_seconds"] >= 60
    assert report["latency_ms"]["average"] > 0
