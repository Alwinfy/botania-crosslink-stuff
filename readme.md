# Usage
## Prereq
You'll need a standard Python3 install, jq, and GNU find. ~~I wrote these on Linux ok dont judge my tools~~
## "Installation"
Copy both scripts to the root of the Botania repo. It's easiest to do the work there.
## gen-mappings.sh
Run this with the lang you want to setup (`en_us`, `ru_ru`, etc.), as in This should create a `mappings_$lang.json` in the cwd, which is what you need to edit.
## `mappings*.json` structure
The things you want to fiddle with are:
 - `names`, which should have as keys human-readable phrases (that are wrapped in Patchouli item & 0 tags) that will get wrapped in links. Their corresponding values are the entries to link to, in the Botania lang file.
 - `ignore`, for all the aforementioned phrases that shouldn't get links at all.
See `sample/` for the final mappings I used for `en_us`.
## convert.py
Run this as `convert.py <mappingsfile> <output file>.` This should also dump to your screen a list of errors to be corrected, and unmapped phrases that are candidates for linking. Add them to `names` or `ignore` in your mappingsfile, as described above. Also, probably don't output to the original lang file unless you're *sure* sure that you're done with generating links.
# Why?
I'm sorry.
