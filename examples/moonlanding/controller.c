#include <stdio.h>
#include <stdlib.h>
#include "fmi2.h"

/******************************************************************************/
void controller
    (fmi2Real a_in,
     fmi2Real* thrust_out,
     fmi2Real v_in)
{
  const float dt = 0.01;
  static float current_time = 0.0;

  /* This controller brings the lander close to the ground, at
     around t = 59.4, after that the lander eventually flies back */

  if (current_time >= 0.0
      && current_time  < 59.4)
    *thrust_out = 2568500.0;
  else
    if (current_time < 100.0)
      *thrust_out = 140000.0;
    else
      *thrust_out = 0.0;

  printf ("%f %f %f\n", current_time, a_in, *thrust_out);

  current_time += dt;
}
