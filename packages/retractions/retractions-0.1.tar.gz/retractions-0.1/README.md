# retractions

Check DOIs for retractions

## Usage

```_retractions
usage: retractions [-h] [-r] [-b {openretractions}] [-i INFILE] [-o OUTFILE]
                   [-u]
                   [doi ...]

positional arguments:
  doi                   DOI to check for retractions or updates. Handled after
                        --infile lists.

optional arguments:
  -h, --help            show this help message and exit
  -r, --retractions-only
                        Only list retracted DOIs, not updated
  -b {openretractions}, --backend {openretractions}
  -i INFILE, --infile INFILE
                        Get DOIs from file (newline-separated); accepts
                        multiple
  -o OUTFILE, --outfile OUTFILE
                        Write to file instead of stdout
  -u, --url             Show DOIs as URLs
```
