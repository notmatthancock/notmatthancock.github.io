#include <stdio.h>
#include "stack.h"

int main() {
    stack S;
    element * el;
    int N = 3;

    stack_init(&S);

    for(int i=0; i < N; i++) {
        el = (element *) malloc(sizeof(element));
        element_init(el, i, i, i);
        stack_push(&S, el);
        printf("Stack top->i after push: %d\n", S.top->i);
    }

    for(int i=0; i < N; i++) {
        printf("n_elements before pop: %d\n", S.n_elements);
        el = stack_pop(&S);
        printf("n_elements after pop: %d\n", S.n_elements);
        free(el);
    }
        
    return 0;
}
