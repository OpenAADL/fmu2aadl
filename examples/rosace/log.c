#include <stdio.h>
#include <stdlib.h>
#include "types.h"
#define FMTFLOAT "%5.5f"

void rosace_log
    (double t,
    double va,
    double az,
    double q,
    double vz,
    double h,
    double delta_th_c,
    double delta_e_c)
{

  static int first=0;
  if (first == 0) {
    printf("# %15s, %15s, %15s, %15s, %15s, %15s, %15s, %15s\n",
           "T","Va","az","q","Vz","h","delta_th_c","delta_e_c");
    first++;
  }

  printf("%3.4f, ", t);
  printf(FMTFLOAT", ", va);
  printf(FMTFLOAT", ", az);
  printf(FMTFLOAT", ", q);
  printf(FMTFLOAT", ", vz);
  printf(FMTFLOAT", ", h);
  printf(FMTFLOAT", ", delta_th_c);
  printf(FMTFLOAT"\n", delta_e_c);
  //  if (first == 2)
  //    exit (0);
}
