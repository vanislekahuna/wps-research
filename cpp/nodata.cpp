/* find out where a stack, assumed ENVI type-4 32-bit IEEE standard
* floating-point format, BSQ interleave, is "no data" i.e. all bands exactly 0 */
#include"misc.h"

int main(int argc, char ** argv){
  if(argc < 2) err("nodata [input binary file name]");

  str fn(argv[1]); // input file name
  str hfn(hdr_fn(fn)); // auto-detect header file name
  size_t nrow, ncol, nband, np, i, j, k;
  hread(hfn, nrow, ncol, nband); // read header
  np = nrow * ncol; // number of input pix

  float * dat = bread(fn, nrow, ncol, nband); // load floats to array

  float * dat2 = (float *) falloc(np);
  for0(i, np) dat2[i] = 0.; // set to zero

  for0(i, nrow){
    size_t ix = i * ncol;
    for0(j, ncol){
      int nz = 0;
      size_t ijx = ix + j;
      for0(k, nband){
        if(dat[(k * np) + ijx] == 0.){
          nz ++;
        }
      }
      if(nz == nband){
        dat2[ijx] = 1.;
      }
    }
  }

  // write output file
  str ofn(fn + str("_nodata.bin"));
  str ohfn(fn + str("_nodata.hdr"));
  hwrite(ohfn, nrow, ncol, 1); // write output header

  FILE * f = fopen(ofn.c_str(), "wb");
  if(!f) err("failed to open output file");
  fwrite(&dat2[0], sizeof(float), np, f); // write data

  fclose(f);
  free(dat);
  free(dat2);
  return 0;
}