// RUN: %clang_cc1 -fsyntax-only -fblocks %s -verify

#define SUPPRESS1 __attribute__((suppress))
#define SUPPRESS2(...) __attribute__((suppress(__VA_ARGS__)))

SUPPRESS1 int global = 42;

SUPPRESS1 void foo() {
  SUPPRESS1 int *p; // no-warning

  SUPPRESS1 int a = 0; // no-warning
  SUPPRESS2()
  int b = 1; // no-warning
  SUPPRESS2("a")
  int c = a + b;                     // no-warning
  SUPPRESS2("a", "b") { b = c - a; } // no-warning

  SUPPRESS2("a", "b")
  if (b == 10)
    a += 4;              // no-warning
  SUPPRESS1 while (1) {} // no-warning
  SUPPRESS1 switch (a) { // no-warning
  default:
    c -= 10;
  }

  // GNU-style attributes and C++11 attributes apply to different things when
  // written like this.  GNU  attribute gets attached to the declaration, while
  // C++11 attribute ends up on the type.
  int SUPPRESS2("r") z; // no-warning
  SUPPRESS2(foo) // no-warning
  float f;
  // expected-error@-2 {{'suppress' attribute requires a string}}
}

union SUPPRESS2("type.1") U { // no-warning
  int i;
  float f;
};

SUPPRESS1 @interface Test { // no-warning
}
@property SUPPRESS2("prop") int *prop; // no-warning
- (void)bar:(int)x SUPPRESS1; // no-warning
@end
