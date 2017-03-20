#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>
#include <cstdlib>

namespace mtx {
    template<class T>
    class matrix {
    public:
        // Default empty constructor.
        matrix() {}

        // Constructor from matrix dimensions.
        matrix(int m, int n) {
            this->m = m; this->n = n;
            this->data = new T[m*n];
            // Initialize to zeros.
            for(int i=0; i < m*n; i++) this->data[i] = T(0);
        }

        // Copy constructor.
        matrix(const matrix & src) : matrix(src.m, src.n) {
            for(int i=0; i < m; i++) {
                for(int j=0; j < n; j++) {
                    (*this)(i,j) = src(i,j);
                }
            }
        }

        // Destructor.
        ~matrix() { delete [] this->data; }

        int n_rows() const { return this->m; }
        int n_cols() const { return this->n; }
        
        // Element accessor.
        T & operator()(int i, int j) const {
            #ifndef NDEBUG
            check_indices(i,j);
            #endif

            // Data stored in row-major.
            int k = i*this->n + j;

            return this->data[k];
        }
    protected:
        T * data;
        int m; // n_rows
        int n; // n_cols
        void check_indices(int i, int j) const {
            if (i < 0 || i >= this->m) {
                std::cerr << "Invalid row index, " << i << ".\n"
                          << "Valid row indices are: 0-" << (this->m-1)
                          << ".\n";
                exit(1);
            }
            if (j < 0 || j >= this->n) {
                std::cerr << "Invalid column index, " << j << ".\n"
                          << "Valid column indices are: 0-" << (this->n-1)
                          << ".\n";
                exit(1);
            }
        }
    };
}

#endif
