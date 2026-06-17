import csv
import random
from collections import defaultdict
from pathlib import Path

SAMPLE_SEED = 42
SAMPLE_SIZE = 5620

RAW_DIR = Path(__file__).parent / "raw"
OUT_DIR = Path(__file__).parent


def stratified_sample(rows, header, target_idx, sample_size, seed):
    by_class = defaultdict(list)
    for row in rows:
        by_class[row[target_idx]].append(row)

    total = len(rows)
    rng = random.Random(seed)

    counts = {cls: max(1, round(sample_size * len(items) / total)) for cls, items in by_class.items()}
    diff = sample_size - sum(counts.values())
    classes_sorted = sorted(by_class.keys(), key=lambda c: len(by_class[c]), reverse=True)
    i = 0
    while diff != 0 and classes_sorted:
        cls = classes_sorted[i % len(classes_sorted)]
        if diff > 0:
            counts[cls] += 1
            diff -= 1
        elif counts[cls] > 1:
            counts[cls] -= 1
            diff += 1
        i += 1

    sampled = []
    for cls, items in by_class.items():
        n = min(counts[cls], len(items))
        sampled.extend(rng.sample(items, n))
    rng.shuffle(sampled)
    return sampled


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def prepare_covtype():
    src = RAW_DIR / "covtype.csv"
    with open(src, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    target_idx = header.index("Cover_Type")
    sampled = stratified_sample(rows, header, target_idx, SAMPLE_SIZE, SAMPLE_SEED)

    out_path = OUT_DIR / "covtype_sample.csv"
    write_csv(out_path, header, sampled)

    dist = defaultdict(int)
    for row in sampled:
        dist[row[target_idx]] += 1
    print(f"covtype_sample.csv: {len(sampled)} linhas, distribuicao Cover_Type: {dict(sorted(dist.items()))}")


def prepare_weather():
    src = RAW_DIR / "weatherAUS.csv"
    with open(src, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    date_idx = header.index("Date")
    new_header = [h for i, h in enumerate(header) if i != date_idx]

    complete_rows = []
    for row in rows:
        if any(value == "NA" or value == "" for value in row):
            continue
        complete_rows.append([v for i, v in enumerate(row) if i != date_idx])

    target_idx = new_header.index("RainTomorrow")
    sampled = stratified_sample(complete_rows, new_header, target_idx, SAMPLE_SIZE, SAMPLE_SEED)

    out_path = OUT_DIR / "weatherAUS_sample.csv"
    write_csv(out_path, new_header, sampled)

    dist = defaultdict(int)
    for row in sampled:
        dist[row[target_idx]] += 1
    print(f"weatherAUS_sample.csv: {len(sampled)} linhas (pool completo: {len(complete_rows)}), distribuicao RainTomorrow: {dict(sorted(dist.items()))}")


if __name__ == "__main__":
    prepare_covtype()
    prepare_weather()
