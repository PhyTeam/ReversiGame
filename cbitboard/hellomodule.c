#include <Python.h>
////////////////////////////////////////////////////////////
// HEADER
///////////////////////////////////////////////////////////
typedef unsigned long long U64;
#define C64(constantU64) constantU64##ULL

#define USE_GAS_X64 1

int popcount_3(uint64_t x);
int popcount(uint64_t x);
int first_bit(unsigned long long);
int next_bit(unsigned long long*);
#define foreach_bit(i, b) for (i = first_bit(b); b; i = next_bit(&b))

static PyObject* get_moves(PyObject* self, PyObject* args);

////////////////////////////////////////////////////////////
// Implementation
///////////////////////////////////////////////////////////

//types and constants used in the functions below

const uint64_t m1  = 0x5555555555555555; //binary: 0101...
const uint64_t m2  = 0x3333333333333333; //binary: 00110011..
const uint64_t m4  = 0x0f0f0f0f0f0f0f0f; //binary:  4 zeros,  4 ones ...
const uint64_t m8  = 0x00ff00ff00ff00ff; //binary:  8 zeros,  8 ones ...
const uint64_t m16 = 0x0000ffff0000ffff; //binary: 16 zeros, 16 ones ...
const uint64_t m32 = 0x00000000ffffffff; //binary: 32 zeros, 32 ones
const uint64_t hff = 0xffffffffffffffff; //binary: all ones
const uint64_t h01 = 0x0101010101010101; //the sum of 256 to the power of 0,1,2,3..

U64 SHIFT_LEFT_MASK = 0x8080808080808080;
U64 SHIFT_RIGHT_MASK = 0x101010101010101;

U64 INV_SHIFT_LEFT_MASK = 0x7f7f7f7f7f7f7f7f;
U64 INV_SHIFT_RIGHT_MASK = 0xEFEFEFEFEFEFEEEE;

#define _BIT_SHIFT_LEFT

//This uses fewer arithmetic operations than any other known
//implementation on machines with fast multiplication.
//It uses 12 arithmetic operations, one of which is a multiply.
int popcount_3(uint64_t x) {
    x -= (x >> 1) & m1;             //put count of each 2 bits into those 2 bits
    x = (x & m2) + ((x >> 2) & m2); //put count of each 4 bits into those 4 bits
    x = (x + (x >> 4)) & m4;        //put count of each 8 bits into those 8 bits
    return (x * h01)>>56;  //returns left 8 bits of x + (x<<8) + (x<<16) + (x<<24) + ...
}
/*
 * Using advandce bit count
 */


int popcount(uint64_t x){
  #if defined(USE_GAS_X64)
    __asm__("popcntq %1,%0" :"=r" (x) :"rm" (x));
  return (int) x;
  #elif defined(USE_MSVC_X64)
      return __popcnt64(x);
  #elif defined(USE_GCC_X64)
      return __builtin_popcountll(x);
  #endif
  // Just using C code
  return popcount_3(x);
}

/**
 *
 * @brief Search the first bit set.
 *
 * On CPU with AMD64 or EMT64 instructions, a fast asm
 * code is provided. Alternatively, a fast algorithm based on
 * magic numbers is provided.
 *
 * @param b 64-bit integer.
 * @return the index of the first bit set.
 */
int first_bit(unsigned long long b)
{
#if defined(USE_GAS_X64)

	__asm__("bsfq %1,%0" : "=r" (b) : "rm" (b));
	return (int) b;

#elif defined(USE_GAS_X86)

  int x1, x2;
	__asm__ ("bsf %0,%0\n"
	         "jnz 1f\n"
	         "bsf %1,%0\n"
	         "jz 1f\n"
	         "addl $32,%0\n"
		     "1:": "=&q" (x1), "=&q" (x2):"1" ((int) (b >> 32)), "0" ((int) b));
	return x1;

#elif defined(USE_MSVC_X64)

	unsigned long index;
	_BitScanForward64(&index, b);
	return (int) index;

#elif defined(USE_GCC_X64)

	return __builtin_ctzll(b);

#elif defined(USE_MASM_X86)
	__asm {
		xor eax, eax
		bsf edx, dword ptr b
		jnz l1
		bsf edx, dword ptr b+4
		mov eax, 32
		jnz l1
		mov edx, -32
	l1:	add eax, edx
	}

#elif defined(USE_GCC_ARM)
	const unsigned int lb = (unsigned int)b;
	if (lb) {
		return  __builtin_clz(lb & -lb) ^ 31;
	} else {
		const unsigned int hb = b >> 32;
		return 32 + (__builtin_clz(hb & -hb) ^ 31);
	}

#else

	const int magic[64] = {
		63, 0, 58, 1, 59, 47, 53, 2,
		60, 39, 48, 27, 54, 33, 42, 3,
		61, 51, 37, 40, 49, 18, 28, 20,
		55, 30, 34, 11, 43, 14, 22, 4,
		62, 57, 46, 52, 38, 26, 32, 41,
		50, 36, 17, 19, 29, 10, 13, 21,
		56, 45, 25, 31, 35, 16, 9, 12,
		44, 24, 15, 8, 23, 7, 6, 5
	};

	return magic[((b & (-b)) * 0x07EDD5E59A4E28C2ULL) >> 58];

#endif
}

/**
 * @brief Search the next bit set.
 *
 * In practice, clear the first bit set and search the next one.
 *
 * @param b 64-bit integer.
  * @return the index of the next bit set.
 */
int next_bit(unsigned long long *b)
{
	*b &= *b - 1;
	return first_bit(*b);
}

#define UP 0
#define DOWN 1
#define LEFT 2
#define RIGHT 3
#define LEFT_UP 4
#define LEFT_RIGHT 5
#define RIGHT_DOWN 6
#define RIGHT_UP 7

inline U64 dilation(int i, U64 bits)
{
    switch (i) {
      case UP:
        return (bits << 8);
      case DOWN:
        return (bits >> 8);
      case LEFT:
        return (bits >> 1) & INV_SHIFT_LEFT_MASK;
      case RIGHT:
        return (bits << 1) & INV_SHIFT_RIGHT_MASK;
      case LEFT_UP:
        return ((bits >> 1) & INV_SHIFT_LEFT_MASK) << 8;
      case LEFT_RIGHT:
        return ((bits << 1) & INV_SHIFT_RIGHT_MASK) << 8;
      case RIGHT_UP:
        return ((bits >> 1) & INV_SHIFT_LEFT_MASK) >> 8;
      case RIGHT_DOWN:
        return ((bits << 1) & INV_SHIFT_RIGHT_MASK) >> 8;
    }
    return 0;
}

static PyObject*
get_moves(PyObject* self, PyObject* args)
{
  unsigned long long black = 0;
  unsigned long long white = 0;
  int p = 0;
  if (!PyArg_ParseTuple(args, "KKi", &black, &white, &p))
    return NULL;

  printf("Black : %d\n", popcount(black));
  printf("White : %d\n", popcount(white));

  // Get empty squares
  U64 empty = ~( black | white );
  U64 opponent =  (p == 1) ? white : black;
  U64 player = (p == 1) ? black : white;
  printf("empty = %llu\n", empty);
  int i;
  U64*  moves = malloc(8 * sizeof(U64));
  for(i = 0; i < 8; i++){
    U64 candidates = opponent & dilation(i, player);
    while (candidates != 0)
    {
        moves[i] |= empty & dilation(i, candidates);
        candidates = opponent & dilation(i, candidates);
    }
  }
  U64 k = 0;
  for (i = 0; i < 8; i++)
  {
      U64 m = moves[i];
      k |= m;
      int index = 0;
      if (m != 0 ){
        foreach_bit(index, m){
          printf("Valid move: (%d, %d)\n", index / 8, index % 8);
        }
      }
  }

  printf("%d\n",k);

  Py_RETURN_NONE;
}

static PyObject*
say_hello(PyObject* self, PyObject* args)
{
    const char* name;

    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;

    printf("Hello %s!\n", name);

    Py_RETURN_NONE;
}

static PyMethodDef HelloMethods[] =
{
     {"say_hello", say_hello, METH_VARARGS, "Greet somebody."},
     {"get_moves", get_moves, METH_VARARGS, "Generate all avilable moves"},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
inithello(void)
{
     (void) Py_InitModule("hello", HelloMethods);
}
