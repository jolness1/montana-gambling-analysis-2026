import csv
import os
import sys

INPUT_REVENUE = os.path.join('input-data', 'video-gambling-revenue-per-machine-FY1993-2022.csv')
INPUT_TAX = os.path.join('input-data', 'tax-revenue-montana-video gambling-FY-1992-2026.csv')
OUT_DIR = 'output'
OUT_FILE = os.path.join(OUT_DIR, 'tax-per-year.csv')


def to_int(value):
    if value is None:
        return None
    s = str(value).strip()
    if s == '':
        return None
    try:
        return int(float(s))
    except Exception:
        return None


def read_csv_map(path, year_key, value_key):
    m = {}
    with open(path, newline='') as fh:
        rdr = csv.DictReader(fh)
        for row in rdr:
            # normalize keys by stripping
            year = None
            for k in row:
                if k.strip() == year_key:
                    year = row[k]
                    break
            val = None
            for k in row:
                if k.strip() == value_key:
                    val = row[k]
                    break
            if year is None:
                continue
            year = str(year).strip()
            if year == '':
                continue
            v = to_int(val)
            if v is None:
                continue
            m[year] = v
    return m


def main():
    rev_map = read_csv_map(INPUT_REVENUE, 'Fiscal Year', 'Total Annual Gross Income')
    tax_map = read_csv_map(INPUT_TAX, 'Fiscal Year', 'Total')

    years = sorted(int(y) for y in (set(rev_map.keys()) & set(tax_map.keys())))
    if not years:
        print('No overlapping years found between inputs.', file=sys.stderr)
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_FILE, 'w', newline='') as outfh:
        writer = csv.writer(outfh)
        writer.writerow(['fiscalYear', 'taxes', 'totalRevenue', 'pct'])
        written = 0
        for y in years:
            ys = str(y)
            taxes = tax_map.get(ys)
            total = rev_map.get(ys)
            if taxes is None or total is None or total == 0:
                continue
            pct = int(round(taxes / total * 100))
            writer.writerow([ys, taxes, total, pct])
            written += 1

    print(f'Wrote {OUT_FILE} with {written} rows.')


if __name__ == '__main__':
    main()
