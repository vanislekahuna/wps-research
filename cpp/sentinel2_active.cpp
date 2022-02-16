#include"misc.h"
int main(int argc, char ** argv){

  if(argc < 2) err("sentinel2_active.exe [input file name]");
  str fn(argv[1]); /* binary files */
  str ofn(fn + "_active.bin");
  str hfn(hdr_fn(fn));  /* headers */
  str hf2(hdr_fn(ofn, true));

  size_t nrow, ncol, nband, np, i, j, k, n, ij;
  vector<string> s, t;
  t.push_back(str("945n"));
  t.push_back(str("1610n"));
  t.push_back(str("2190n"));
  hread(hfn, nrow, ncol, nband, s);
  np = nrow * ncol;
  n = s.size();
  long int bi[3] = {-1, -1, -1};
  for0(i, n) for0(j, 3) if(contains(s[i], t[j])) bi[j] = i * np;
  float * dat = bread(fn, nrow, ncol, nband);
  float * out = falloc(np);
  
  for0(ij, np) out[ij] = dat[ij + bi[2]] - dat[ij + bi[1]] > 175.;
  bwrite(out, ofn, nrow, ncol, 1);
  hwrite(hf2, nrow, ncol, 1);

  free(dat); /* would be nice to plot spectra */
  free(out);
  return 0;
}
