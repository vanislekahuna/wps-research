/* 20240605 split a class map into one file per class
*/
#include"misc.h"
int main(int argc, char ** argv){
  if(argc < 2) err("class_split [input binary (classification) file name]");

  str fn(argv[1]); // input file name
  str hfn(hdr_fn(fn)); // auto-detect header file name
  size_t nrow, ncol, nband, np, i, j;
  hread(hfn, nrow, ncol, nband); // read header

  np = nrow * ncol;
  if(nband != 1) err("this program defines results for 1-band images");

  float * dat = bread(fn, nrow, ncol, nband); // read data into array
  float * out = falloc(nrow * ncol);
  float * is_nan = falloc(nrow * ncol);

  for0(i, np){ 
    dat[i] = 0.;
    out[i] = 0;
    is_nan[i] = 0.;
  }

  map<float, size_t> count; // accumulate the data
  for0(i, np){
    float d = dat[i];

    if(isnan(d) || isinf(d)){
      is_nan[i] = 1.;
    }
    else{
      if(count.count(d) < 1) count[d] = 0;
      count[d] += 1;
    }
  }
  
  cout << count << endl;
  
  for(map<float, size_t>::iterator it = count.begin(); it != count.end(); it++){
    float w = it->first;
    for0(i, np){
      float d = dat[i];
      if(w == d) out[i] = 1.;
      else out[i] = 0.;
    } 
    bwrite(out, fn + str("_") + std::to_string(w) + str(".bin"), nrow, ncol, 1);
    hwrite(fn + str("_") + std::to_string(w) + str(".hdr"), nrow, ncol, 1);
  }
 
  bwrite(is_nan,  fn + str("_NAN.bin"), nrow, ncol, 1);
  hwrite( fn + str("_NAN.bin"), nrow, ncol, 1);
  free(dat);
  free(out);
  free(is_nan);
  return 0;
}
