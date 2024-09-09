#include "test_file.h"

#include <stdio.h>

/* comment */

#if 0
	#define TEST	21	/* A */
#else
	#define TEST	42	/* B */
#endif

typedef struct toto_s
{
  int a;
} toto_t, *toto_p;

enum tutu_e
  {
   AAA,
   BBB,
  };

void too_many_parameters(int a, int b, int c, int d, int             e)	/* end */
{
  return a;
}

void too_many_parameters_2(int a,
			   int b,
			   int c,
			   int d,
 /* test */		   void             * echo,
			   void* gamma)	/* end */
{
  return a;
}

int main_mlfsmfkjsqfqsfskfns_fsfsfsqfjsqjfs_fdsfmskfjslfjsmlfjqmfj(void)
{
  toto_t toto;

  toto.a = AAA;
  printf("%d; %d\n", TEST, toto.a);
  /* comment */
  return 0;
}
