//
//  libCombineArrays
//
//  Created by Norbert Henseler on 16/3/22.
//
#include <iostream>
using namespace std;

//
// Three at the moment identical versions of combine arrays z, r and return result in array y
// y_j = sum_i z(i*n+j)*r(i*n+j), i=0,..,m, j = 0,..,n
// m: num rows
// n: num columns
// 
extern "C"
{
    extern int combine_arrays_v1( int *pz, double *pr, double *py, int n, int m)
    {		
		for( int j = 0; j < n; j++){
            py[j] = 0;
            for( int i = 0; i < m; i++){
                py[j] = py[j] + pz[i * n + j] * pr[i * n + j];
            }
		}
        return 1;
    }
	
    extern int combine_arrays_v2( int *pz, double *pr, double *py, int n, int m)
    {		
		for( int j = 0; j < n; j++){
            py[j] = 0;
            for( int i = 0; i < m; i++){
                py[j] = py[j] + pz[i * n + j] * pr[i * n + j];
            }
		}
        return 1;
    }
	
    extern int combine_arrays_v3( int *pz, double *pr, double *py, int n, int m)
    {		
		for( int j = 0; j < n; j++){
            py[j] = 0;
            for( int i = 0; i < m; i++){
                py[j] = py[j] + pz[i * n + j] * pr[i * n + j];
            }
		}
        return 1;
    }
	
}


int main(int argc, const char * argv[]) {
    // insert code here...
    std::cout << "Hello, World!\n";
	return 0;
}
