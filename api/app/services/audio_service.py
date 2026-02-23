import hashlib
import random

from app.models.audio import AudioOptimizeResult, AudioSyncResult


async def analyze_sync(
    feed_paths: list[str], feed_ids: list[str]
) -> list[AudioSyncResult]:
    """Placeholder audio sync analysis – returns deterministic mock offsets."""
    results: list[AudioSyncResult] = []
    for path, fid in zip(feed_paths, feed_ids):
        # Deterministic pseudo-random offset based on the path
        seed = int(hashlib.md5(path.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed)
        offset = round(rng.uniform(-0.5, 0.5), 4)
        confidence = round(rng.uniform(0.7, 1.0), 4)
        results.append(
            AudioSyncResult(
                feed_id=fid,
                detected_offset_seconds=offset,
                confidence=confidence,
            )
        )
    return results


async def optimize_audio(
    feed_paths: list[str],
    master_path: str,
    normalize: bool = True,
    noise_reduce: bool = False,
) -> AudioOptimizeResult:
    """Placeholder audio optimization – returns mock result for MVP."""
    return AudioOptimizeResult(
        output_path="/data/output/optimized_mix.wav",
        settings_applied={
            "normalize": normalize,
            "noise_reduce": noise_reduce,
            "master": master_path,
            "input_count": len(feed_paths),
        },
    )
