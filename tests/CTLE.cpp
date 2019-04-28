#ifdef WIN32
#include <CON>
#else
#include </dev/random>
#endif
#include <bits/stdc++.h>
int main() {
  int n, m;
  std::cin >> n >> m;
  std::cout << n + m << std::endl;
  return 0;
}
