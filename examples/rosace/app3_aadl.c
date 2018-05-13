#include <stdio.h>
#include "common.h"
#include "io.h"

#include "deployment.h"
#include "request.h"
#include "po_hi_gqueue.h"
#include "po_hi_task.h"
#include <app3_code.c>

/* Helper macros to access AADL entities                                     */

#define LOCAL_PORT(THREAD_INSTANCE_NAME, PORT_NAME) THREAD_INSTANCE_NAME ## _local_ ## PORT_NAME
#define REQUEST_PORT(THREAD_INSTANCE_NAME, PORT_NAME) THREAD_INSTANCE_NAME ## _global_ ## PORT_NAME
#define PORT_VARIABLE(THREAD_INSTANCE_NAME, PORT_NAME) vars.REQUEST_PORT(THREAD_INSTANCE_NAME,PORT_NAME).REQUEST_PORT(THREAD_INSTANCE_NAME,PORT_NAME)


void altitude_hold_aadl (double h_f, double h_c, double* output) {
  *output = (double) altitude_hold
    ((float) h_f,
     (float) 10000.0 /*h_c*/);
}

void vz_control_aadl (double vz_f, double vz_c, double q_f, double az_f, double* output) {
  *output = (double) Vz_control
    ((float) vz_f,
     (float) vz_c,
     (float) q_f,
     (float) az_f);
}

void va_control_aadl (double va_f, double vz_f, double q_f, double va_c, double* output) {
  *output = (double) Va_control
    ((float) va_f,
     (float) vz_f,
     (float) q_f,
     (float) 230.0 /*va_c*/);
}

void init_aircraft (void) {

  __po_hi_request_t request;

  request.port = REQUEST_PORT (aircraft_dynamics, t);
  request.PORT_VARIABLE (aircraft_dynamics, t) = (double) 41813.92119463;
  __po_hi_gqueue_store_in
    (software_aircraft_dynamics_k,
     LOCAL_PORT (aircraft_dynamics, t),
     &request);

  request.port = REQUEST_PORT (aircraft_dynamics, delta_e);
  request.PORT_VARIABLE (aircraft_dynamics, delta_e) = (double) 0.012009615652468;
  __po_hi_gqueue_store_in
    (software_aircraft_dynamics_k,
     LOCAL_PORT (aircraft_dynamics, delta_e),
     &request);

}
