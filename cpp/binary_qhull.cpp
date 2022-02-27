/* list points where a float mask is equal to 1. as input to qhull */
#include"misc.h"
int main(int argc, char ** argv){
  if(argc < 2) err("binary_list [input binary class file name]");

  float d;
  str fn(argv[1]); // input file name
  str hfn(hdr_fn(fn)); // auto-detect header file name
  size_t nrow, ncol, nband, np, i, j;
  hread(hfn, nrow, ncol, nband); // read header

  np = nrow * ncol;
  if(nband != 1) err("this program defines results for 1-band images");

  // read data into float array
  float * dat = bread(fn, nrow, ncol, nband);

  ofstream of; 
  of.open("qhull.dat");

  str s(" ");
  size_t n = 0;

  for0(i, nrow){
    for0(j, ncol){
      if(dat[i * ncol + j] == 1.) n++;
    }
  }

  of << to_string(2) << s << to_string(n) << s;
  for0(i, nrow){
    for0(j, ncol){
      if(dat[i * ncol + j] == 1.){
        of << i << s << j << s;
      }
    }
  }

  of << endl;
  of.close();

  str r(exec("qhull -i < qhull.dat"));
  strip(r);
  vector<str> lines(split(r, '\n'));
  cout << "[" << r << "]" << endl;

  cout << lines << endl;

  int n_pts = atoi(lines[0].c_str());
  cout << lines.size() << endl;
  if(n_pts != lines.size() - 1) err("unexpected number of output lines");
  
  for0(i, n_pts){
    vector<str> x(split(lines[i+1], ' '));
    cout << s << s << x << endl;
    if(len(x) != 2) err("unexpected number of records");
  }


  return 0;
}