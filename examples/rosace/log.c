#include <stdio.h>
#include "types.h"
#define FMTFLOAT "%5.15f"

void rosace_log
    (float t,
    float va,
    float az,
    float q,
    float vz,
    float h,
    float delta_th_c,
    float delta_e_c)
{

  static int first=1;
  if (first) {
    printf("# %15s, %15s, %15s, %15s, %15s, %15s, %15s, %15s\n",
           "T","Va","az","q","Vz","h","delta_th_c","delta_e_c");
    first = 0;
  }

  printf("%3.4f, ", t);
  printf(FMTFLOAT", ", va);
  printf(FMTFLOAT", ", az);
  printf(FMTFLOAT", ", q);
  printf(FMTFLOAT", ", vz);
  printf(FMTFLOAT", ", h);
  printf(FMTFLOAT", ", delta_th_c);
  printf(FMTFLOAT"\n", delta_e_c);

}
