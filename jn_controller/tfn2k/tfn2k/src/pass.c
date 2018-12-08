/* PASS.h - temporary password include
   DELETE this file after compilation ! */

#include "aes.h"

char
 _c1 = 49 + 26,
 _c2 = 50 + 26,
 _c3 = 51 + 26,
 _c4 = 52 + 26,
 _c5 = 53 + 26,
 _c6 = 54 + 26,
 _c7 = 55 + 26,
 _c8 = 56 + 26,
 _c9 = 0 + 26,
 _c10 = 0 + 26,
 _c11 = 0 + 26,
 _c12 = 0 + 26,
 _c13 = 0 + 26,
 _c14 = 0 + 26,
 _c15 = 0 + 26,
 _c16 = 0 + 26,
 _c17 = 0 + 26,
 _c18 = 0 + 26,
 _c19 = 0 + 26,
 _c20 = 0 + 26,
 _c21 = 0 + 26,
 _c22 = 0 + 26,
 _c23 = 0 + 26,
 _c24 = 0 + 26,
 _c25 = 0 + 26,
 _c26 = 0 + 26,
 _c27 = 0 + 26,
 _c28 = 0 + 26,
 _c29 = 0 + 26,
 _c30 = 0 + 26,
 _c31 = 0 + 26,
 _c32 = 0 + 26;

 int al = 26;

void security_through_obscurity ( int sw1tch )
{
char hi[32];

if (!sw1tch) aes_setkey("");
  else
 {
 hi[0] = _c1 - al;
 hi[1] = _c2 - al;
 hi[2] = _c3 - al;
 hi[3] = _c4 - al;
 hi[4] = _c5 - al;
 hi[5] = _c6 - al;
 hi[6] = _c7 - al;
 hi[7] = _c8 - al;
 hi[8] = _c9 - al;
 hi[9] = _c10 - al;
 hi[10] = _c11 - al;
 hi[11] = _c12 - al;
 hi[12] = _c13 - al;
 hi[13] = _c14 - al;
 hi[14] = _c15 - al;
 hi[15] = _c16 - al;
 hi[16] = _c17 - al;
 hi[17] = _c18 - al;
 hi[18] = _c19 - al;
 hi[19] = _c20 - al;
 hi[20] = _c21 - al;
 hi[21] = _c22 - al;
 hi[22] = _c23 - al;
 hi[23] = _c24 - al;
 hi[24] = _c25 - al;
 hi[25] = _c26 - al;
 hi[26] = _c27 - al;
 hi[27] = _c28 - al;
 hi[28] = _c29 - al;
 hi[29] = _c30 - al;
 hi[30] = _c31 - al;
 hi[31] = _c32 - al;
 aes_setkey(hi);
 }
}
