/* patch.cpp: tiling processing to feed into an ML-type code
   - cut image data (and ground reference data) into small patches (nonoverlapping at this point)
   - use majority voting scheme to assign label to each patch
   - if patches are too large relative to the homogeneous areas of a patch, results will suffer

Assume this is the portion of the data to fit the "model" on: kinda the image data input here "is" the model..

*/
#include"../misc.h"
size_t nrow, ncol, nband, np; // image attributes

void accumulate(map<float, size_t> &m, float key){
  if(m.count(key) < 1) m[key] = 0;
  m[key] += 1; // histogram on $\mathbb{R}^1
}

// could add "stride" parameter later (increase patches towards moving window)
int main(int argc, char ** argv){
  if(argc < 4) err("patch [input envi-type4 floating point stack bsq with gr] [# of groundref classes at end] [patch size]\n");

  str bfn(argv[1]);
  str hfn(hdr_fn(bfn));
  size_t ps, nref;
  hread(hfn, nrow, ncol, nband);
  printf("nrow %zu ncol %zu nband %zu\n", nrow, ncol, nband);

  float * dat = bread(bfn, nrow, ncol, nband); // read input data
  np = nrow * ncol; // number of pixels
  ps = atoi(argv[3]); // patch width / length: square patch
  nref = atoi(argv[2]); // number of groundref classes one-hot encoded

  size_t i, j, m, n;
  if(ps >= nrow || ps >= ncol) err("patch size too big");
  if(nref >= nband) err("check number of groundref bands");

  size_t di, dj, k, ci;
  size_t nb = nband - nref; // image data bands: total image bands, less # of ref bands
  size_t floats_per_patch = ps * ps * nb; // floats per patch (image data)
  float * patch = falloc(sizeof(float) * floats_per_patch);

  FILE * f_ps = wopen((bfn + str("_ps")).c_str()); // patch size
  fwrite(&ps, sizeof(size_t), 1, f_ps);
  fclose(f_ps);

  FILE * f_patch = wopen((bfn + str("_patch")).c_str()); // patch data
  FILE * f_patch_i = wopen((bfn + str("_patch_i")).c_str()); // start row for patch 
  FILE * f_patch_j = wopen((bfn + str("_patch_j")).c_str()); // start col for patch
  FILE * f_patch_label = wopen((bfn + str("_patch_label")).c_str()); // patch label

  size_t truthed = 0;
  size_t nontruthed = 0;
  map<float, size_t> count; // count labels on a patch

  // band-interleave-by-pixel, by patch!
  for(i = 0; i <= nrow - (nrow % ps + ps); i += ps){
    // start row for patch (stride parameter would be the step for this loop)
    for(j = 0; j <=  ncol - (ncol % ps + ps); j += ps){
      ci = 0; // j is start col for patch

      for0(di, ps){
        m = i + di;
        for0(dj, ps){
          n = j + dj; // extract data on a patch (left->right to linear order)
          for0(k, nb) patch[ci ++] = dat[(k * nrow * ncol) + (m * ncol) + n];
        }
      }
      if(ci != ps * ps * nb) err("patch element count mismatch");

      // count labels on each patch
      count.clear(); // mass for each label on the patch
      for0(di, ps){
        m = (i + di) * ncol; 

        for0(dj, ps){
          n = (j + dj) + m;
          int no_match = true;

          for0(k, nref){
            if(dat[((k + nb) * np) + n] == 1.){
              no_match = false;
              accumulate(count, k + 1);
            }
          }
          if(no_match) accumulate(count, 0); // default to 0 / null label
        }
      }

      float max_k = 0.;
      size_t max_c = 0;
      map<float, size_t>::iterator it; // lazy match
      for(it = count.begin(); it != count.end(); it++){
        if(it->first > 0 && it->second > max_c){
          max_c = it->second; // no leading class: doesn't count
          max_k = it->first;
        }
      }

      size_t n_match = 0;
      for(it = count.begin(); it != count.end(); it++) if(it->second == max_c) n_match ++;

      if(max_c > 0){
        truthed ++;
        cout << count << " max_c " << max_c << endl;
        if(n_match > 1) printf("\tWarning: patch had competing classes\n");
      }
      else nontruthed ++;

      fwrite(&i, sizeof(size_t), 1, f_patch_i);
      fwrite(&j, sizeof(size_t), 1, f_patch_j);
      fwrite(&max_k, sizeof(float), 1, f_patch_label);
      fwrite(patch, sizeof(float), floats_per_patch, f_patch);
    }
  }
  printf("\n");
  printf(" nwin: %zu\n", (size_t)ps);
  printf(" image pixels: %zu\n", np);
  printf(" pix per patch: %zu\n",(size_t)(ps * ps));
  printf(" est. patches:%zu\n", np / (ps * ps));
  printf(" total patches: %zu\n", truthed + nontruthed);
  printf(" truthed: %zu\t\t[%.2f / 100]\n", truthed, 100. * (float)(truthed) / ((float)(truthed + nontruthed)));
  printf(" nontruthed: %zu\n", nontruthed);

  fclose(f_patch); // patch data
  fclose(f_patch_i); // patch start i
  fclose(f_patch_j); // patch start j
  fclose(f_patch_label); // patch label
  free(patch);
  return 0;
}
