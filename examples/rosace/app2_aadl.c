#include "common.h"
#include "io.h"

#include "app2_code.c"

void va_filter_aadl (float va, float* output) {
  *output = (double) Va_filter ((float) va);
}

void h_filter_aadl (float h, float* output) {
  *output = (double) h_filter ((float) h);
}

void az_filter_aadl (float az, float* output) {
  *output = (double) az_filter ((float) az);
}

void vz_filter_aadl (float vz, float* output) {
  *output = (double) Vz_filter ((float) vz);
}

void q_filter_aadl (float q, float* output) {
  *output = (double) q_filter ((float) q);
}
