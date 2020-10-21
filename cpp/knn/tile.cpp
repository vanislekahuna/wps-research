#include"../misc.h" // tiler for ML app
size_t nrow, ncol, nband, np;

int main(int argc, char ** argv){
  if(argc < 4) err("tile [input envi-type4 floating point stack bsq with gr] [# of groundref classes at end] [patch size]\n");

  int ps, nref;
  str bfn(argv[1]);
  str hfn(hdr_fn(bfn));
  hread(hfn, nrow, ncol, nband);
  printf("nrow %zu ncol %zu nband %zu\n", nrow, ncol, nband);

  float * dat = bread(bfn, nrow, ncol, nband); // read input data
  np = nrow * ncol;
  ps = atoi(argv[3]); // patch size
  nref = atoi(argv[2]); // number of groundref classes one-hot encoded

  size_t i, j, m, n;
  if(ps >= nrow || ps >= ncol) err("patch size too big");
  if(nref >= nband) err("check number of groundref bands");

  unsigned int di, dj, k, ci;
  unsigned int nb = nband - nref;
  unsigned int floats_per_patch = ps * ps * nb;
  float * patch = falloc(sizeof(float) * floats_per_patch);

  FILE * f_patch = wopen("patches.dat");

  map<float, size_t> count; // count labels on a patch

  for(i = 0; i < nrow - ps; i += ps){
    // start row for patch
    for(j = 0; j < ncol - ps; j += ps){
      // start col for patch
      ci = 0;
      for0(di, ps){
        m = i + di;
        for0(dj, ps){
          n = j + dj;
          for0(k, nb){
            patch[ci ++] = dat[(k * nrow * ncol) + (m * ncol) + n];
          }
        }
      }
      if(ci != ps * ps * nb) err("patch element count mismatch");
      // don't forget to calculate class for patch, by majority
      //
      count.clear();
      for0(di, ps){
        m = (i + di) * ncol;
        for0(dj, ps){
          n = j + dj + m;
          for0(k, nref){
            // histogram: mass for each label
            float key = dat[((k + nb) * np) + n];
            if(count.count(key) < 1) count[key] = 0;
            count[key] += 1;
          }
        }
      }
      float max_key = -1.;
      size_t max_count = 0;
      map<float, size_t>::iterator it; // lazy match
      for(it = count.begin(); it != count.end(); it++){
        if(it->second > max_count){
          max_count = it->second;
          max_key = it->first;
        }
      }
      size_t n_match = 0;
      for(it = count.begin(); it != count.end(); it++) if(it->second == max_count) n_match ++;

      if(n_match > 1){
        printf("\tWarning: patch had competing classes\n");
      }

      fwrite(patch, sizeof(float), floats_per_patch, f_patch);
    }
  }

  // patch label
  // patch i, patch j
  // patch start coord i, j (patch i, j * ps)
  // patch centre coord i, j
  // patch data

  fclose(f_patch);
  free(patch);
  return 0;
}